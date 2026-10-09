"""End-to-end GUI workflow, in-process: the real back_end/CoGeNT pages driven through QtWebEngine.

Flow per the index page: Load DBC -> TX/RX message page -> Save -> signal page -> Save ->
code gen -> 11 files in CODE_GEN. Runs from a copy of the app in a folder whose path has spaces."""
import json
import sys

import pytest

from gui_support import js, navigate, start_app_copy, wait_alert, wait_ready
from support import CODE_FILES, LEGACY_REFS, normalize_header

pytestmark = pytest.mark.gui
FIXTURE = "s237_36144_2"


@pytest.fixture(scope="module")
def app_copy(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE)
    yield back_end, home, fx, dbc
    restore()  # window lives for the whole module, not one test


def test_full_generate_flow_matches_legacy_run(qtbot, app_copy):
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    with qtbot.waitSignal(gui.page.loadFinished, timeout=30000):
        gui.template = ("Tool_Index_Page.html", {})
    wait_ready(qtbot, gui)

    # upload_dbc only alerts; it does not change the page, so no loadFinished to wait for
    js(qtbot, gui, f"document.getElementById('file_path').value={json.dumps(dbc.as_posix())};"
                   f"document.getElementById('ch0_node_name').value={json.dumps(fx.node)};"
                   "document.getElementById('form_submit').click(); 1")
    wait_alert(qtbot, gui, "Database loaded successfully")

    msg_data = (fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8")
    sig_data = (fx.data_dir / "CanDbcSigConfiguration.data").read_text(encoding="utf-8")
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()")
    assert gui.template[0] == "CAN_DBC_msg.html"
    navigate(qtbot, gui, f"BackEnd.Can_dbc_msg_SaveButton({json.dumps(msg_data)})")
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_sig\"]').click()")
    assert gui.template[0] == "CAN_DBC_sig.html"
    navigate(qtbot, gui, f"BackEnd.Can_dbc0_sig_SaveButton({json.dumps(sig_data)})")

    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    legacy_dir = LEGACY_REFS[FIXTURE][0]
    for name in CODE_FILES:
        assert normalize_header((home / "CODE_GEN" / name).read_bytes()) == \
            normalize_header((legacy_dir / name).read_bytes()), name


def test_real_save_and_back_forms_keep_saved_configuration(qtbot, app_copy):
    """Open each configuration page (filled from the saved .data) and press its real
    "Save and Back" button: the re-saved .data must be byte-identical, and code gen must
    still reproduce the legacy run."""
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    for link, page, data_name in (("BackEnd.Can_dbc0_msg", "CAN_DBC_msg.html", "CanDbcMsgConfiguration.data"),
                                  ("BackEnd.Can_dbc0_sig", "CAN_DBC_sig.html", "CanDbcSigConfiguration.data")):
        navigate(qtbot, gui, f"document.querySelector('a[href=\"{link}\"]').click()")
        assert gui.template[0] == page
        navigate(qtbot, gui, "document.getElementById('form_submit').click()")
        assert gui.template[0] == "Tool_Index_Page.html"
        assert (home / "data" / data_name).read_bytes() == (fx.data_dir / data_name).read_bytes(), data_name
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    legacy_dir = LEGACY_REFS[FIXTURE][0]
    for name in CODE_FILES:
        assert normalize_header((home / "CODE_GEN" / name).read_bytes()) == \
            normalize_header((legacy_dir / name).read_bytes()), name


def test_second_generate_in_same_session_gives_identical_files(qtbot, app_copy):
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    first = {n: (home / "CODE_GEN" / n).read_bytes() for n in CODE_FILES}
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    for n in CODE_FILES:
        second = (home / "CODE_GEN" / n).read_bytes()
        # Only the revision-note "Date" line (minute resolution) may differ between runs.
        assert normalize_header(second) == normalize_header(first[n]), n
        changed = [i for i, (a, b) in enumerate(zip(second.splitlines(), first[n].splitlines())) if a != b]
        assert all(second.splitlines()[i].startswith(b"Date") for i in changed), n


def test_browse_button_puts_chosen_dbc_path_in_field(qtbot, app_copy, monkeypatch):
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    chosen = dbc.as_posix()
    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName",
                        staticmethod(lambda *a, **k: (chosen, "DBC files (*.dbc)")))
    js(qtbot, gui, "document.getElementById('ch0_dbc_file').click(); 1")
    qtbot.waitUntil(lambda: js(qtbot, gui, "document.getElementById('file_path').value") == chosen, timeout=20000)


def test_save_and_load_configuration_round_trip(qtbot, app_copy, monkeypatch):
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    config_dir = home / "Config"
    before = set(config_dir.glob("*.cfg")) if config_dir.exists() else set()
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('input[name=save_cofiguration]').click()")
    wait_alert(qtbot, gui, "Configuration saved successfully")
    qtbot.waitUntil(lambda: len(set(config_dir.glob("*.cfg")) - before) == 1, timeout=20000)
    saved = (set(config_dir.glob("*.cfg")) - before).pop()
    import zipfile
    with zipfile.ZipFile(saved) as z:
        names = set(z.namelist())
        assert {"data/CanDbcMsgConfiguration.data", "data/CanDbcSigConfiguration.data",
                "data/dbc_details.data", "html/Tool_Index_Page.html", "js/CanDbcMsgConfiguration.js"} <= names
        assert z.read("data/CanDbcMsgConfiguration.data") == (fx.data_dir / "CanDbcMsgConfiguration.data").read_bytes()

    monkeypatch.setattr(back_end.QtWidgets.QFileDialog, "getOpenFileName",
                        staticmethod(lambda *a, **k: (str(saved), "Config files (*.cfg)")))
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('input[name=load_cofiguration]').click()")
    wait_alert(qtbot, gui, "Configuration loaded successfully")


def test_generation_error_then_message_page_still_opens(qtbot, app_copy):
    back_end, home, fx, dbc = app_copy
    gui = back_end.app
    (home / "data" / "CanDbcMsgConfiguration.data").write_text("{}", encoding="utf-8")
    gui.alerts.clear()
    navigate(qtbot, gui, "BackEnd.default_page()")
    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    text = wait_alert(qtbot, gui, "Code generation failed")
    assert "CanDbcMsgConfiguration.data" in text and "Traceback" not in text
    assert (home / "CODE_GEN" / "errorlog.txt").exists()
    assert not getattr(sys.stdout, "closed", False)  # stdout not left on a generator file
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()")
    assert gui.alerts == []
    assert gui.template[0] == "CAN_DBC_msg.html"
