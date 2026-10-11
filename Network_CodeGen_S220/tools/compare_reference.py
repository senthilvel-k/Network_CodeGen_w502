"""Compare generated CoGeNT files with a manually modified reference workspace.

Usage (from Network_CodeGen_S220):
  .venv/Scripts/python.exe tools/compare_reference.py --generated CODE_GEN --reference <workspace>
        [--plan CODE_GEN/fifo_plan.json] [--report report.md] [--patch-dir patches]

For every generated file the workspace file with the same name is located (it must be unique).
can_rxrule.cfg and nw_can_dll.h are also compared structurally (rules / dispatch entries). With
--plan, the hand-written nw_can_dll.c of the workspace is checked against the merged ID blocks.
The reference workspace is only read. Exit code 0 when every compared file matches after
normalization and no dispatch-code finding exists, else 1."""
import argparse
import difflib
import json
import os
import re
import sys
from pathlib import Path

GENERATED_FILES = ["can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
                   "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
                   "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h"]


def _text(path):
    return Path(path).read_text(encoding="latin-1").replace("\r", "")


def parse_rx_rules(path):
    """[(id, mask, ptr0, ptr1)] in rule-table order."""
    t = _text(path)
    rules = {}
    for kind in ("ID", "MASK", "PTR0", "PTR1"):
        for n, v in re.findall(r"#define\s+CAN0_RX_RULE(\d+)_%s\s+\(CAN_UINT32\)\s*(0x[0-9a-fA-F]+)" % kind, t):
            rules.setdefault(int(n), {})[kind] = int(v, 16)
    order = [int(n) for n in re.findall(r"\{CAN0_RX_RULE(\d+)_ID,", t)]
    return [(rules[n]["ID"], rules[n]["MASK"], rules[n]["PTR0"], rules[n]["PTR1"]) for n in order]


def parse_dispatch_vectors(path):
    """{vector: [(id, dlc, vnim handle, layer)]} from the dllhscanRxIdsVector tables."""
    t = _text(path)
    out = {}
    for m in re.finditer(r"dllhscanRxIdsVector(\d)\[ \] =\s*\{(.*?)\n\};", t, re.S):
        entries = re.findall(r"\{\s*(0x[0-9a-fA-F]+),.*?(?:(\d+)u,)?\s*#endif\s*(\w+),\s*(\w+)\s*\}", m.group(2), re.S)
        out[int(m.group(1))] = [(int(i, 16), d, h, layer) for i, d, h, layer in entries]
    return out


def normalized_lines(path):
    """Text without the revision-notes footer, whitespace collapsed, blank lines dropped."""
    text = _text(path)
    cut = text.find("R E V I S I O N")
    if cut != -1:
        text = text[:text.rfind("/*", 0, cut)]
    return [re.sub(r"\s+", " ", line).strip() for line in text.split("\n") if line.strip()]


# ---- nw_can_dll.c dispatch code ------------------------------------------------------------------
def _blocks(groups_or_plan):
    blocks = []
    for g in groups_or_plan:
        if isinstance(g, dict):   # fifo_plan.json entry
            blocks.append((int(g["base"], 16), int(g["mask"], 16),
                           {int(m["id"], 16): m["vnim_handle"] for m in g["members"]}))
        else:                     # cogent_fifo.MergedGroup
            blocks.append((g.base, g.block.mask,
                           {int(m["id"]): "VNIM_%s_MESSAGE" % m["Msg_name"].upper() for m in g.members}))
    return blocks


def _region(text, start):
    """Text of the brace block that starts after position start."""
    i = text.find("{", start)
    depth = 0
    for j in range(i, len(text)):
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        if depth == 0:
            return text[i:j + 1]
    return text[i:]


def check_dispatch_code(nw_can_dll_c, groups_or_plan):
    """Findings (strings) where DllDispatchReceivedMessage does not map every merged ID to its handle."""
    text = re.sub(r"//[^\n]*", "", _text(nw_can_dll_c))
    findings = []
    for base, mask, expected in _blocks(groups_or_plan):
        cond = re.search(r"\(\s*\(\s*pRmd->Identifier\.I32\s*&\s*0x%Xu?\s*\)\s*==\s*0x%Xu?\s*\)" % (mask, base), text, re.I)
        if not cond:
            findings.append("0x%03X/0x%03X: no dispatch branch for this merged block in %s (expected a check "
                            "'(pRmd->Identifier.I32 & 0x%03Xu) == 0x%03Xu')" % (base, mask, nw_can_dll_c, mask, base))
            continue
        region = _region(text, cond.end())
        mapped = {}
        for case_id, if_id, handle in re.findall(
                r"(?:case\s*(0x[0-9A-Fa-f]+)u?\s*:|Identifier\.I32\s*==\s*(0x[0-9A-Fa-f]+)u?\s*\))\s*canFrameHandle\s*=\s*(\w+)", region):
            mapped[int(case_id or if_id, 16)] = handle
        default = re.search(r"\belse\s+canFrameHandle\s*=\s*(\w+)", region)
        unmapped = [i for i in sorted(expected) if i not in mapped]
        if default and len(unmapped) == 1:
            mapped[unmapped[0]] = default.group(1)
            unmapped = []
        for i in unmapped:
            findings.append("0x%03X/0x%03X: ID 0x%03X (%s) is not mapped in the dispatch branch" % (base, mask, i, expected[i]))
        for i, handle in sorted(mapped.items()):
            if i in expected and handle != expected[i]:
                findings.append("0x%03X/0x%03X: ID 0x%03X is mapped to %s, expected %s" % (base, mask, i, handle, expected[i]))
            elif i not in expected:
                findings.append("0x%03X/0x%03X: ID 0x%03X is mapped to %s but is not received in this configuration"
                                % (base, mask, i, handle))
    return findings


