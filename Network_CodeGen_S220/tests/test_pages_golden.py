import json
import re
import zipfile

import pytest

from support import (EXPECTED, PAGE_FILES, ROOT, _fail_with_diff, assert_same_file, fixture_names,
                     load_fixture)

# Pages archived in each saved .cfg were produced by the legacy tool in that session.
MSG_SIG_PAGES = [f for f in PAGE_FILES if not f.startswith("CanFilter")]

# Labels corrected on purpose after the legacy tool (spelling, page titles); applied to the legacy pages
# before comparing, so every other byte must still be identical.
LABEL_FIXES = {
    "CanDbcMsgConfiguration.html": [(b"<title>Filter</title>", b"<title>CoGeNT - TX/RX messages</title>"),
                                    (b"<th>Message Timout ID</th>", b"<th>Message Timeout ID</th>")],
    "CanDbcSigConfiguration.html": [(b"<title>Filter</title>", b"<title>CoGeNT - TX/RX signals</title>"),
                                    (b"<th>byte_order</th>", b"<th>Byte order</th>"),
                                    (b"<th>Byte_order</th>", b"<th>Byte order</th>")],
    "CanFilterconfiguration.html": [(b"<title>Filter</title>", b"<title>CoGeNT - Filter</title>"),
                                    (b"<th>Messsage Type</th>", b"<th>Message Type</th>")],
}


def with_label_fixes(fname, legacy):
    for old, new in LABEL_FIXES.get(fname, []):
        legacy = legacy.replace(old, new)
    return legacy


INIT_VALUE = re.compile(rb'(id = "([A-Z0-9_]+)_(?:tx|rx)_init_value" name = "[^"]*" value =")([^"]*)(")')


def with_dbc_start_values(name, fname, legacy):
    """The init value shown for a signal without saved settings is its DBC start value. The legacy parser
    ignored the start value of signals whose DBC name is not upper case (BMS_CellTemp1 500 -> 0x0); fixed
    on purpose (multiplex-generation spec, section 6), so the archived page gets the DBC start values."""
    if fname != "CanDbcSigConfiguration.html":
        return legacy
    import sys
    sys.path.insert(0, str(ROOT))
    from Can_dbc_gen import init_value_default
    from Dbc_Parser import dbc_parser
    fx = load_fixture(name)
    parser = dbc_parser(str(fx.dbc), fx.node)
    start = {sig: d.get("GenSigStartValue") for direction in ("tx", "rx")
             for mes in parser.get_msg_type("ALL", direction) for sig, d in mes["Sig_List"].items()}
    return INIT_VALUE.sub(lambda m: m.group(1) + init_value_default(start.get(m.group(2).decode())).encode() + m.group(4),
                          legacy)

def _archived(name, fname):
    meta = json.loads((load_fixture(name).dir / "fixture.json").read_text(encoding="utf-8"))
    member = ("html/" if fname.endswith(".html") else "js/") + fname
    with zipfile.ZipFile(ROOT / meta["source_cfg"]) as z:
        return z.read(member)


@pytest.mark.parametrize("fname", MSG_SIG_PAGES)
@pytest.mark.parametrize("name", fixture_names())
def test_page_output_matches_archived_legacy_page(generated, name, fname):
    actual = (generated(name, "pages") / fname).read_bytes()
    expected = with_dbc_start_values(name, fname, with_label_fixes(fname, _archived(name, fname)))
    if actual != expected:
        _fail_with_diff(actual, expected, fname, (name, fname), "archived-in-cfg(py27 run)")


@pytest.mark.parametrize("fname", PAGE_FILES)
@pytest.mark.parametrize("name", fixture_names())
def test_page_output_matches_py27(generated, name, fname):
    expected = EXPECTED / name / "pages" / fname
    if not expected.exists():
        pytest.skip("INCOMPLETE: no Python 2.7 oracle output (run tools/make_expected.py)")
    actual = (generated(name, "pages") / fname).read_bytes()
    legacy = with_label_fixes(fname, expected.read_bytes())
    if actual != legacy:
        _fail_with_diff(actual, legacy, fname, (name, fname), "expected(py27)")
