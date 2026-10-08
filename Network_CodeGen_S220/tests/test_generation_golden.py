import pytest

from support import (CODE_FILES, EXPECTED, LEGACY_REFS, assert_same_as_legacy, assert_same_file,
                     fixture_names)


LEGACY_CASES = [(name, fname) for name, (_, files) in sorted(LEGACY_REFS.items()) for fname in files]


@pytest.mark.parametrize("name,fname", LEGACY_CASES)
def test_code_output_matches_legacy_run(generated, name, fname):
    """Byte-identical to a known-good Python 2.7 run of the same source (headers normalized)."""
    legacy_dir = LEGACY_REFS[name][0]
    assert_same_as_legacy(generated(name, "code") / fname, legacy_dir / fname, (name, fname))


@pytest.mark.parametrize("name", fixture_names())
def test_every_fixture_generates_all_files(generated, name):
    out = generated(name, "code")
    missing = [f for f in CODE_FILES if not (out / f).is_file() or (out / f).stat().st_size == 0]
    assert missing == []


@pytest.mark.parametrize("fname", CODE_FILES)
@pytest.mark.parametrize("name", fixture_names())
def test_code_output_matches_py27(generated, name, fname):
    expected = EXPECTED / name / "code" / fname
    if not expected.exists():
        pytest.skip("INCOMPLETE: no Python 2.7 oracle output (run tools/make_expected.py)")
    assert_same_file(generated(name, "code") / fname, expected, (name, fname))
