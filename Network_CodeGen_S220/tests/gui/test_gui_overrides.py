"""Code overrides page: sidebar link, the saved settings as rows, Save, invalid entries named on the page.
Real 40024 DBC + CODE_GEN/DBC_40024_2 configuration. Tests run in file order and share one app."""
import json

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert

pytestmark = pytest.mark.gui
FIXTURE = "s2xx_40024"
FILE = "CanOverrideConfiguration.data"
LINK = "document.querySelector('a[href=\"BackEnd.overrides_page\"]').click()"
SAVE = "document.getElementById('ov-save').click()"


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE, dbc_folder="input DBC 40024")
    yield back_end, home, fx, dbc
    restore()


def row(table, msg):
    return "document.querySelector('#%s tr[data-msg=\"%s\"]')" % (table, msg)


def saved(home):
    return json.loads((home / "data" / FILE).read_text(encoding="utf-8"))


def test_page_needs_a_loaded_dbc(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.default_page()")
    gui.alerts.clear()
    js(qtbot, gui, LINK + "; 1")
    wait_alert(qtbot, gui, "no DBC is loaded")
    settle(qtbot, gui)


def test_sidebar_link_between_receive_fifo_and_reapply(qtbot, app):
    gui = app[0].app
    hrefs = js(qtbot, gui, "Array.from(document.querySelectorAll('.cg-nav a')).map(function (a) "
                           "{ return a.getAttribute('href'); }).join(',')")
    assert "BackEnd.fifo_page,BackEnd.overrides_page,BackEnd.reapply_page" in hrefs


def test_page_shows_the_saved_settings(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / FILE).write_text(json.dumps({"tx": {"IC10_200": {"confirmation": True}},
                                                  "rx": {"TC_NSM": {"timeout": 100}},
                                                  "numeric_order": ["REM_MSG_"]}), encoding="utf-8")
    gui.alerts.clear()
    js(qtbot, gui, "document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value=%s;"
                   "document.getElementById('form_submit').click(); 1" % (json.dumps(dbc.as_posix()), json.dumps(fx.node)))
    wait_alert(qtbot, gui, "Database loaded successfully")
    settle(qtbot, gui)
    navigate(qtbot, gui, LINK)
    assert gui.template[0] == "Overrides.html"
    assert js(qtbot, gui, row("tx-rows", "IC10_200") + ".querySelector('.tx-conf').checked") is True
    assert js(qtbot, gui, row("rx-rows", "TC_NSM") + ".querySelector('.rx-timeout').value") == "100"
    assert js(qtbot, gui, "document.getElementById('numeric-order').value") == "REM_MSG_"
    options = js(qtbot, gui, "Array.from(document.querySelectorAll('#tx-add option')).map(function (o) "
                             "{ return o.value; }).join(',')")
    assert "MCM_SP" in options.split(",") and "TC_NSM" not in options.split(",")     # transmit messages only


def test_save_writes_the_settings(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    js(qtbot, gui, "document.getElementById('tx-add').value='MCM_SP'; addTx(); 1")
    js(qtbot, gui, "var r=" + row("tx-rows", "MCM_SP") + "; r.querySelector('.tx-attr').value='Event';"
                   "r.querySelector('.tx-offset').value='0'; 1")
    js(qtbot, gui, "document.getElementById('nm-add').value='IC_ACTIVE'; addNm(); 1")
    js(qtbot, gui, "var r=document.querySelector('#nm-rows tr:last-child'); r.querySelector('.nm-label').value='IC_ACTIVE';"
                   "r.querySelector('.nm-buffer').value='Nm_msg_buffer'; 1")
    js(qtbot, gui, "document.getElementById('host-prefix').value='REM_MSG_';"
                   "document.getElementById('host-function').value='host_update_msg'; 1")
    navigate(qtbot, gui, SAVE)
    assert saved(home) == {"tx": {"IC10_200": {"confirmation": True}, "MCM_SP": {"attribute": "Event", "offset": 0}},
                           "rx": {"TC_NSM": {"timeout": 100}},
                           "nm_tx": [{"message": "IC_ACTIVE", "label": "IC_ACTIVE", "buffer": "Nm_msg_buffer"}],
                           "host_forward": {"prefix": "REM_MSG_", "function": "host_update_msg"},
                           "numeric_order": ["REM_MSG_"]}
    assert "Saved" in js(qtbot, gui, "document.getElementById('ov-saved').innerText")
    assert js(qtbot, gui, row("tx-rows", "MCM_SP") + ".querySelector('.tx-attr').value") == "Event"


def test_invalid_entry_is_named_and_nothing_is_saved(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    before = (home / "data" / FILE).read_text(encoding="utf-8")
    js(qtbot, gui, row("rx-rows", "TC_NSM") + ".querySelector('.rx-timeout').value='10ms'; 1")
    navigate(qtbot, gui, SAVE)
    error = js(qtbot, gui, "document.getElementById('ov-error').innerText")
    assert "TC_NSM" in error and "timeout" in error
    assert (home / "data" / FILE).read_text(encoding="utf-8") == before
    assert js(qtbot, gui, row("rx-rows", "TC_NSM") + ".querySelector('.rx-timeout').value") == "10ms"   # entry kept


def test_removing_every_row_saves_no_override(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    js(qtbot, gui, "Array.from(document.querySelectorAll('.ov-remove')).forEach(function (b) { b.click(); });"
                   "document.getElementById('host-prefix').value='';document.getElementById('host-function').value='';"
                   "document.getElementById('numeric-order').value=''; 1")
    navigate(qtbot, gui, SAVE)
    assert saved(home) == {}
    assert js(qtbot, gui, "document.querySelectorAll('#tx-rows tr[data-msg]').length") == 0
