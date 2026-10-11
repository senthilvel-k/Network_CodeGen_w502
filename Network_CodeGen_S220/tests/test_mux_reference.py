"""Generated BMS19_100 / BMS20_100 code against the S2XX workspace (read in place; skipped without it).

Every line that names an indexed message, one of its signals or the multiplex flag area is compared
(white space removed, counted). The differences must be exactly the intended ones of the spec
(docs/superpowers/specs/2026-10-11-multiplex-generation-design.md, section 9); whole functions are
compared too."""
import os
import re
from collections import Counter
from pathlib import Path

import pytest

from test_mux_generation import both  # noqa: F401  (module fixture: 40024 with/without BMS19/BMS20)

WS = Path(os.environ.get("COGENT_REFERENCE_WS", r"D:\networkgen\dc.app.scl.vehiclecomm"))
pytestmark = pytest.mark.skipif(not WS.is_dir(), reason="INCOMPLETE: reference workspace not available")
NAMES = re.compile(r"BMS19_100|BMS20_100|BMS_CELLTEMP|BMS_CELLVOLTAGE|IL_MUX_MSG_OFFSET_ID")
FILES = ["nw_il_msg.h", "nw_il_par.h", "nw_il_par.c", "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h",
         "vnim.msg.resource", "vnim.txrx.resource", "nw_host_mgr_txrx.resource"]
V2632 = r"BMS20_100\.bms20_100\.bms_cellvoltage_index_[45]\.BMS_CELLVOLTAGE(26|32)_1=\(CAN_UINT8\)\(\(\(data\)>>%d\)&0xff\);"
# file -> [(kind, line pattern (white space removed), count, spec section 9 item)]
INTENDED = {
    "nw_il_par.h": [
        ("extra", r"#defineIL_MUX_MSG_OFFSET_ID162", 1, "1 flag area after the regular flags"),
        ("missing", r"#defineIL_MUX_MSG_OFFSET_ID161", 1, "1"),
        ("extra", r"#defineILClr_BMS_CELLVOLTAGE78_DataChanged\(\).*~0x20u\)\)\)", 1, "9 hand code lacks the u"),
        ("missing", r"#defineILClr_BMS_CELLVOLTAGE78_DataChanged\(\).*~0x20\)\)\)", 1, "9"),
    ],
    "nw_il_par.c": [
        ("extra", V2632 % 2, 2, "5 the upper bits start after 2 bits"),
        ("missing", V2632 % 3, 2, "5"),
        ("extra", r"ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged\(\);", 1, "2 BMS20 PreCopy"),
        ("missing", r"ILSet_BMS_CELLTEMP_INDEX_DataChanged\(\);", 1, "2"),
    ],
    "nw_vnim_app_signals_par.c": [
        ("extra", r"ILRxPut_BMS_CELLVOLTAGE\d+\(0x0u\);", 192, "4 init list, 9 format"),
        ("missing", r"ILRxPut_BMS_CELLVOLTAGE\d+\(0x00\);", 96, "9"),
        ("extra", r"ILRxPut_BMS_CELLVOLTAGE_INDEX\(0x0u\);", 2, "4, 9"),
        ("missing", r"ILRxPut_BMS_CELLVOLTAGE_INDEX\(0x00\);", 2, "3 set twice, 9"),
        ("extra", r"ILRxPut_BMS_CELLTEMP\d+\(0x1f4u\);", 64, "9 init value as the signals page writes it"),
        ("missing", r"ILRxPut_BMS_CELLTEMP\d+\(0x1F4u\);", 64, "9"),
        ("extra", r"ILRxPut_BMS_CELLTEMP_INDEX\(0x0u\);", 1, "9"),
        ("missing", r"ILRxPut_BMS_CELLTEMP_INDEX\(0x00\);", 1, "9"),
        ("extra", r"ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged\(\);", 2, "3, 7 all-frames case"),
        ("extra", r"NM_MSG_MISSING\(VNIM_BMS20_100_MSGID\);", 1, "3"),
        ("missing", r"NM_MSG_MISSING\(VNIM_BMS19_100_MSGID\);", 1, "3"),
        ("extra", r"Vnim_BMS_Timeout_flag\|=\(unsigned32\)VNIM_BMS(19|20)_100_MSGID_BIT;", 2, "6 message loss"),
        ("extra", r"caseVNIM_BMS(19|20)_100_MSGID:", 2, "6"),
        ("extra", r"if\(\(BMS_node_cfg_st==CF_OPT_BMS_PRSNT\)&&\(BMS(19|20)_100_FC_cfg_st==TRUE\)\)", 2, "6"),
        ("extra", r"vnim_dtc_log\(NM_BMS_NODE,VNIM_MSG_LOSS,VNIM_BMS(19|20)_100_MSGID\);", 2, "6"),
    ],
}


