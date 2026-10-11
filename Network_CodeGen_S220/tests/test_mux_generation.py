"""40024 fixture generated with BMS19_100 / BMS20_100 enabled (indexed multiplexed messages)."""
import json
import os
import re
import shutil
import sys

import pytest

from support import CODE_FILES, ROOT, enable_indexed, load_fixture, run_file

sys.path.insert(0, str(ROOT))
FIXTURE = "s2xx_40024_a"
FIFO = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}]}


def _generate(home, enable):
    from cogent_generate import run_code_generation
    fx = load_fixture(FIXTURE)
    shutil.copytree(fx.data_dir, home / "data")
    (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps(FIFO), encoding="utf-8")
    if enable:
        enable_indexed(home, fx.dbc, fx.node)
    run_code_generation(str(fx.dbc), fx.node, "2000-01-01 00:00")
    return {f: run_file(home, f).read_text(encoding="latin-1") for f in CODE_FILES}


@pytest.fixture(scope="module")
def both(tmp_path_factory):
    out = {}
    for enable in (False, True):
        home = tmp_path_factory.mktemp("bms_%s" % enable)
        old = os.getcwd()
        os.chdir(home)
        try:
            out[enable] = _generate(home, enable)
        finally:
            os.chdir(old)
    return out


def lines(text):
    return [re.sub(r"\s+", "", l) for l in text.replace("\r", "").split("\n") if l.strip()]


def test_types_follow_the_legacy_multiplex_type(both):
    h = both[True]["nw_il_msg.h"]
    assert h.index("}VCU5_500_msgType;") < h.index("}BMS_CELLTEMP_INDEX_0_sigType;") \
        < h.index("}BMS19_100_msgType;") < h.index("}BMS_CELLVOLTAGE_INDEX_0_sigType;") \
        < h.index("}BMS20_100_msgType;") < h.index("/* ACC1_500 */")
    assert "BMS_CELLTEMP_DATA_Sigbuf  bms_celltemp_data;" in h
    assert lines("typedef union {\n  CAN_UINT8 msgBuffer[8];\n  BMS_CELLVOLTAGE_INDEX_0_sigType  "
                 "bms_cellvoltage_index_0;") == lines(h[h.index("/* BMS20_100 */"):])[1:4]


def test_disabled_messages_change_nothing(both):
    assert "BMS19_100" not in both[False]["nw_il_msg.h"]
