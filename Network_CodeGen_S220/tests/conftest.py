import os
import sys

import pytest

os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from support import load_fixture, run_harness  # noqa: E402


@pytest.fixture(scope="session")
def generated(tmp_path_factory):
    cache = {}

    def get(name, stage):
        if (name, stage) not in cache:
            out = tmp_path_factory.mktemp(f"{name}_{stage}") / "out"
            run_harness(sys.executable, load_fixture(name), out, stage)
            cache[(name, stage)] = out
        return cache[(name, stage)]

    return get
