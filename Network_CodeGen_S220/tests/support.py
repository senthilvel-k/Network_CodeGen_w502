import difflib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
EXPECTED = ROOT / "tests" / "expected"  # Python 2.7 oracle output (tools/make_expected.py)
HARNESS = ROOT / "tools" / "gen_harness.py"
DUMP = ROOT / "tools" / "dump_dbc.py"
ACCEPTED = ROOT / "tests" / "accepted_order_diffs.json"

CODE_FILES = [
    "can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
    "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
    "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h",
]
PAGE_FILES = [
    "CanDbcMsgConfiguration.html", "CanDbcMsgConfiguration.js",
    "CanDbcSigConfiguration.html", "CanDbcSigConfiguration.js",
    "CanFilterconfiguration.html", "CanFilterconfiguration.js",
]

# Known-good legacy runs produced by the CURRENT source (output dates after the last
# generator edit, 2024-07-02) with the same DBC and saved configuration:
# fixture -> (legacy CODE_GEN folder, files compared).
LEGACY_REFS = {
    "s237_36144_2": (ROOT / "CODE_GEN" / "DBC_S237_36144_2", CODE_FILES),
    "s2xx_40024": (ROOT / "CODE_GEN" / "DBC_40024_2", CODE_FILES),
    "s2xx_40024_a": (ROOT / "CODE_GEN" / "DBC_40024", CODE_FILES),
}
# Legacy runs made by OLDER generator code: informational comparison only.
OLD_CODE_REFS = {
    "s237_35354": ROOT / "CODE_GEN" / "DBC_S237_35354",
    "s237_35891": ROOT / "CODE_GEN" / "DBC_S237_35891",
    "s237_36026": ROOT / "CODE_GEN" / "DBC_S237_36026",
    "s237_36144": ROOT / "CODE_GEN" / "DBC_S237_36144",
}


@dataclass(frozen=True)
class Fixture:
    name: str
    dir: Path
    dbc: Path
    node: str
    data_dir: Path


def fixture_names():
    if not FIXTURES.exists():
        return []
    return sorted(p.name for p in FIXTURES.iterdir() if (p / "fixture.json").exists())


def load_fixture(name):
    d = FIXTURES / name
    meta = json.loads((d / "fixture.json").read_text(encoding="utf-8"))
    return Fixture(name, d, d / meta["dbc"], meta["node"], d / "data")


def run_harness(python, fx, out, stage, dbc=None, data_dir=None):
    cmd = [str(python), "-B", str(HARNESS), "--dbc", str(dbc or fx.dbc), "--node", fx.node,
           "--data", str(data_dir or fx.data_dir), "--out", str(out), "--stage", stage]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        pytest.fail(f"harness failed for {fx.name}/{stage}:\n{r.stderr[-4000:]}")


def _accepted():
    if not ACCEPTED.exists():
        return set()
    return {tuple(x) for x in json.loads(ACCEPTED.read_text(encoding="utf-8"))}


def _fail_with_diff(a, e, name, key, label):
    al = a.decode("latin-1").splitlines()
    el = e.decode("latin-1").splitlines()
    order_only = sorted(al) == sorted(el)
    if order_only and tuple(key) in _accepted():
        return
    diff = "\n".join(list(difflib.unified_diff(el, al, label, "actual", lineterm="", n=2))[:80])
    kind = "ORDER-ONLY" if order_only else "CONTENT"
    pytest.fail(f"{name} differs ({kind}) for {key}:\n{diff}")


def assert_same_file(actual, expected, key):
    a, e = actual.read_bytes(), expected.read_bytes()
    if a != e:
        _fail_with_diff(a, e, actual.name, key, "expected(py27)")


HEADER_ALL = re.compile(rb"^(Date|By|Traceability)[ \t]*:.*$", re.M)
HEADER_DATE_BY = re.compile(rb"^(Date|By)[ \t]*:.*$", re.M)


def normalize_header(data):
    """Blank the per-run revision-note lines (date, user, DBC file name)."""
    return HEADER_ALL.sub(lambda m: m.group(1) + b": <normalized>", data)


def normalize_date_by(data):
    return HEADER_DATE_BY.sub(lambda m: m.group(1) + b": <normalized>", data)


def assert_same_as_legacy(actual, legacy, key):
    a, e = normalize_header(actual.read_bytes()), normalize_header(legacy.read_bytes())
    if a != e:
        _fail_with_diff(a, e, actual.name, key, "legacy(py27 run)")
