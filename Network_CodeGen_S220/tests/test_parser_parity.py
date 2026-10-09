import json
import subprocess
import sys

import pytest

from support import DUMP, EXPECTED, fixture_names, load_fixture


@pytest.mark.parametrize("name", fixture_names())
def test_parser_matches_py27(name):
    expected = EXPECTED / name / "parser.json"
    if not expected.exists():
        pytest.skip("INCOMPLETE: no Python 2.7 oracle output (run tools/make_expected.py)")
    fx = load_fixture(name)
    r = subprocess.run([sys.executable, "-B", str(DUMP), str(fx.dbc), fx.node], capture_output=True)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[-4000:]
    assert json.loads(r.stdout) == json.loads(expected.read_bytes())


@pytest.mark.parametrize("name", fixture_names())
def test_parser_dump_runs_and_finds_node(name):
    fx = load_fixture(name)
    r = subprocess.run([sys.executable, "-B", str(DUMP), str(fx.dbc), fx.node], capture_output=True)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[-4000:]
    dump = json.loads(r.stdout)
    assert dump["node_ok"] is True
    assert dump["GenMsgILSupport/tx"] and dump["GenMsgILSupport/rx"]
