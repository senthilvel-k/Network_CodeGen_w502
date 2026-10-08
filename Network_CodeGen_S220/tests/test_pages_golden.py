import json
import zipfile

import pytest

from support import (EXPECTED, PAGE_FILES, ROOT, _fail_with_diff, assert_same_file, fixture_names,
                     load_fixture)

# Pages archived in each saved .cfg were produced by the legacy tool in that session.
MSG_SIG_PAGES = [f for f in PAGE_FILES if not f.startswith("CanFilter")]

def _archived(name, fname):
    meta = json.loads((load_fixture(name).dir / "fixture.json").read_text(encoding="utf-8"))
    member = ("html/" if fname.endswith(".html") else "js/") + fname
    with zipfile.ZipFile(ROOT / meta["source_cfg"]) as z:
        return z.read(member)


@pytest.mark.parametrize("fname", MSG_SIG_PAGES)
@pytest.mark.parametrize("name", fixture_names())
def test_page_output_matches_archived_legacy_page(generated, name, fname):
    actual = (generated(name, "pages") / fname).read_bytes()
    expected = _archived(name, fname)
    if actual != expected:
        _fail_with_diff(actual, expected, fname, (name, fname), "archived-in-cfg(py27 run)")


@pytest.mark.parametrize("fname", PAGE_FILES)
@pytest.mark.parametrize("name", fixture_names())
def test_page_output_matches_py27(generated, name, fname):
    expected = EXPECTED / name / "pages" / fname
    if not expected.exists():
        pytest.skip("INCOMPLETE: no Python 2.7 oracle output (run tools/make_expected.py)")
    assert_same_file(generated(name, "pages") / fname, expected, (name, fname))
