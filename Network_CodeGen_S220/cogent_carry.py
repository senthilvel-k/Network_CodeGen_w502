"""Re-apply hand edits of generated files to a new generation (three-way merge), for the GUI page
'Re-apply edits' and tools/carry_forward.py.

  base   the generated files the edits started from (e.g. CODE_GEN/DBC_40024)
  edited the workspace (each generated file is found by its name and must be unique there)
  new    the new generation (normally CODE_GEN)
  out    a new or empty folder, not inside the other three (they are only read)

For every generated file the changes base -> edited are applied to the new file (git merge-file,
diff3). Then:
  - can_rxrule.cfg and nw_can_dll.h are taken from the new generation: they are produced by the
    Receive FIFO settings (merging them can duplicate dispatch tables);
  - white-space-only conflicts keep your formatting, header-stamp-only conflicts the new stamp;
  - values derived from the message list are recomputed: IL_RX_NUM_* (new value + your change),
    IL_MUX_MSG_OFFSET_ID / IL_NUM_OF_RX_DATA_CHANGED_FLAG (first flag byte after the generated ones),
    the VNIM_*_MESSAGE handle numbers (enum order, then Diag/NM handles) and the per-message arrays
    vnim_msg_byte_position / vnim_msg_bit_mask;
  - the result is checked (conflict markers, definitions lost or doubled, table sizes and order).
Everything else that overlaps stays between conflict markers and is listed under Manual Action Required."""
import difflib
import os
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

GENERATED_FILES = ["can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
                   "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
                   "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h"]
