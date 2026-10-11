"""cogent_mux layout model on synthetic messages in the parser's format (Dbc_Parser)."""
import pytest

from cogent_mux import Field, OutOfScope, classify, flag_area, layout, layouts


def mes(name, signals, dlc=8, direction="rx"):
    """signals: (name, mul, start, length[, order]) with mul 'M', 'm<N>' or None (plain)."""
    sig_list = {}
    for s in signals:
        sname, mul, start, length = s[:4]
        d = {"Len": str(length), "Order": s[4] if len(s) > 4 else "Intel", "Endbit": str(start)}
        if mul == "M":
            d["Mul_order"] = "root"
        elif mul:
            d["Mul_order"] = mul.lstrip("m")
        sig_list[sname] = d
    multiplexed = any(s[1] for s in signals)
    return {"Msg_name": name, "DLC": str(dlc), "Multiplex": "YES" if multiplexed else "NO", "DIR": direction,
            "Sig_List": sig_list, "id": "1000"}


# BMS19-like: 8-bit multiplexor in byte 0, 16-bit temperatures from bit 16, index 2 shorter
TEMPS = mes("BMS19_100", [("BMS_CELLTEMP_INDEX", "M", 0, 8)] +
            [("BMS_CELLTEMP%d" % (3 * i + k + 1), "m%d" % i, 16 + 16 * k, 16) for i in range(2) for k in range(3)] +
            [("BMS_CELLTEMP7", "m2", 16, 16), ("BMS_CELLTEMP8", "m2", 32, 16)])
# BMS20-like: 4-bit multiplexor, 10-bit voltages from bit 4
VOLTS = mes("BMS20_100", [("BMS_CELLVOLTAGE_INDEX", "M", 0, 4)] +
            [("BMS_CELLVOLTAGE%d" % (6 * i + k + 1), "m%d" % i, 4 + 10 * k, 10) for i in range(2) for k in range(6)])
VCU5 = mes("VCU5_500", [("VIN_INDEX", "M", 56, 2), ("VIN_DATA_0", "m0", 0, 56), ("VIN_DATA_1", "m1", 0, 56),
                        ("VIN_DATA_2", "m2", 0, 24)])


def test_classification():
    assert classify(VCU5) == "legacy"
    assert classify(TEMPS) == "indexed" and classify(VOLTS) == "indexed"
    assert classify(mes("PLAIN_10", [("A", None, 0, 8)])) == "regular"


def test_data_union_layout_of_bms19():
    lay = layout(TEMPS)
    assert lay.kind == "data" and lay.region == (2, 7) and lay.group == "BMS_CELLTEMP_DATA"
    assert lay.outer == [Field("BMS_CELLTEMP_INDEX", 8), Field("unused1", 8), None]
    assert lay.structs[0] == [Field("BMS_CELLTEMP1_0", 8), Field("BMS_CELLTEMP1_1", 8), Field("BMS_CELLTEMP2_0", 8),
                              Field("BMS_CELLTEMP2_1", 8), Field("BMS_CELLTEMP3_0", 8), Field("BMS_CELLTEMP3_1", 8)]
    assert lay.structs[2] == [Field("BMS_CELLTEMP7_0", 8), Field("BMS_CELLTEMP7_1", 8), Field("BMS_CELLTEMP8_0", 8),
                              Field("BMS_CELLTEMP8_1", 8)]                       # ends at its last used byte
    t1 = lay.signals[0]
    assert (t1.name, t1.path, t1.ctype, t1.shadow) == \
        ("BMS_CELLTEMP1", "bms19_100.bms_celltemp_data.bms_celltemp_index_0", "CAN_UINT16", "BMS19_100__CELLTEMP1")
    assert [s.name for s in lay.signals][-1] == "BMS_CELLTEMP_INDEX"
    assert lay.multiplexor.path == "bms19_100" and lay.multiplexor.one_field


