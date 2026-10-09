import hashlib
import importlib.util
import sys

import pytest

from support import CODE_FILES, ROOT, load_fixture, run_harness


def _harness():
    spec = importlib.util.spec_from_file_location("gen_harness", ROOT / "tools" / "gen_harness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _digests(folder):
    return {name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in CODE_FILES}


def test_generation_is_repeatable_in_process(tmp_path):
    h, fx = _harness(), load_fixture("s237_36144")
    before = sys.stdout
    h.run(str(fx.dbc), fx.node, str(fx.data_dir), str(tmp_path / "a"), "code")
    assert sys.stdout is before
    h.run(str(fx.dbc), fx.node, str(fx.data_dir), str(tmp_path / "b"), "code")
    assert sys.stdout is before
    for name in CODE_FILES:
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes(), name


@pytest.mark.parametrize("name", ["s2xx_40024", "s237_36144_2"])
def test_three_separate_generations_are_byte_identical(tmp_path, name):
    fx = load_fixture(name)
    runs = []
    for i in range(3):
        out = tmp_path / f"run{i}"
        run_harness(sys.executable, fx, out, "code")
        runs.append(_digests(out))
    assert runs[0] == runs[1] == runs[2]
