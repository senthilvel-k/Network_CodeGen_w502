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
    import carry_forward
    before = _digest(REFERENCE_WS)
    out = tmp_path / "merged"
    results = carry_forward.carry_forward(ROOT / "CODE_GEN" / "DBC_40024", REFERENCE_WS, generated, out)
    assert _digest(REFERENCE_WS) == before                     # the workspace is only read
    assert [r["file"] for r in results if r["conflicts"]] == []
    stamp = re.compile(r"^(Date|By|Traceability)\s*:")
    for r in results:
        got = [l for l in (out / r["file"]).read_text(encoding="latin-1").split("\n") if not stamp.match(l)]
        want = [l for l in reference(r["file"]).read_text(encoding="latin-1").replace("\r", "").split("\n")
                if not stamp.match(l)]
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