def test_frame_union_layout_of_bms20():
    lay = layout(VOLTS)
    assert lay.kind == "frame" and lay.region is None
    assert lay.structs[0][:4] == [Field("BMS_CELLVOLTAGE_INDEX", 4), Field("BMS_CELLVOLTAGE1_0", 4),
                                  Field("BMS_CELLVOLTAGE1_1", 6), Field("BMS_CELLVOLTAGE2_0", 2)]
    v1 = lay.signals[0]
    assert (v1.parts, v1.widths, v1.path) == (["BMS_CELLVOLTAGE1_0", "BMS_CELLVOLTAGE1_1"], [4, 6],
                                              "bms20_100.bms_cellvoltage_index_0")
    assert lay.multiplexor.path == "bms20_100.bms_cellvoltage_index_0"


def test_signal_order_gaps_and_plain_signal():
    m = mes("GAP_100", [("SEL", "M", 0, 8), ("B", "m3", 16, 8), ("A", "m0", 24, 8), ("CRC", None, 56, 8)])
    lay = layout(m)
    assert [s.name for s in lay.signals] == ["A", "B", "CRC", "SEL"]          # (index, start), plain, mux
    assert lay.indexes == [0, 3] and sorted(lay.structs) == [0, 3]
    assert lay.kind == "data" and lay.region == (2, 3)
    assert lay.outer == [Field("SEL", 8), Field("unused1", 8), None, Field("unused4", 8), Field("unused5", 8),
                         Field("unused6", 8), Field("CRC", 8)]
    assert lay.structs[3] == [Field("B", 8)] and lay.structs[0] == [Field("unused2", 8), Field("A", 8)]


def test_frame_union_index_ends_at_its_last_byte():
    m = mes("SHORT_100", [("SEL", "M", 0, 4), ("A", "m0", 4, 12), ("B", "m1", 4, 4)], dlc=8)
    lay = layout(m)
    assert lay.kind == "frame"
    assert lay.structs[1] == [Field("SEL", 4), Field("B", 4)]


@pytest.mark.parametrize("bad, problem", [
    (mes("MOTO_100", [("S", "M", 0, 8), ("X", "m0", 23, 16, "Motorola")]), "Motorola"),
    (mes("LONG_100", [("S", "M", 0, 8), ("X", "m0", 8, 40)]), "longer than 32 bits"),
    (mes("NOMUX_100", [("X", "m0", 8, 8), ("Y", "m1", 8, 8)]), "no multiplexor"),
    (mes("TX_100", [("S", "M", 0, 8), ("X", "m0", 8, 16)], direction="tx"), "transmitted"),
    (mes("FD_100", [("S", "M", 0, 8), ("X", "m0", 8, 16)], dlc=64), "DLC"),
    (mes("OVER_100", [("S", "M", 0, 8), ("X", "m0", 4, 8)]), "overlaps"),
])
def test_out_of_scope_messages_are_named(bad, problem):
    with pytest.raises(OutOfScope) as exc:
        classify(bad)
    assert problem in exc.value.problem and exc.value.msg_name == bad["Msg_name"]


def test_extended_multiplexing_is_out_of_scope():
    m = mes("EXT_100", [("S", "M", 0, 8), ("X", "m0", 8, 8)])
    m["Sig_List"]["X"]["Mul_order"] = "1M"
    with pytest.raises(OutOfScope) as exc:
        classify(m)
    assert "extended multiplexing" in exc.value.problem


def test_layouts_only_for_enabled_receive_messages():
    cfg = {"BMS19_100_rx_enable": "on", "BMS19_100_msg_type_no_of_events": "Appl",
           "BMS20_100_rx_enable": "", "BMS20_100_msg_type_no_of_events": "Appl",
           "VCU5_500_rx_enable": "on", "VCU5_500_msg_type_no_of_events": "Appl"}
    assert list(layouts([VOLTS, TEMPS, VCU5], cfg)) == ["BMS19_100"]


def test_flag_area_order_multiplexors_last():
    lays = {"BMS19_100": layout(TEMPS), "BMS20_100": layout(VOLTS)}
    area = flag_area(lays)
    assert area[0] == ("BMS_CELLTEMP1", 0, 0x1) and area[7] == ("BMS_CELLTEMP8", 0, 0x80)
    assert area[8] == ("BMS_CELLVOLTAGE1", 1, 0x1)
    assert area[-2:] == [("BMS_CELLTEMP_INDEX", 2, 0x10), ("BMS_CELLVOLTAGE_INDEX", 2, 0x20)]