FIFO_FILES = ("can_rxrule.cfg", "nw_can_dll.h")
ENUM_FILE, IL_PAR_H, VNIM_C = "nw_vnim_app_signals_par.h", "nw_il_par.h", "nw_vnim_app_signals_par.c"
LABELS = ("new generation", "previous generation", "your edit")
MESSAGE_ARRAYS = ("vnim_msg_byte_position", "vnim_msg_bit_mask")
MESSAGE_TABLES = {"VNIM_NODE_LIST": 1, "VNIM_MSG_CONTENT_FAILURE_DTC_IDS": 1, "VNIM_SIGNAL_FAULT_LIST": 2}


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
MARKER = re.compile(r"^(<<<<<<< |\|\|\|\|\|\|\| |=======$|>>>>>>> )", re.M)


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
            r = subprocess.run(cmd, capture_output=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except FileNotFoundError:
            raise UsageError("Git is needed for re-applying edits but was not found. Install Git for Windows "
                             "(it adds git to PATH), then run again.")
        if r.returncode < 0 or r.returncode > 127:
            raise UsageError("git merge-file failed: %s" % r.stderr.decode("utf-8", "replace").strip())
        merged = r.stdout.decode("latin-1")
    return _resolve(merged)


def _blocks(text):
    """Split merged text into plain lines and conflict blocks [new, base, edited, markers]."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if not lines[i].startswith("<<<<<<< "):
            out.append(lines[i])
            i += 1
            continue
        parts, markers, part, j = ([], [], []), [lines[i]], 0, i + 1
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
        markers.append(lines[j])
        out.append(list(parts) + [markers])
        i = j + 1
    return out


def _join(blocks, resolver=None):
    """Text from _blocks output; resolver(new, base, edited) -> lines or None decides each conflict."""
    out, conflicts = [], []
    for b in blocks:
        if isinstance(b, str):
            out.append(b)
            continue
        new, base, edited, markers = b
        lines = resolver(new, base, edited) if resolver else None
        if lines is not None:
            out += lines
            continue
        conflicts.append((len(out) + 1, new, base, edited))
        out += [markers[0]] + new + [markers[1]] + base + [markers[2]] + edited + [markers[3]]
    return "\n".join(out), conflicts


def _resolve(text):
    """Resolve white-space-only and header-stamp-only conflicts; list the others."""
    auto = Counter()

    def resolver(new, base, edited):
        if _norm(new) == _norm(edited):
            auto["white space"] += 1
            return edited
        if all(STAMP.match(l) for l in new + base + edited if l.strip()):
            auto["header stamp"] += 1
            return new
        return None
    merged, conflicts = _join(_blocks(text), resolver)
    return merged, conflicts, dict(auto)


# ---- values derived from the message list ---------------------------------------------------------
DEFINE = re.compile(r"^(#define\s+)(\w+)(\s+)(.*?)(\s*)$")
HANDLE = re.compile(r"^#define (VNIM_(\w+?)_MESSAGE)(\s+)(\d+)\s*$")


def message_order(header):
    """VNIM_<name>_MSGID names in enum order (None without a clean enum)."""
    if "NUM_VNIM_MESSAGES" not in header:
        return None
    block = header[:header.index("NUM_VNIM_MESSAGES")]
    if "{" not in block or MARKER.search(block[block.rindex("{"):]):
        return None
    return re.findall(r"VNIM_(\w+?)_MSGID", block[block.rindex("{"):])


def _defines(lines):
    return {m.group(2): m.group(4) for m in (DEFINE.match(l) for l in lines) if m}


def _flag_count(new_text):
    m = re.search(r"^#define IL_NUM_OF_RX_DATA_CHANGED_FLAG\s+(\d+)\s*$", new_text, re.M)
    return int(m.group(1)) if m else None


def resolve_counts(new, base, edited, new_text):
    """Conflict of the IL_RX_NUM_* / data-changed-flag defines: your change applied to the new values,
    the multiplex flag offset set to the first flag byte after the generated ones. None if not that block."""
    if not any(l.startswith("#define IL_RX_NUM_") for l in edited):
        return None
    nv, bv, flags = _defines(new), _defines(base), _flag_count(new_text)
    out = []
    for line in edited:
        m = DEFINE.match(line)
        if not m:
            out.append(line)              # comments and blank lines: yours
            continue
        prefix, name, gap, value, trail = m.groups()
        extra = re.fullmatch(r"\(\s*\d+\s*\+\s*(\d+)\s*\)", value)
        if name == "IL_MUX_MSG_OFFSET_ID" and flags is not None:
            value = str(flags)
        elif name == "IL_NUM_OF_RX_DATA_CHANGED_FLAG" and extra and flags is not None:
            value = "(%d + %s)" % (flags, extra.group(1))
        elif value.isdigit() and nv.get(name, "").isdigit() and bv.get(name, "").isdigit():
            value = str(int(nv[name]) + int(value) - int(bv[name]))
        elif nv.get(name) == value:
            pass
        else:
            return None
        out.append(prefix + name + gap + value + trail)
    return out


def _split_handles(lines):
    idx = [i for i, l in enumerate(lines) if HANDLE.match(l)]
    if not idx:
        return lines, [], []
    return lines[:idx[0]], lines[idx[0]:idx[-1] + 1], lines[idx[-1] + 1:]


def _resolve_part(new, base, edited, new_text):
    if _norm(new) == _norm(edited):
        return edited
    if _norm(edited) == _norm(base):
        return new
    if _norm(new) == _norm(base):
        return edited
    return resolve_counts(new, base, edited, new_text)


def resolve_il_par_conflict(new, base, edited, new_text):
    """nw_il_par.h conflict: receive counts recomputed; handle defines kept as placeholders (rebuilt from
    the enum afterwards); anything else in the conflict must be unchanged on one side. None = unresolved."""
    parts = [_split_handles(side) for side in (new, base, edited)]
    if not any(p[1] for p in parts):
        return resolve_counts(new, base, edited, new_text)
    if any(l.strip() and not HANDLE.match(l) for p in parts for l in p[1]):
        return None                                   # other lines between handle defines
    before = _resolve_part(parts[0][0], parts[1][0], parts[2][0], new_text)
    after = _resolve_part(parts[0][2], parts[1][2], parts[2][2], new_text)
    if before is None or after is None:
        return None
    return before + (parts[0][1] or parts[2][1]) + after


def rebuild_handles(text, order, new_text, edited_text):
    """VNIM_*_MESSAGE handle block numbered in enum order, then the other handles (Diag/NM) of the new
    generation (and of your file) in their order. Returns (text, changed)."""
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if HANDLE.match(l)]
    if not idx or idx[-1] - idx[0] + 1 != len(idx):
        return text, False                      # no single contiguous handle block: leave it to the checks
    layout = next((m for m in (HANDLE.match(l) for l in edited_text.split("\n")) if m), None) \
        or HANDLE.match(lines[idx[0]])                     # your column layout, else the generated one
    width = len(layout.group(1)) + len(layout.group(3))
    rest = []
    for source in (new_text, edited_text):
        for m in (HANDLE.match(l) for l in source.split("\n")):
            if m and m.group(2) not in order and m.group(2) not in rest:
                rest.append(m.group(2))
    names = list(order) + rest
    block = ["#define " + ("VNIM_%s_MESSAGE" % n).ljust(max(width, len("VNIM_%s_MESSAGE" % n) + 1)) + str(i)
             for i, n in enumerate(names)]
    if [lines[i] for i in idx] == block:
        return text, False
    return "\n".join(lines[:idx[0]] + block + lines[idx[-1] + 1:]), True


def _array_rows(values):
    rows = [values[i:i + 8] for i in range(0, len(values), 8)]
    return ["    " + ",".join(r) + (",  \\" if k < len(rows) - 1 else "") for k, r in enumerate(rows)]


def rebuild_message_arrays(text, n):
    """vnim_msg_byte_position / vnim_msg_bit_mask with one entry per message (generated layout).
    Returns (text, rebuilt array names)."""
    rebuilt = []
    for name in MESSAGE_ARRAYS:
        m = re.search(r"(%s\[NUM_VNIM_MESSAGES\]\s*=\s*\n\{\n)(.*?)(\n\};)" % name, text, re.S)
        if not m:
            continue
        body = m.group(2)
        count = len([v for v in re.split(r"[,\s\\]+", body) if v])
        if not MARKER.search(body) and count == n:
            continue
        values = ([str(i // 8) for i in range(n)] if name.endswith("position")
                  else ["0x%X" % (1 << (i % 8)) for i in range(n)])
        text = text[:m.start(2)] + "\n".join(_array_rows(values)) + text[m.end(2):]
        rebuilt.append(name)
    return text, rebuilt


# ---- checks of the merged result ---------------------------------------------------------------------
DEF_NAMES = re.compile(r"^\s*#define\s+(\w+)|^\s*(?:static\s+)?(?:const\s+)?\w+(?:\s+const)?\s+(\w+)\s*\[[^\]]*\]\s*=", re.M)


def _definition_counts(text):
    return Counter(a or b for a, b in DEF_NAMES.findall(text))


def duplicate_definitions(merged, new, edited):
    m, n, e = _definition_counts(merged), _definition_counts(new), _definition_counts(edited)
    return ["%s defined %d times (%d in the new generation, %d in your file)" % (k, v, n.get(k, 0), e.get(k, 0))
            for k, v in sorted(m.items()) if v > max(n.get(k, 0), e.get(k, 0))]


def missing_definitions(merged, new, base, edited):
    """Names the new generation defines that the merged file lost (unless you removed them on purpose)."""
    m, n, b, e = (_definition_counts(t) for t in (merged, new, base, edited))
    return sorted(k for k in n if k not in m and not (k in b and k not in e))


def table_problems(text, filename, order):
    problems = []
    n = len(order)
    if filename == ENUM_FILE:
        for name, per in MESSAGE_TABLES.items():
            m = re.search(r"^#define\s+%s\s*\\\n((?:.*\\\n)*.*)$" % name, text, re.M)
            if m:
                body = re.sub(r"/\*.*?\*/", "", m.group(1)).replace("\\", " ")
                count = len([x for x in body.split(",") if x.strip()])
                if count != n * per:
                    problems.append("%s has %d entries for %d messages" % (name, count, n))
    if filename == VNIM_C:
        for name in MESSAGE_ARRAYS:
            m = re.search(r"%s\[NUM_VNIM_MESSAGES\]\s*=\s*\n\{\n(.*?)\n\};" % name, text, re.S)
            if m:
                count = len([v for v in re.split(r"[,\s\\]+", m.group(1)) if v])
                if count != n:
                    problems.append("%s has %d entries for %d messages" % (name, count, n))
    if filename == IL_PAR_H:
        handles = [HANDLE.match(l) for l in text.split("\n")]
        handles = [(h.group(2), int(h.group(4))) for h in handles if h]
        if handles:
            if [name for name, _ in handles[:n]] != list(order):
                problems.append("VNIM_*_MESSAGE handles are not in the order of the VNIM_*_MSGID enum")
            if [v for _, v in handles] != list(range(len(handles))):
                problems.append("VNIM_*_MESSAGE handle numbers are not 0..%d" % (len(handles) - 1))
        m = re.search(r"^#define IL_RX_NUM_MESSAGES\s+(\d+)", text, re.M)
        if m and order and int(m.group(1)) != n:
            problems.append("IL_RX_NUM_MESSAGES is %s, the enum has %d messages" % (m.group(1), n))
        mux = re.search(r"^#define IL_MUX_MSG_OFFSET_ID\s+(\d+)\s*$", text, re.M)
        used = [int(i) for i in re.findall(r"il_Rx_DataChanged_Flag\[\s*(\d+)\s*\]", text)]
        if mux and used and int(mux.group(1)) <= max(used):
            problems.append("IL_MUX_MSG_OFFSET_ID is %s, but the generated data-changed flags use bytes 0..%d: the "
                            "multiplexed signal flags share byte %s with them (the first free byte is %d)"
                            % (mux.group(1), max(used), mux.group(1), max(used) + 1))
    return problems


# ---- the merge ---------------------------------------------------------------------------------------
def carry_forward(base_dir, edited_root, new_dir, out_dir):
    """Merge every generated file into out_dir; returns a list of per-file result dicts."""
    for name, folder in (("previous generation", base_dir), ("workspace", edited_root), ("new generation", new_dir)):
        if not Path(folder).is_dir():
            raise UsageError("the %s folder %s does not exist" % (name, folder))
        if _inside(out_dir, folder):
            raise UsageError("the output folder %s is inside the %s folder %s, which is only read; choose another "
                             "output folder" % (out_dir, name, folder))
    if Path(out_dir).exists() and any(Path(out_dir).iterdir()):
        raise UsageError("the output folder %s is not empty; choose a new folder so no earlier result is "
                         "overwritten" % out_dir)
    os.makedirs(out_dir, exist_ok=True)
    results, texts = [], {}
    for name in GENERATED_FILES:
        res = {"file": name, "status": "", "detail": "", "conflicts": [], "edits": 0, "auto": {}, "origin": None,
               "edited_path": None, "rules_applied": [], "checks": []}
        new_path = Path(new_dir) / name
        if not new_path.is_file():
            res.update(status="skipped", detail="not in the new generation")
            results.append(res)
            continue
        new, eol = _read(new_path)
        edited_path, why_edited = _find(edited_root, name)
        base_path = Path(base_dir) / name
        res["edited_path"] = str(edited_path) if edited_path else None
        base = edited = None
        if edited_path is None:
            merged = new
            res.update(status="new file taken", detail="your file: " + why_edited)
        elif not base_path.is_file():
            merged = new
            res.update(status="new file taken", detail="no %s in the previous generation, so your edits are unknown" % name)
        else:
            base, edited = _read(base_path)[0], _read(edited_path)[0]
            res["edits"] = _edit_count(base, edited)
            if name in FIFO_FILES:
                merged = new
                res.update(status="new generation taken",
                           detail="made from the Receive FIFO settings; %d edit region(s) of your file not re-applied" % res["edits"])
            else:
                merged, res["conflicts"], res["auto"] = merge3(new, base, edited)
                res["detail"] = "; ".join("%d %s conflict(s) resolved" % (n, kind) for kind, n in res["auto"].items())
            mine, theirs = traceability(edited), traceability(base)
            if mine and theirs and mine != theirs:
                res["origin"] = (mine, theirs)
                res["detail"] = "; ".join(x for x in (res["detail"], "your file was generated from %s" % mine) if x)
        texts[name] = {"merged": merged, "new": new, "base": base, "edited": edited, "eol": eol}
        results.append(res)

    by_name = {r["file"]: r for r in results}
    order = message_order(texts[ENUM_FILE]["merged"]) if ENUM_FILE in texts else None
    if order is not None and IL_PAR_H in texts and texts[IL_PAR_H]["edited"] is not None:
        t, r = texts[IL_PAR_H], by_name[IL_PAR_H]
        merged, conflicts = _join(_blocks(t["merged"]), lambda n, b, e: resolve_il_par_conflict(n, b, e, t["new"]))
        if len(conflicts) < len(r["conflicts"]):
            r["rules_applied"].append("receive counts and multiplex flag offset recomputed")
        merged, changed = rebuild_handles(merged, order, t["new"], t["edited"])
        if changed:
            r["rules_applied"].append("VNIM_*_MESSAGE handle numbers rebuilt (%d messages, then Diag/NM)" % len(order))
        t["merged"] = merged
        r["conflicts"] = _join(_blocks(merged))[1]
    if order is not None and VNIM_C in texts and texts[VNIM_C]["edited"] is not None:
        t, r = texts[VNIM_C], by_name[VNIM_C]
        merged, rebuilt = rebuild_message_arrays(t["merged"], len(order))
        if rebuilt:
            r["rules_applied"].append("per-message arrays %s rebuilt for %d messages" % (", ".join(rebuilt), len(order)))
        t["merged"] = merged
        r["conflicts"] = _join(_blocks(merged))[1]

    for r in results:
        if r["file"] not in texts:
            continue
        t = texts[r["file"]]
        if t["edited"] is not None:
            r["checks"] += duplicate_definitions(t["merged"], t["new"], t["edited"])
            r["checks"] += ["%s is defined in the new generation but missing in the result" % k
                            for k in missing_definitions(t["merged"], t["new"], t["base"], t["edited"])]
        if order is not None and not r["conflicts"]:
            r["checks"] += table_problems(t["merged"], r["file"], order)
        if r["conflicts"]:
            r["status"] = "CONFLICTS"
        elif not r["status"]:
            r["status"] = "merged" if r["edits"] else "no hand edits"
        with open(Path(out_dir) / r["file"], "w", encoding="latin-1", newline=t["eol"]) as fh:
            fh.write(t["merged"])
    return results


def needs_attention(results):
    return [r for r in results if r["conflicts"] or r["origin"] or r["checks"]
            or r["status"] in ("new file taken", "skipped")]


def report(results, base_dir, edited_root, new_dir, out_dir):
    lines = ["# Hand edits re-applied", "",
             "Previous generation: `%s`  " % base_dir, "Your edited files: `%s`  " % edited_root,
             "New generation: `%s`  " % new_dir, "Result: `%s`" % out_dir, "",
             "| File | Result | Your edit regions | Conflicts | Note |", "|---|---|---|---|---|"]
    for r in results:
        note = "; ".join(x for x in [r.get("detail", "")] + r["rules_applied"] if x)
        lines.append("| %s | %s | %d | %d | %s |" % (r["file"], r["status"], r["edits"], len(r["conflicts"]), note))
    lines += ["", "White-space-only conflicts keep your formatting; header-stamp-only conflicts keep the new "
              "Date / By / Traceability lines; can_rxrule.cfg and nw_can_dll.h come from the new generation.", "",
              "## Manual Action Required", ""]
    if not needs_attention(results):
        lines += ["None. Review the result (your edits were applied without conflicts and every check passed), then "
                  "copy the files into your workspace.", ""]
    n = 0
    for r in results:
        for problem in r["checks"]:
            n += 1
            lines += ["### %d. %s: check failed" % (n, r["file"]), "",
                      "- **File and location:** %s" % os.path.join(out_dir, r["file"]),
                      "- **Current value:** %s" % problem,
                      "- **Required change:** correct the file so the check passes",
                      "- **Why not automatic:** the merge result does not match the structure of the generated file",
                      "- **Dependencies:** the other files of this generation",
                      "- **Steps:** compare the place with the new generation and with your previous file",
                      "- **Verification:** run Re-apply edits again on the corrected inputs, or build the project", ""]
        if r["origin"]:
            n += 1
            mine, theirs = r["origin"]
            lines += ["### %d. %s: REVIEW, your file comes from another generation" % (n, r["file"]), "",
                      "- **File and location:** %s (header Traceability)" % r["edited_path"],
                      "- **Current value:** your file was generated from `%s`; the previous generation from `%s`" % (mine, theirs),
                      "- **Required change:** confirm that the %d region(s) where your file differs from the previous "
                      "generation are edits you want to keep; differences that only come from the older generation should "
                      "be dropped" % r["edits"],
                      "- **Why not automatic:** an old generated line cannot be told apart from a hand edit",
                      "- **Dependencies:** the other files of the same generation",
                      "- **Steps:** compare your file with the generated file of `%s` and remove differences you do not "
                      "want from %s" % (mine, os.path.join(out_dir, r["file"])),
                      "- **Verification:** tools/compare_reference.py --generated <result> --reference <workspace> shows "
                      "only intended differences", ""]
        if r["status"] in ("new file taken", "skipped") and not r["conflicts"]:
            n += 1
            lines += ["### %d. %s: %s" % (n, r["file"], r["status"]), "",
                      "- **File and location:** %s (whole file)" % r["file"],
                      "- **Current value:** %s" % r["detail"],
                      "- **Required change:** if you edited this file by hand, apply those edits to %s again"
                      % os.path.join(out_dir, r["file"]),
                      "- **Why not automatic:** without the previous generated file and your edited file no edit can be derived",
                      "- **Dependencies:** none known",
                      "- **Steps:** choose folders that contain the file, or edit by hand",
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
                      "- **Dependencies:** other conflicts of the same message or signal (often in nw_il_par.h/.c and "
                      "nw_vnim_app_signals_par.h/.c together)",
                      "- **Steps:** open the file at line %d, edit the block between `<<<<<<< %s` and `>>>>>>> %s`, delete "
                      "the marker lines" % (line, LABELS[0], LABELS[2]),
                      "- **Verification:** no line starting with `<<<<<<<`, `|||||||`, `=======` or `>>>>>>>` remains; the "
                      "project builds", ""]
    return "\n".join(lines)
