"""Re-apply your hand edits of generated files to newly generated files (three-way merge).

Usage (from Network_CodeGen_S220):
  .venv/Scripts/python.exe tools/carry_forward.py --base <old generated files> --edited <workspace>
        --new CODE_GEN --out <new folder> [--report <file.md>]

  --base    the generated files your edits started from (e.g. CODE_GEN/DBC_40024)
  --edited  your workspace (or a folder); each file is found by its name and must be unique there
  --new     the newly generated files (normally CODE_GEN)
  --out     folder for the merged files; it must not exist yet or be empty, and must not be inside
            --edited, --base or --new

For every generated file the changes base -> edited are applied to the new file (git merge-file,
diff3 style). Where the new generation changed the same lines as your edit:
  - if both versions differ only in white space or blank lines, your version is kept;
  - if only the header stamp (Date / By / Traceability) differs, the new stamp is kept;
  - otherwise both versions stay in the file between conflict markers and the report lists them
    under "Manual Action Required".
If your file's header names a different DBC than the --base file, its differences may come from
that other generation rather than from hand edits; the report says so.
--base, --edited and --new are only read. Exit code: 0 when everything merged, 1 when conflicts or
missing files need you, 2 on usage errors."""
import argparse
import difflib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

GENERATED_FILES = ["can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
                   "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
                   "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h"]
LABELS = ("new generation", "previous generation", "your edit")


class UsageError(Exception):
    pass


def _read(path):
    raw = Path(path).read_bytes().decode("latin-1")
    return raw.replace("\r\n", "\n"), ("\r\n" if "\r\n" in raw else "\n")


def _find(root, name):
    root = Path(root)
    if (root / name).is_file():
        return root / name, None
    hits = sorted(p for p in root.rglob(name) if p.is_file())
    if len(hits) == 1:
        return hits[0], None
    return None, ("not found in %s" % root) if not hits else ("%d files named %s in %s: %s" % (
        len(hits), name, root, ", ".join(str(h.relative_to(root)) for h in hits)))


def _inside(path, folder):
    path, folder = Path(path).resolve(), Path(folder).resolve()
    return path == folder or folder in path.parents


def _edit_count(a, b):
    sm = difflib.SequenceMatcher(None, a.split("\n"), b.split("\n"), autojunk=False)
    return sum(1 for op in sm.get_opcodes() if op[0] != "equal")


STAMP = re.compile(r"^(Date|By|Traceability)\s*:")


def _norm(lines):
    return [re.sub(r"\s+", " ", l).strip() for l in lines if l.strip()]


def traceability(text):
    m = re.search(r"^Traceability\s*:\s*(.*?)\s*$", text, re.M)
    return m.group(1) if m else None


def merge3(new, base, edited):
    """(merged text, conflicts, auto-resolved counts) with LF line ends;
    conflicts = [(line, new lines, base lines, edited lines)]."""
    if edited == base:
        return new, [], {}
    if new == base or new == edited:
        return edited, [], {}
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, text in zip(("new", "base", "edited"), (new, base, edited)):
            p = os.path.join(tmp, name)
            with open(p, "w", encoding="latin-1", newline="\n") as fh:
                fh.write(text)
            paths.append(p)
        cmd = ["git", "merge-file", "-p", "--diff3", "--diff-algorithm=histogram",
               "-L", LABELS[0], "-L", LABELS[1], "-L", LABELS[2]] + paths
        try:
            r = subprocess.run(cmd, capture_output=True)
        except FileNotFoundError:
            raise UsageError("git is needed for the three-way merge but was not found on PATH")
        if r.returncode < 0 or r.returncode > 127:
            raise UsageError("git merge-file failed: %s" % r.stderr.decode("utf-8", "replace").strip())
        merged = r.stdout.decode("latin-1")
    return _resolve(merged)


