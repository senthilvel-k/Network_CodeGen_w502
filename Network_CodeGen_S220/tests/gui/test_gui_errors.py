"""Error popups of the GUI: each one names the operation, the cause, the file/input and the fix.

Uses the real 40024 "_Edited" DBC (from a folder whose name contains spaces and an apostrophe)
with the configuration saved in CODE_GEN/DBC_40024_2. Tests run in file order and share one app."""
import json
import shutil
import zipfile

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert
from support import CODE_FILES, LEGACY_REFS, normalize_header

pytestmark = pytest.mark.gui
FIXTURE = "s2xx_40024"
MSG_LINK = "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()"
SIG_LINK = "document.querySelector('a[href=\"BackEnd.Can_dbc0_sig\"]').click()"
CODE_GEN_BTN = "document.querySelector('input[name=code_generate]').click()"
FIFO_FILE = "CanFifoConfiguration.data"
# The legacy runs of 40024 use 209 receive rules; these limits keep the legacy comparisons meaningful.
LEGACY_LIMITS = {"max_rx_rules": 256, "max_rules_per_fifo": 128}
REFERENCE_CONFIG = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
                    "additional_rx_messages": ["BMS19_100", "BMS20_100"]}


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE,
                                                     dbc_folder="input DBC (Rev 40024, it's edited)")
    (home / "data" / FIFO_FILE).write_text(json.dumps(LEGACY_LIMITS), encoding="utf-8")
    yield back_end, home, fx, dbc
    restore()


def fill_and_load(qtbot, gui, dbc_text, node):
    js(qtbot, gui, "document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value=%s;"
                   "document.getElementById('form_submit').click(); 1" % (json.dumps(dbc_text), json.dumps(node)))
    settle(qtbot, gui)


