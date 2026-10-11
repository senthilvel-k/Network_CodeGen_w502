"""Comparison with the manually modified reference workspace (read in place, never copied into git).

COGENT_REFERENCE_WS (default D:/networkgen/dc.app.scl.vehiclecomm) holds the files the user edits
after generation. These tests regenerate with the FIFO configuration that reproduces the manual
receive-rule edits and compare the result with the reference files."""
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

from support import ROOT, load_fixture, run_harness

REFERENCE_WS = Path(os.environ.get("COGENT_REFERENCE_WS", r"D:\networkgen\dc.app.scl.vehiclecomm"))
pytestmark = pytest.mark.skipif(not REFERENCE_WS.is_dir(), reason="INCOMPLETE: reference workspace %s not available" % REFERENCE_WS)

FIXTURE = "s2xx_40024_a"   # the reference IL/VNIM files come from this run (2026-02-26 12:10)
FIFO_CONFIG = {
    "merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
    "additional_rx_messages": ["BMS19_100", "BMS20_100"],
}

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
from cogent_generate import output_relpath  # noqa: E402


def reference(name):
    hits = [p for p in REFERENCE_WS.rglob(name) if p.is_file()]
    assert len(hits) == 1, "expected exactly one %s in %s, found %s" % (name, REFERENCE_WS, hits)
    return hits[0]


def normalized(path):
    """Text without the revision-notes footer, whitespace collapsed, blank lines dropped."""
    text = path.read_text(encoding="latin-1").replace("\r", "")
    cut = text.find("R E V I S I O N")
    if cut != -1:
        text = text[:text.rfind("/*", 0, cut)]
    return [re.sub(r"\s+", " ", line).strip() for line in text.split("\n") if line.strip()]


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    fx = load_fixture(FIXTURE)
    data = tmp_path_factory.mktemp("ref") / "data"
    shutil.copytree(fx.data_dir, data)
    (data / "CanFifoConfiguration.data").write_text(json.dumps(FIFO_CONFIG), encoding="utf-8")
    out = data.parent / "out"
    run_harness(sys.executable, fx, out, "code", data_dir=data)
    return out


def test_receive_rules_match_reference_exactly(generated):
    from compare_reference import parse_rx_rules
    got = parse_rx_rules(generated / "can_rxrule.cfg")
    want = parse_rx_rules(reference("can_rxrule.cfg"))
    assert len(got) == len(want) == 184
    assert got == want


def test_dispatch_vectors_match_reference_exactly(generated):
    from compare_reference import parse_dispatch_vectors
    got = parse_dispatch_vectors(generated / "nw_can_dll.h")
    want = parse_dispatch_vectors(reference("nw_can_dll.h"))
    assert [len(got[v]) for v in (0, 1, 2)] == [64, 64, 56]
    assert got == want


@pytest.mark.parametrize("name", ["can_rxrule.cfg", "nw_can_dll.h"])
def test_fifo_files_match_reference_text_except_revision_notes_and_whitespace(generated, name):
    got, want = normalized(generated / name), normalized(reference(name))
    assert got == want


def _digest(folder):
    return {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob("*") if p.is_file()}