# ---- report ----------------------------------------------------------------------------------------
def compare_file(gen, ref, patch_dir=None):
    a, b = _text(gen).split("\n"), _text(ref).split("\n")
    result = {"file": gen.name, "reference": str(ref), "exact": a == b,
              "normalized_equal": normalized_lines(gen) == normalized_lines(ref)}
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    result["hunks"] = [{"op": t, "generated_lines": "%d-%d" % (i1 + 1, i2), "reference_lines": "%d-%d" % (j1 + 1, j2),
                        "generated": a[i1:i2][:3], "reference": b[j1:j2][:3]} for t, i1, i2, j1, j2 in hunks]
    result["changed_lines"] = sum((i2 - i1) + (j2 - j1) for _, i1, i2, j1, j2 in hunks)
    if gen.name == "can_rxrule.cfg":
        result["rules_equal"] = parse_rx_rules(gen) == parse_rx_rules(ref)
    if gen.name == "nw_can_dll.h":
        result["dispatch_equal"] = parse_dispatch_vectors(gen) == parse_dispatch_vectors(ref)
    if patch_dir and hunks:
        os.makedirs(patch_dir, exist_ok=True)
        with open(os.path.join(patch_dir, gen.name + ".patch"), "w", encoding="latin-1", newline="\n") as fh:
            fh.writelines(l + "\n" for l in difflib.unified_diff(a, b, "generated/" + gen.name, "reference/" + gen.name, lineterm=""))
    return result


def find_reference(workspace, name):
    hits = [p for p in Path(workspace).rglob(name) if p.is_file()]
    return hits[0] if len(hits) == 1 else None


def build_report(generated, reference, plan_path=None, patch_dir=None):
    rows, details, ok = [], [], True
    for name in GENERATED_FILES:
        gen = Path(generated) / name
        if not gen.is_file():
            continue
        ref = find_reference(reference, name)
        if ref is None:
            rows.append("| %s | - | not found (or not unique) in reference | - |" % name)
            ok = False
            continue
        r = compare_file(gen, ref, patch_dir)
        status = "identical" if r["exact"] else "equal after normalization" if r["normalized_equal"] else "DIFFERENT"
        extra = []
        if "rules_equal" in r:
            extra.append("rules %s" % ("identical" if r["rules_equal"] else "DIFFERENT"))
        if "dispatch_equal" in r:
            extra.append("dispatch entries %s" % ("identical" if r["dispatch_equal"] else "DIFFERENT"))
        ok &= r["normalized_equal"] or r.get("rules_equal", False) or r.get("dispatch_equal", False)
        rows.append("| %s | %s | %s | %d |" % (name, os.path.relpath(r["reference"], reference), status + ("; " + ", ".join(extra) if extra else ""), r["changed_lines"]))
        if not r["normalized_equal"]:
            details.append("### %s\n\n%d differing regions (first 10):\n" % (name, len(r["hunks"])))
            for h in r["hunks"][:10]:
                details.append("- %s generated %s / reference %s\n  - generated: `%s`\n  - reference: `%s`"
                               % (h["op"], h["generated_lines"], h["reference_lines"],
                                  " / ".join(x.strip()[:90] for x in h["generated"]) or "(none)",
                                  " / ".join(x.strip()[:90] for x in h["reference"]) or "(none)"))
            details.append("")
    lines = ["# Generated vs reference comparison", "", "Generated: `%s`  " % generated, "Reference: `%s`" % reference, "",
             "| File | Reference file | Result | Changed lines (raw) |", "|---|---|---|---|"] + rows + [""]
    if plan_path and os.path.exists(plan_path):
        plan = json.load(open(plan_path, encoding="utf-8"))
        dll_c = find_reference(reference, "nw_can_dll.c")
        lines.append("## nw_can_dll.c dispatch code for merged ID blocks\n")
        if dll_c is None:
            lines.append("nw_can_dll.c not found (or not unique) in the reference workspace.\n")
            ok = False
        else:
            findings = check_dispatch_code(dll_c, plan["merged_blocks"])
            lines.append("All merged IDs are mapped correctly.\n" if not findings else "\n".join("- " + f for f in findings) + "\n")
            ok &= not findings
    lines += details
    return "\n".join(lines), ok


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--generated", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--plan")
    p.add_argument("--report")
    p.add_argument("--patch-dir")
    a = p.parse_args(argv)
    report, ok = build_report(a.generated, a.reference, a.plan, a.patch_dir)
    if a.report:
        Path(a.report).write_text(report, encoding="utf-8")
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