def _resolve(text):
    """Resolve white-space-only and header-stamp-only conflicts; list the others."""
    lines, out, conflicts, auto = text.split("\n"), [], [], {"white space": 0, "header stamp": 0}
    i = 0
    while i < len(lines):
        if not lines[i].startswith("<<<<<<< "):
            out.append(lines[i])
            i += 1
            continue
        parts, markers, part = ([], [], []), [lines[i]], 0
        j = i + 1
        while not lines[j].startswith(">>>>>>> "):
            if lines[j].startswith("||||||| ") and part == 0:
                part = 1
                markers.append(lines[j])
            elif lines[j] == "=======" and part in (0, 1):
                part = 2
                markers.append(lines[j])
            else:
                parts[part].append(lines[j])
            j += 1
        new, base, edited = parts
        if _norm(new) == _norm(edited):
            out += edited
            auto["white space"] += 1
        elif all(STAMP.match(l) for l in new + base + edited if l.strip()):
            out += new
            auto["header stamp"] += 1
        else:
            conflicts.append((len(out) + 1, new, base, edited))
            out += [markers[0]] + new + [markers[1]] + base + [markers[2]] + edited + [lines[j]]
        i = j + 1
    return "\n".join(out), conflicts, {k: v for k, v in auto.items() if v}


def carry_forward(base_dir, edited_root, new_dir, out_dir):
    """Merge every generated file; returns a list of per-file result dicts."""
    for name, folder in (("--base", base_dir), ("--edited", edited_root), ("--new", new_dir)):
        if not Path(folder).is_dir():
            raise UsageError("%s %s is not a folder" % (name, folder))
        if _inside(out_dir, folder):
            raise UsageError("--out %s must not be inside %s %s (that folder is only read)" % (out_dir, name, folder))
    if Path(out_dir).exists() and any(Path(out_dir).iterdir()):
        raise UsageError("--out %s is not empty; choose a new folder so no earlier result is overwritten" % out_dir)
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for name in GENERATED_FILES:
        new_path = Path(new_dir) / name
        if not new_path.is_file():
            results.append({"file": name, "status": "skipped", "detail": "not in --new", "conflicts": [], "edits": 0,
                            "auto": {}, "origin": None, "edited_path": None})
            continue
        new, eol = _read(new_path)
        edited_path, why_edited = _find(edited_root, name)
        base_path = Path(base_dir) / name
        res = {"file": name, "edited_path": str(edited_path) if edited_path else None, "conflicts": [], "edits": 0,
               "auto": {}, "origin": None}
        if edited_path is None:
            merged, res["status"], res["detail"] = new, "new file taken", "your file: " + why_edited
        elif not base_path.is_file():
            merged, res["status"], res["detail"] = new, "new file taken", "no %s in --base, so your edits are unknown" % name
        else:
            base, _ = _read(base_path)
            edited, _ = _read(edited_path)
            res["edits"] = _edit_count(base, edited)
            merged, res["conflicts"], res["auto"] = merge3(new, base, edited)
            if res["conflicts"]:
                res["status"] = "CONFLICTS"
            elif res["edits"] == 0:
                res["status"] = "no hand edits"
            else:
                res["status"] = "merged"
            res["detail"] = "; ".join("%d %s conflict(s) resolved" % (n, kind) for kind, n in res["auto"].items())
            mine, theirs = traceability(edited), traceability(base)
            if mine and theirs and mine != theirs:
                res["origin"] = (mine, theirs)
                res["detail"] = "; ".join(x for x in (res["detail"], "your file was generated from %s" % mine) if x)
        with open(Path(out_dir) / name, "w", encoding="latin-1", newline=eol) as fh:
            fh.write(merged)
        results.append(res)
    return results


