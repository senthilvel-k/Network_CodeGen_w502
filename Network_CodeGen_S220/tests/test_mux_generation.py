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


FLAG = re.compile(r"#define (ILSet_\w+)_DataChanged\(\) +(\(il_Rx_DataChanged_Flag\[[^\]]+\].*)")


def flags(text):
    return dict(FLAG.findall(text))


def test_flag_area_and_counts(both):
    h, plain = both[True]["nw_il_par.h"], both[False]["nw_il_par.h"]
    assert "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (162 + 17) " in h
    assert "#define IL_MUX_MSG_OFFSET_ID   162 " in h and "IL_MUX_MSG_OFFSET_ID" not in plain
    f, p = flags(h), flags(plain)
    assert {k: v for k, v in f.items() if k in p} == p                 # every regular flag unchanged
    assert f["ILSet_BMS_CELLTEMP1"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 0] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLVOLTAGE1"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 4] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLTEMP_INDEX"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 16] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLVOLTAGE_INDEX"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 16] |= (CAN_UINT8) (0x2))")


def test_macros_and_prototypes_after_the_regular_ones(both):
    h = both[True]["nw_il_par.h"]
    assert "#define ILRxPut_BMS_CELLTEMP_INDEX(data)    BMS19_100.bms19_100.BMS_CELLTEMP_INDEX= data" in h
    assert "#define ILRxPut_BMS_CELLVOLTAGE_INDEX(data)    " \
           "BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX= data" in h
    put = h.index("#define ILRxPut_BMS_CELLTEMP_INDEX(data)")
    assert h.index("#define ILRxPut_TIME_TO_CHARGE(data)") < put < h.index("Receive Signal Rx Get Macros")
    assert "#define IlRxGetBMS_CELLTEMP_INDEX() \t\tBMS19_100.bms19_100.BMS_CELLTEMP_INDEX" in h
    assert "void ILRxPut_BMS_CELLVOLTAGE1(CAN_UINT16 data);" in h and "CAN_UINT16 IlRxGetBMS_CELLTEMP1(void);" in h
    assert h.index("void ILRxPut_RESERVED_WLC(") < h.index("void ILRxPut_BMS_CELLTEMP1(CAN_UINT16 data);")
    assert h.count("void ILRxPut_BMS_CELLTEMP1(") == 1 and h.count("#define ILSet_BMS_CELLTEMP1_DataChanged") == 1
    assert "VNIM_RX_BMS_CELLTEMP1" not in h and "VNIM_RX_BMS_CELLTEMP_INDEX" not in h


def test_receive_code_after_the_regular_code(both):
    c = both[True]["nw_il_par.c"]
    assert c.index("WLC_NSM_buf WLC_NSM;") < c.index("CAN_UINT16 BMS19_100__CELLTEMP1;")
    assert c.index("void ILRxPut_RESERVED_WLC(") < c.index("void ILRxPut_BMS_CELLTEMP1(CAN_UINT16 data)")
    assert c.index("void IlRxGetRESERVED_WLC(") < c.index("CAN_UINT16 IlRxGetBMS_CELLTEMP1(void)")
    assert c.index("void WLC_NSM_PreCopy (void)") < c.index("void BMS19_100_PreCopy (void)") \
        < c.index("void BMS20_100_PreCopy (void)")
    for fn in ("void BMS19_100_PreCopy", "void ILRxPut_BMS_CELLTEMP1(", "CAN_UINT16 IlRxGetBMS_CELLVOLTAGE96("):
        assert c.count(fn) == 1, fn
    assert "vin_index_data" in c and "bms_celltemp_index_data" not in c


def _function(text, head):
    start = text.index(head)
    return text[start:text.index("\n}\n", start)]


def test_vnim_lists_follow_the_hand_code_order(both):
    v = both[True]["nw_vnim_app_signals_par.c"]
    ind = _function(v, "void VnimIlRx_BMS19_100_MsgIndication( void )")
    sets = re.findall(r"ILSet_(\w+)_DataChanged", ind)
    assert sets[0] == "BMS_CELLTEMP1" and sets[-1] == "BMS_CELLTEMP_INDEX"
    gets = re.findall(r"if\(ILGet_(\w+)_DataChanged", ind)
    assert gets[0] == "BMS_CELLTEMP_INDEX" and gets[1] == "BMS_CELLTEMP1" and len(gets) == 33
    assert "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();" in _function(v, "void VnimIlRx_BMS20_100_Timeout( void )")
    case = v[v.index("       case VNIM_BMS20_100_MSGID:\n         ILRxPut_BMS_CELLVOLTAGE1"):]
    case = case[:case.index("break;")]
    assert "NM_MSG_MISSING(VNIM_BMS20_100_MSGID);" in case and "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();" in case
    assert case.index("ILRxPut_BMS_CELLVOLTAGE96(") < case.index("ILRxPut_BMS_CELLVOLTAGE_INDEX(")


def test_init_list_appended_multiplexor_first(both):
    v = both[True]["nw_vnim_app_signals_par.c"]
    i = v.index("   ILRxPut_BMS_CELLTEMP_INDEX(0x0u);")
    assert v.index("ILRxPut_RESERVED_WLC(&Onfail_value_zero[0]);") < i < v.index("   ILRxPut_BMS_CELLTEMP1(0x1F4u);") \
        < v.index("   ILRxPut_BMS_CELLVOLTAGE_INDEX(0x0u);") < v.index("   ILRxPut_BMS_CELLVOLTAGE1(0x0u);")


def test_no_per_signal_application_macros(both):
    assert "VNIM_IS_BMS_CELLTEMP1_MISSING" not in both[True]["nw_vnim_app_signals_par.h"]
    assert "VNIM_IS_BMS_CELLTEMP1_MISSING" not in both[True]["nw_vnim_app_signals_par.c"]