def test_carrying_hand_edits_forward_reproduces_the_reference_except_the_header_stamp(generated, tmp_path):
    """Hybrid workflow: FIFO rules generated + the other hand edits re-applied from the workspace.
    CODE_GEN/DBC_40024 holds the generated files the workspace edits started from."""
    import cogent_carry
    before = _digest(REFERENCE_WS)
    out = tmp_path / "merged"
    results = cogent_carry.carry_forward(ROOT / "CODE_GEN" / "DBC_40024", REFERENCE_WS, generated, out)
    assert _digest(REFERENCE_WS) == before                     # the workspace is only read
    assert [r["file"] for r in results if r["conflicts"]] == []
    # your file shares data-changed flag byte 161 between generated and multiplexed signals: reported, not changed
    assert {r["file"]: r["checks"] for r in results if r["checks"]} == {"nw_il_par.h": [
        "IL_MUX_MSG_OFFSET_ID is 161, but the generated data-changed flags use bytes 0..161: the multiplexed signal "
        "flags share byte 161 with them (the first free byte is 162)"]}
    arrays = re.compile(r"(vnim_msg_byte_position|vnim_msg_bit_mask)\[NUM_VNIM_MESSAGES\]\s*=\s*\n\{\n(.*?)\n\};", re.S)
    stamp = re.compile(r"^(Date|By|Traceability)\s*:")
    for r in results:
        got_text = (out / output_relpath(r["file"])).read_text(encoding="latin-1")
        want_text = reference(r["file"]).read_text(encoding="latin-1").replace("\r", "")
        if r["file"] in cogent_carry.FIFO_FILES:              # generated from the FIFO settings: only your padding differs
            assert normalized(out / output_relpath(r["file"])) == normalized(reference(r["file"])), r["file"]
            continue
        if r["file"] == cogent_carry.VNIM_C:                  # your arrays have 192 entries for 193 messages: rebuilt
            assert [len(re.split(r"[,\s\\]+", body.strip())) for _, body in arrays.findall(got_text)] == [193, 193]
            got_text, want_text = arrays.sub("ARRAY", got_text), arrays.sub("ARRAY", want_text)
        got = [l for l in got_text.split("\n") if not stamp.match(l)]
        want = [l for l in want_text.split("\n") if not stamp.match(l)]
        assert got == want, r["file"]
    # files whose header names an older DBC than CODE_GEN/DBC_40024 are flagged for review
    assert sorted(r["file"] for r in results if r["origin"]) == ["can_rxrule.cfg", "nw_can_dll.h", "nw_nm_par.h"]


def test_reference_dispatch_code_covers_every_merged_message(generated):
    from compare_reference import check_dispatch_code
    import cogent_fifo
    from Dbc_Parser import dbc_parser
    import can_rx_filt_gen
    fx = load_fixture(FIXTURE)
    cfg_data = json.loads((fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    config = cogent_fifo.FifoConfig(merge_blocks=[cogent_fifo.MergeBlock(0x3D0, 0x7F0), cogent_fifo.MergeBlock(0x4F0, 0x7F0)],
                                    additional_rx_messages=["BMS19_100", "BMS20_100"])
    plan = can_rx_filt_gen.plan_rx_rules(dbc_parser(str(fx.dbc), fx.node), cfg_data, config)
    findings = check_dispatch_code(reference("nw_can_dll.c"), plan.groups)
    assert findings == [], findings


LOCAL_41490 = ROOT / "local_reports" / "DBC_41490"


@pytest.mark.skipif(not (LOCAL_41490 / "generated").is_dir(), reason="INCOMPLETE: local 41490 generation not available")
def test_re_applying_the_40024_edits_to_41490_needs_no_manual_conflict_resolution(tmp_path):
    """41490 adds AMP5_2000/AMP6_2000: your BMS19/BMS20 code, REM order and other edits are re-applied;
    the derived values are recomputed and every check passes."""
    import cogent_carry
    before = _digest(REFERENCE_WS)
    out = tmp_path / "merged"
    results = {r["file"]: r for r in cogent_carry.carry_forward(ROOT / "CODE_GEN" / "DBC_40024", REFERENCE_WS,
                                                                 LOCAL_41490 / "generated", out)}
    assert _digest(REFERENCE_WS) == before
    assert {f: len(r["conflicts"]) for f, r in results.items() if r["conflicts"]} == {}
    assert {f: r["checks"] for f, r in results.items() if r["checks"]} == {}
    il_par = (out / output_relpath("nw_il_par.h")).read_text(encoding="latin-1")
    assert re.search(r"^#define IL_RX_NUM_MESSAGES\s+195\s*$", il_par, re.M)
    assert re.search(r"^#define IL_MUX_MSG_OFFSET_ID\s+163\s*$", il_par, re.M)
    assert re.search(r"^#define IL_NUM_OF_RX_DATA_CHANGED_FLAG\s+\(163 \+ 17\)\s*$", il_par, re.M)
    handles = re.findall(r"^#define VNIM_(\w+?)_MESSAGE\s+(\d+)\s*$", il_par, re.M)
    assert len(handles) == 214 and handles[195] == ("IL_RX", "195") and handles[-1] == ("WLC_ACTIVE", "213")
    names = [n for n, _ in handles]
    assert names.index("BMS19_100") == names.index("BMS18_50") + 1 and ("AMP5_2000", "2") in handles