def report(results, base_dir, edited_root, new_dir, out_dir):
    lines = ["# Hand edits carried forward", "",
             "Previous generation (base): `%s`  " % base_dir, "Your edited files: `%s`  " % edited_root,
             "New generation: `%s`  " % new_dir, "Merged result: `%s`" % out_dir, "",
             "| File | Result | Your edit regions | Conflicts | Note |", "|---|---|---|---|---|"]
    for r in results:
        lines.append("| %s | %s | %d | %d | %s |" % (r["file"], r["status"], r["edits"], len(r["conflicts"]), r.get("detail", "")))
    needs = [r for r in results if r["conflicts"] or r["origin"] or r["status"] in ("new file taken", "skipped")]
    lines += ["", "White-space-only conflicts keep your formatting; header-stamp-only conflicts keep the new "
              "Date / By / Traceability lines.", "", "## Manual Action Required", ""]
    if not needs:
        lines += ["None. Review the merged files (your edits were applied without conflicts), then copy them into "
                  "your workspace.", ""]
    n = 0
    for r in results:
        if r["origin"]:
            n += 1
            mine, theirs = r["origin"]
            lines += ["### %d. %s: REVIEW, your file comes from another generation" % (n, r["file"]), "",
                      "- **File and location:** %s (header Traceability)" % r["edited_path"],
                      "- **Current value:** your file was generated from `%s`; --base was generated from `%s`" % (mine, theirs),
                      "- **Required change:** confirm that the %d region(s) where your file differs from --base are "
                      "edits you want to keep; differences that only come from the older generation should be dropped"
                      % r["edits"],
                      "- **Why not automatic:** the tool cannot tell an old generated line from a hand edit",
                      "- **Dependencies:** the other files of the same generation",
                      "- **Steps:** compare your file with the generated file of `%s` (if you still have that run, pass it "
                      "as --base for this file); remove differences you do not want from %s"
                      % (mine, os.path.join(out_dir, r["file"])),
                      "- **Verification:** tools/compare_reference.py --generated <out> --reference <workspace> shows only intended differences", ""]
        if r["status"] in ("new file taken", "skipped") and not r["conflicts"]:
            n += 1
            lines += ["### %d. %s: %s" % (n, r["file"], r["status"]), "",
                      "- **File and location:** %s (whole file)" % r["file"],
                      "- **Current value:** %s" % r["detail"],
                      "- **Required change:** if you edited this file by hand, apply those edits to %s again"
                      % os.path.join(out_dir, r["file"]),
                      "- **Why not automatic:** without the previous generated file and your edited file no edit can be derived",
                      "- **Dependencies:** none known",
                      "- **Steps:** pass the folder that contains the file with --base / --edited, or edit by hand",
                      "- **Verification:** tools/compare_reference.py shows only intended differences", ""]
        for line, new, base, edited in r["conflicts"]:
            n += 1
            lines += ["### %d. %s line %d: the new generation changed lines you edited" % (n, r["file"], line), "",
                      "- **File and location:** %s, conflict starting at line %d" % (os.path.join(out_dir, r["file"]), line),
                      "- **Current value (new generation):**", "", "```", *(new or ["(nothing)"]), "```", "",
                      "- **Previous generation (your edit was based on this):**", "", "```", *(base or ["(nothing)"]), "```", "",
                      "- **Your edit:**", "", "```", *(edited or ["(nothing)"]), "```", "",
                      "- **Required change:** decide which content is right for the new generation and keep only that",
                      "- **Why not automatic:** the generator changed the same lines; only you know whether your edit still applies",
                      "- **Dependencies:** other conflicts of the same message or signal (often in nw_il_par.h/.c and nw_vnim_app_signals_par.h/.c together)",
                      "- **Steps:** open the file at line %d, edit the block between `<<<<<<< %s` and `>>>>>>> %s`, delete the marker lines"
                      % (line, LABELS[0], LABELS[2]),
                      "- **Verification:** no line starting with `<<<<<<<`, `|||||||`, `=======` or `>>>>>>>` remains; the project builds", ""]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in ("--base", "--edited", "--new", "--out"):
        p.add_argument(name, required=True)
    p.add_argument("--report", help="write the Markdown report here (default: <out>/CARRY_FORWARD.md)")
    a = p.parse_args(argv)
    try:
        results = carry_forward(a.base, a.edited, a.new, a.out)
    except UsageError as exc:
        print("carry_forward: %s" % exc, file=sys.stderr)
        return 2
    text = report(results, a.base, a.edited, a.new, a.out)
    report_path = a.report or os.path.join(a.out, "CARRY_FORWARD.md")
    Path(report_path).write_text(text, encoding="utf-8")
    print(text)
    print("\nReport: %s" % report_path)
    return 1 if any(r["conflicts"] or r["origin"] or r["status"] in ("new file taken", "skipped") for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