def ws_file(name):
    hits = [p for p in WS.rglob(name) if p.is_file()]
    assert len(hits) == 1, hits
    return hits[0].read_text(encoding="latin-1")


def bms_lines(text):
    out = Counter()
    for line in text.replace("\r", "").split("\n"):
        if NAMES.search(line):
            out[re.sub(r"\s+", "", line)] += 1
    return out


def norm_lines(text):
    return [re.sub(r"\s+", "", l) for l in text.replace("\r", "").split("\n") if l.strip()]


def functions(text, pattern):
    """C functions whose header matches pattern: header line .. first line that is exactly '}'."""
    lines = text.replace("\r", "").split("\n")
    out = {}
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            j = i + 1
            while lines[j].rstrip() != "}":
                j += 1
            out[re.sub(r"\s+", "", line)] = norm_lines("\n".join(lines[i:j + 1]))
    return out


@pytest.mark.parametrize("name", FILES)
def test_bms_lines_match_the_workspace(both, name):
    gen, ws = bms_lines(both[True][name]), bms_lines(ws_file(name))
    rules = INTENDED.get(name, [])
    found, unexplained = Counter(), []
    for kind, diff in (("extra", gen - ws), ("missing", ws - gen)):
        for line, n in diff.items():
            rule = next((r for r in rules if r[0] == kind and re.fullmatch(r[1], line)), None)
            if rule is None:
                unexplained.append("%s x%d %s" % (kind, n, line))
            else:
                found[rule] += n
    assert not unexplained, "\n".join(sorted(unexplained))
    assert {r: found[r] for r in rules} == {r: r[2] for r in rules}


def test_flag_count(both):
    assert "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (161 + 17)" in ws_file("nw_il_par.h")
    assert "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (162 + 17)" in both[True]["nw_il_par.h"]


@pytest.mark.parametrize("name, pattern, differing", [
    ("nw_il_par.c", r"^void (BMS19_100|BMS20_100)_PreCopy", {"voidBMS20_100_PreCopy(void)"}),
    ("nw_il_par.c", r"^void ILRxPut_BMS_CELL",
     {"voidILRxPut_BMS_CELLVOLTAGE26(CAN_UINT16data)", "voidILRxPut_BMS_CELLVOLTAGE32(CAN_UINT16data)"}),
    ("nw_il_par.c", r"^CAN_UINT16 IlRxGetBMS_CELL", set()),
    ("nw_vnim_app_signals_par.c", r"^void VnimIlRx_(BMS19_100|BMS20_100)_(MsgIndication|Timeout)", set()),
])
def test_bms_functions_match_the_workspace(both, name, pattern, differing):
    gen, ws = functions(both[True][name], pattern), functions(ws_file(name), pattern)
    assert sorted(gen) == sorted(ws)
    assert {f for f in gen if gen[f] != ws[f]} == differing


def test_bms_types_match_the_workspace(both):
    def block(text):
        lines = norm_lines(text)
        return lines[lines.index("}VCU5_500_msgType;") + 1:lines.index("}BMS20_100_msgType;") + 1]
    assert block(both[True]["nw_il_msg.h"]) == block(ws_file("nw_il_msg.h"))
