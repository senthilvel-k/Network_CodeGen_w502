import sys

from support import ROOT

DBC = ROOT / "DBC" / "S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc"


def test_parser_reads_dbc_with_undefined_cp1252_bytes(tmp_path):
    dbc = tmp_path / "weird.dbc"
    dbc.write_bytes(DBC.read_bytes() + b'\r\nCM_ "bytes \x81\x8d\x90 not in cp1252";\r\n')
    sys.path.insert(0, str(ROOT))
    from Dbc_Parser import dbc_parser
    assert dbc_parser(str(dbc), "SMART_CORE").check_parsing() is True
    assert dbc_parser(str(dbc), "SMART_CORE").check__node() is True
