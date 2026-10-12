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


def latest_run(home):
    """The newest run folder CODE_GEN/<date_time> of an app folder."""
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import cogent_generate
    run = cogent_generate.latest_run(str(Path(home) / "CODE_GEN"))
    assert run, "no run folder in %s" % (Path(home) / "CODE_GEN")
    return Path(run)


def run_file(home, name):
    """A generated file of the newest run folder (in the repository layout)."""
    import cogent_generate
    return latest_run(home) / cogent_generate.output_relpath(name)


def enable_indexed(home, dbc, node="SMART_CORE", names=("BMS19_100", "BMS20_100"), notify="200ms_Delay_g1"):
    """Enable receive messages and give their signals the settings the TX/RX signals page saves for new
    signals (init value = DBC start value), with the notification group of the S2XX BMS signals."""
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from Dbc_Parser import dbc_parser
    data = Path(home) / "data"
    msg_cfg = json.loads((data / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    sig_cfg = json.loads((data / "CanDbcSigConfiguration.data").read_text(encoding="utf-8"))
    for mes in dbc_parser(str(dbc), node).get_msg_type("ALL", "rx"):
        if mes["Msg_name"] in names:
            msg_cfg[mes["Msg_name"] + "_rx_enable"] = "on"
            for sig, d in mes["Sig_List"].items():
                start = d.get("GenSigStartValue") or "0"
                sig_cfg.update({sig + "_green_drive": "", sig + "_os_notify_no_of_events": notify,
                                sig + "_rx_init_value": hex(int(float(start))),
                                sig + "_signal_content": "", sig + "_signal_fault_id": ""})
    (data / "CanDbcMsgConfiguration.data").write_text(json.dumps(msg_cfg), encoding="utf-8")
    (data / "CanDbcSigConfiguration.data").write_text(json.dumps(sig_cfg), encoding="utf-8")


# The Code overrides of the S2XX hand edits (data\CanOverrideConfiguration.data), with neutral names for the
# NM buffer and the host function (the repository is public; tests/test_overrides_reference.py uses the
# project's own names from your local configuration archive)
S2XX_OVERRIDES = {
    "tx": dict([("EX_SUMMARY_RESPONSE_%d" % i, {"attribute": "Event", "period": 0, "offset": 0}) for i in range(4)] + [
        ("MCM_SP", {"attribute": "Event", "offset": 0}),
        ("MCM_WAKEUP", {"attribute": "Event"}),
        ("REM_ACK_MSG", {"attribute": "Periodic+Event"}),
        ("IC10_200", {"confirmation": True}),
        ("IC11_500", {"confirmation": True}),
        ("MCM4_1000", {"confirmation": True})]),
    "rx": {"TC_NSM": {"timeout": 100}},
    "nm_tx": [{"message": "MCM_WAKEUP", "label": "MCM_WAKEUP_REASON", "buffer": "Nm_wakeup_buffer"},
              {"message": "IC_ACTIVE", "label": "IC_ACTIVE", "buffer": "Nm_msg_buffer"},
              {"message": "MCM_ACTIVE", "label": "MCM_ACTIVE", "buffer": "Nm_msg_buffer"},
              {"message": "IS_ACTIVE", "label": "IS_ACTIVE", "buffer": "Nm_msg_buffer"},
              {"message": "MCM_SLEEP", "label": "MCM_SLEEP", "buffer": "Nm_msg_buffer"}],
    "host_forward": {"prefix": "REM_MSG_", "function": "host_update_msg"},
    "numeric_order": ["REM_MSG_"],
}


S2XX_FIFO = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
             "additional_rx_messages": ["BMS19_100", "BMS20_100"]}


def s2xx_max_match(home, dbc, node="SMART_CORE"):
    """Settings that reproduce the S2XX workspace: BMS19_100 / BMS20_100 enabled (cell temperatures typed as
    0x1F4, as in the workspace), Tx debounce on REMOTE_HV_CONNECT_REQ_TGU instead of CHARGING_ON_OFF_REQ,
    the Receive FIFO blocks (when none are saved) and the Code overrides."""
    enable_indexed(home, dbc, node)
    data = Path(home) / "data"
    sig = json.loads((data / "CanDbcSigConfiguration.data").read_text(encoding="utf-8"))
    sig.update({"BMS_CELLTEMP%d_rx_init_value" % k: "0x1F4" for k in range(1, 33)})
    sig.update({"CHARGING_ON_OFF_REQ_tx_debounce": "", "REMOTE_HV_CONNECT_REQ_TGU_tx_debounce": "on"})
    (data / "CanDbcSigConfiguration.data").write_text(json.dumps(sig), encoding="utf-8")
    if not (data / "CanFifoConfiguration.data").exists():
        (data / "CanFifoConfiguration.data").write_text(json.dumps(S2XX_FIFO, indent=1), encoding="utf-8")
    (data / "CanOverrideConfiguration.data").write_text(json.dumps(S2XX_OVERRIDES, indent=1), encoding="utf-8")


def run_folder_count(home):
    import cogent_generate
    return len(cogent_generate.run_folders(str(Path(home) / "CODE_GEN")))


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


PRECOPY_HEAD = re.compile(rb"^void \w+_PreCopy \(void\)")
RVALUE_DECLARED = re.compile(rb"^\s+\w+\s+rValue;")


def comment_precopy_rvalue(data):
    """The legacy PreCopy wrote stray 'rValue |= ...' lines where rValue is not declared (does not
    compile); CoGeNT writes them commented out, as the S2XX workspace has them. Applied to the legacy
    references of nw_il_par.c."""
    out, inside, declared = [], False, False
    for line in data.split(b"\n"):
        if PRECOPY_HEAD.match(line):
            inside, declared = True, False
        elif line.rstrip(b"\r") == b"}":
            inside = False
        declared = declared or (inside and bool(RVALUE_DECLARED.match(line)))
        if inside and not declared and line.startswith(b"   rValue |= "):
            line = b"   // " + line[3:]
        out.append(line)
    return b"\n".join(out)


def reference_bytes(path):
    data = path.read_bytes()
    return comment_precopy_rvalue(data) if path.name == "nw_il_par.c" else data


def assert_same_file(actual, expected, key):
    a, e = actual.read_bytes(), reference_bytes(expected)
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
    a, e = normalize_header(actual.read_bytes()), normalize_header(reference_bytes(legacy))
    if a != e:
        _fail_with_diff(a, e, actual.name, key, "legacy(py27 run)")