def test_index_page_shows(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    with qtbot.waitSignal(gui.page.loadFinished, timeout=30000):
        gui.template = ("Tool_Index_Page.html", {})
    settle(qtbot, gui)
    gui.alerts.clear()


def test_message_page_before_load_dbc_asks_to_load_first(qtbot, app):
    gui = app[0].app
    js(qtbot, gui, MSG_LINK + "; 1")
    settle(qtbot, gui)
    assert len(gui.alerts) == 1, gui.alerts
    assert "Load DBC" in gui.alerts[0] and "TX/RX Message Configurations" in gui.alerts[0]
    assert gui.template[0] == "Tool_Index_Page.html"
    gui.alerts.clear()


def test_code_gen_before_load_dbc_explains(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, CODE_GEN_BTN)
    settle(qtbot, gui)
    assert len(gui.alerts) == 1 and "Load DBC" in gui.alerts[0] and "Code generation" in gui.alerts[0], gui.alerts
    gui.alerts.clear()


def test_load_dbc_with_empty_fields_shows_one_message(qtbot, app):
    gui = app[0].app
    fill_and_load(qtbot, gui, "", "")
    assert len(gui.alerts) == 1, gui.alerts
    assert "Loading the DBC failed" in gui.alerts[0]
    assert "DBC file" in gui.alerts[0] and "Node Name" in gui.alerts[0]
    gui.alerts.clear()


def test_load_dbc_missing_file_names_the_path(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    missing = (home / "no such folder" / "missing.dbc").as_posix()
    fill_and_load(qtbot, gui, missing, "SMART_CORE")
    assert len(gui.alerts) == 1, gui.alerts
    assert "DBC file not found" in gui.alerts[0] and missing in gui.alerts[0]
    gui.alerts.clear()


def test_load_dbc_unknown_node_lists_nodes(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    fill_and_load(qtbot, gui, dbc.as_posix(), "NO_SUCH_NODE")
    assert len(gui.alerts) == 1, gui.alerts
    text = gui.alerts[0]
    assert "NO_SUCH_NODE" in text and "not defined" in text and "SMART_CORE" in text and dbc.name in text
    gui.alerts.clear()


def test_load_dbc_succeeds(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    fill_and_load(qtbot, gui, dbc.as_posix(), "SMART_CORE")
    assert any("Database loaded successfully" in a for a in gui.alerts), gui.alerts
    gui.alerts.clear()


def test_code_gen_before_saving_pages_names_the_pages(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, CODE_GEN_BTN)
    settle(qtbot, gui)
    assert len(gui.alerts) == 1, gui.alerts
    assert "TX/RX Message Configurations" in gui.alerts[0] and "TX/Rx signal Configurations" in gui.alerts[0]
    gui.alerts.clear()


def test_message_page_opens_without_saved_message_configuration(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / "CanDbcMsgConfiguration.data").unlink()
    navigate(qtbot, gui, MSG_LINK)
    settle(qtbot, gui)
    assert gui.alerts == [] and gui.template[0] == "CAN_DBC_msg.html"
    msg_data = (fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8")
    navigate(qtbot, gui, "BackEnd.Can_dbc_msg_SaveButton(%s)" % json.dumps(msg_data))


def test_signal_page_opens_without_saved_signal_configuration(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / "CanDbcSigConfiguration.data").unlink()
    gui.console.clear()
    navigate(qtbot, gui, SIG_LINK)
    settle(qtbot, gui)
    assert gui.alerts == [] and gui.template[0] == "CAN_DBC_sig.html"
    assert not [c for c in gui.console if "SyntaxError" in c[0]], gui.console
    sig_data = (fx.data_dir / "CanDbcSigConfiguration.data").read_text(encoding="utf-8")
    navigate(qtbot, gui, "BackEnd.Can_dbc0_sig_SaveButton(%s)" % json.dumps(sig_data))


def test_code_gen_matches_legacy_and_keeps_path_with_apostrophe(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    text = wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    assert "11 files" in text
    legacy = LEGACY_REFS[FIXTURE][0]
    for name in CODE_FILES:
        assert normalize_header((home / "CODE_GEN" / name).read_bytes()) == \
            normalize_header((legacy / name).read_bytes()), name
    assert js(qtbot, gui, "document.getElementById('file_path').value") == dbc.as_posix()
    assert js(qtbot, gui, "document.getElementById('ch0_node_name').value") == "SMART_CORE"
    gui.alerts.clear()


def test_code_gen_failure_explains_and_keeps_previous_files(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    before = {n: (home / "CODE_GEN" / n).read_bytes() for n in CODE_FILES}
    data = json.loads((fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    data["BMS19_100_rx_enable"] = "on"
    navigate(qtbot, gui, "BackEnd.Can_dbc_msg_SaveButton(%s)" % json.dumps(json.dumps(data)))
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    settle(qtbot, gui)
    assert len(gui.alerts) == 1, gui.alerts
    text = gui.alerts[0]
    assert text.startswith("Code generation failed") and "BMS19_100" in text and "Traceback" not in text
    assert "errorlog.txt" in text
    assert {n: (home / "CODE_GEN" / n).read_bytes() for n in CODE_FILES} == before
    assert "Traceback" in (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")
    original = (fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8")
    navigate(qtbot, gui, "BackEnd.Can_dbc_msg_SaveButton(%s)" % json.dumps(original))
    gui.alerts.clear()


def test_code_gen_overflow_popup_names_rules_messages_and_candidates(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    before = {n: (home / "CODE_GEN" / n).read_bytes() for n in CODE_FILES}
    (home / "data" / FIFO_FILE).unlink()                     # platform defaults: 192 rules, 64 per FIFO
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    settle(qtbot, gui)
    assert len(gui.alerts) == 1, gui.alerts
    text = gui.alerts[0]
    assert text.startswith("Code generation failed while planning the CAN receive rules")
    assert "209 receive rules are needed but the controller accepts at most 192" in text
    assert "0x4F0-0x4FF: 16 messages" in text and "merge_blocks" in text and "Traceback" not in text
    assert {n: (home / "CODE_GEN" / n).read_bytes() for n in CODE_FILES} == before
    gui.alerts.clear()


def test_code_gen_with_merged_blocks_reports_rules_and_manual_actions(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / FIFO_FILE).write_text(json.dumps(REFERENCE_CONFIG), encoding="utf-8")
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    text = wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    assert "CAN receive rules: 184 of 192 (FIFO 0/1/2: 64/64/56)" in text
    assert "Manual action required: 5 item(s), see CODE_GEN\\MANUAL_ACTIONS.md" in text
    report = (home / "CODE_GEN" / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "nw_can_dll.c dispatch for the merged block 0x3D0-0x3DF" in report
    assert json.loads((home / "CODE_GEN" / "fifo_plan.json").read_text(encoding="utf-8"))["total_rules"] == 184
    settle(qtbot, gui)
    gui.alerts.clear()


def test_save_configuration_failure_is_not_reported_as_success(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "Config").write_text("a file where the Config folder should be", encoding="utf-8")
    js(qtbot, gui, "document.querySelector('input[name=save_cofiguration]').click(); 1")
    settle(qtbot, gui)
    assert not any("saved successfully" in a for a in gui.alerts), gui.alerts
    assert len(gui.alerts) == 1 and "Saving the configuration failed" in gui.alerts[0], gui.alerts
    (home / "Config").unlink()
    gui.alerts.clear()


def test_save_configuration_reports_the_archive_path(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    js(qtbot, gui, "document.querySelector('input[name=save_cofiguration]').click(); 1")
    text = wait_alert(qtbot, gui, "Configuration saved successfully")
    saved = list((home / "Config").glob("*.cfg"))
    assert len(saved) == 1 and saved[0].name in text
    with zipfile.ZipFile(saved[0]) as z:                       # the FIFO configuration belongs to the project
        assert json.loads(z.read("data/" + FIFO_FILE).decode("utf-8")) == REFERENCE_CONFIG
    settle(qtbot, gui)
    gui.alerts.clear()


def test_load_configuration_cancel_shows_nothing(qtbot, app, monkeypatch):
    back_end = app[0]
    gui = back_end.app
    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: ("", "")))
    js(qtbot, gui, "document.querySelector('input[name=load_cofiguration]').click(); 1")
    settle(qtbot, gui)
    assert gui.alerts == []


def test_load_configuration_rejects_a_non_archive_with_reason(qtbot, app, monkeypatch):
    back_end, home, fx, dbc = app
    gui = back_end.app
    notes = home / "notes.txt"
    notes.write_text("not a configuration", encoding="utf-8")
    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName",
                        staticmethod(lambda *a, **k: (str(notes), "")))
    js(qtbot, gui, "document.querySelector('input[name=load_cofiguration]').click(); 1")
    settle(qtbot, gui)
    assert len(gui.alerts) == 1, gui.alerts
    assert "Loading the configuration failed" in gui.alerts[0] and "notes.txt" in gui.alerts[0]
    assert "configuration archive" in gui.alerts[0]
    gui.alerts.clear()


def test_load_archive_without_fifo_configuration_sets_the_current_one_aside(qtbot, app, monkeypatch):
    back_end, home, fx, dbc = app
    gui = back_end.app
    old = home / "older project.cfg"
    with zipfile.ZipFile(old, "w") as z:                       # as saved before the FIFO configuration existed
        for name in ("dbc_details.data", "CanDbcMsgConfiguration.data", "CanDbcSigConfiguration.data"):
            z.write(home / "data" / name, "data/" + name)
    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: (str(old), "")))
    js(qtbot, gui, "document.querySelector('input[name=load_cofiguration]').click(); 1")
    text = wait_alert(qtbot, gui, "Configuration loaded successfully")
    assert "renamed to CanFifoConfiguration.data.previous" in text
    assert not (home / "data" / FIFO_FILE).exists()
    aside = home / "data" / (FIFO_FILE + ".previous")
    assert json.loads(aside.read_text(encoding="utf-8")) == REFERENCE_CONFIG
    aside.replace(home / "data" / FIFO_FILE)
    settle(qtbot, gui)
    gui.alerts.clear()


def test_browse_cancel_keeps_the_dbc_path(qtbot, app, monkeypatch):
    back_end, home, fx, dbc = app
    gui = back_end.app
    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName", staticmethod(lambda *a, **k: ("", "")))
    before = js(qtbot, gui, "document.getElementById('file_path').value")
    assert before
    js(qtbot, gui, "document.getElementById('ch0_dbc_file').click(); 1")
    settle(qtbot, gui)
    assert js(qtbot, gui, "document.getElementById('file_path').value") == before


def test_filter_page_opens_without_error_popup(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.Can_Filter()")
    settle(qtbot, gui)
    assert gui.alerts == [] and gui.template[0] == "Can_filter.html"
    navigate(qtbot, gui, "BackEnd.default_page()")