def test_types_text_of_bms19():
    from cogent_mux import types
    text = types(layout(TEMPS))
    assert "typedef struct {\n  CAN_UINT8 BMS_CELLTEMP1_0:8;" in text
    assert "}BMS_CELLTEMP_INDEX_0_sigType;" in text
    assert "typedef union \n{\n   CAN_UINT8          sig_buffer[6];\n   BMS_CELLTEMP_INDEX_0_sigType  " \
           "bms_celltemp_index_0;" in text
    assert "/* BMS19_100 */\ntypedef struct {\n  CAN_UINT8 BMS_CELLTEMP_INDEX:8;\n  CAN_UINT8 unused1:8;\n" \
           "  BMS_CELLTEMP_DATA_Sigbuf  bms_celltemp_data;\n}BMS19_100_msgType;" in text


def norm(text):
    import re
    return [re.sub(r"\s+", "", l) for l in text.split("\n") if l.strip()]


def test_put_get_functions_of_a_split_signal():
    from cogent_mux import get_functions, put_functions
    lays = {"BMS20_100": layout(VOLTS)}
    put = norm("\n".join(put_functions(lays)))
    assert put[:5] == norm("void ILRxPut_BMS_CELLVOLTAGE1(CAN_UINT16 data)\n{\n    CAN_ENTER_CRITICAL_SECTION(0);\n"
                           "   BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_0 = (CAN_UINT8) ((data) & 0x0f);\n"
                           "   BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_1 = (CAN_UINT8) (((data) >>4) & 0x3f);")
    get = norm("\n".join(get_functions(lays)))
    assert get[:6] == norm("CAN_UINT16 IlRxGetBMS_CELLVOLTAGE1(void)\n{\n   CAN_UINT16  rValue;\n"
                           "    CAN_ENTER_CRITICAL_SECTION(0);\n"
                           "   rValue = (CAN_UINT16)((CAN_UINT16)BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_0);\n"
                           "   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_1) << 4);")


def test_precopy_checks_only_the_received_index():
    from cogent_mux import precopy
    text = norm(precopy(layout(VOLTS)))
    assert text[:4] == norm("void BMS20_100_PreCopy (void)\n{\n   CAN_UINT16 rValue;\n"
                            "   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))")
    assert norm("if((BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX != "
                "Rx_buffer.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX))\n{\n"
                "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();") == text[5:8]
    assert norm("if(Rx_buffer.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX == 1)")[0] in text
    i = text.index(norm("if(rValue != BMS20_100__CELLVOLTAGE1)")[0])
    assert text[i:i + 5] == norm("if(rValue != BMS20_100__CELLVOLTAGE1)\n{\nBMS20_100__CELLVOLTAGE1 = rValue;\n"
                                 "ILSet_BMS_CELLVOLTAGE1_DataChanged();\n}")


def test_precopy_compares_a_plain_signal():
    from cogent_mux import precopy
    m = mes("GAP_100", [("SEL", "M", 0, 8), ("B", "m3", 16, 8), ("A", "m0", 24, 8), ("CRC", None, 56, 8)])
    text = norm(precopy(layout(m)))
    i = text.index(norm("if((GAP_100.gap_100.CRC != Rx_buffer.gap_100.CRC))")[0])
    assert text[i + 2] == "ILSet_CRC_DataChanged();"
    assert "CAN_UINT8rValue;" in text


def test_shadows():
    from cogent_mux import shadows
    assert shadows({"BMS19_100": layout(TEMPS)})[0] == "CAN_UINT16 BMS19_100__CELLTEMP1;"


def test_parser_reads_start_values_of_mixed_case_signals():
    """BA_ "GenSigStartValue" SG_ 1003 BMS_CellTemp1 500; - the signals page default comes from it."""
    import sys
    sys.path.insert(0, "tests")
    from support import load_fixture
    from Dbc_Parser import dbc_parser
    fx = load_fixture("s2xx_40024_a")
    sigs = {m["Msg_name"]: m["Sig_List"] for m in dbc_parser(str(fx.dbc), fx.node).get_msg_type("ALL", "rx")}
    assert sigs["BMS19_100"]["BMS_CELLTEMP1"]["GenSigStartValue"] == "500"
    assert sigs["BMS19_100"]["BMS_CELLTEMP_INDEX"]["GenSigStartValue"] == "0"
