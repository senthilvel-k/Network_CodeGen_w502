"""New messages/signals (no saved settings) are announced on the home page, in the sidebar and on the
configuration pages, where 'Next new' and 'Only new' make them easy to find. Tests share one app."""
import json

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert

pytestmark = pytest.mark.gui
FIXTURE = "s2xx_40024"
MSG_LINK = "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()"
SIG_LINK = "document.querySelector('a[href=\"BackEnd.Can_dbc0_sig\"]').click()"
BANNER = "(document.getElementById('cogent-new-banner') || {innerText: 'NO BANNER'}).innerText"


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE, dbc_folder="input DBC 40024")
    data = home / "data"
    msg = json.loads((data / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    sig = json.loads((data / "CanDbcSigConfiguration.data").read_text(encoding="utf-8"))
    (data / "CanDbcMsgConfiguration.data").write_text(
        json.dumps({k: v for k, v in msg.items() if not k.startswith("BMS4_100_")}), encoding="utf-8")
    (data / "CanDbcSigConfiguration.data").write_text(
        json.dumps({k: v for k, v in sig.items() if not k.startswith(NEW_SIGNAL + "_")}), encoding="utf-8")
    yield back_end, home, fx, dbc
    restore()


NEW_SIGNAL = "BMS_OPERATIONMODE"   # a signal of BMS1_10, an enabled application message (its page row id)


def test_home_announces_new_message_and_signal(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert js(qtbot, gui, "document.getElementById('new-banner') === null")      # nothing before Load DBC
    js(qtbot, gui, "document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value='SMART_CORE';"
                   "document.getElementById('form_submit').click(); 1" % json.dumps(dbc.as_posix()))
    wait_alert(qtbot, gui, "Database loaded successfully")
    settle(qtbot, gui)
    banner = js(qtbot, gui, "document.getElementById('new-banner').innerText")
    assert "1 message (BMS4_100)" in banner and "1 signal" in banner
    assert "1 new" in js(qtbot, gui, "document.getElementById('nav-messages').innerText")
    assert "1 new" in js(qtbot, gui, "document.getElementById('nav-signals').innerText")


def test_message_page_banner_next_and_only_new(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, MSG_LINK)
    assert "1 new message" in js(qtbot, gui, BANNER)
    js(qtbot, gui, "document.getElementById('cogent-next-new').click(); 1")
    assert js(qtbot, gui, "document.querySelector('tr.cogent-current').id") == "BMS4_100"
    js(qtbot, gui, "document.getElementById('cogent-only-new').click(); 1")
    visible = "Array.from(document.querySelectorAll('#rx_table tr, #tx_table tr')).filter(function (r) { return r.id && r.style.display !== 'none'; }).length"
    assert js(qtbot, gui, visible) == 1
    js(qtbot, gui, "document.getElementById('cogent-only-new').click(); 1")
    assert js(qtbot, gui, visible) > 100


def test_signal_page_banner(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.default_page()")
    fx = app[2]
    navigate(qtbot, gui, MSG_LINK)
    navigate(qtbot, gui, "BackEnd.Can_dbc_msg_SaveButton(%s)" % json.dumps((fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8")))
    navigate(qtbot, gui, SIG_LINK)
    assert "1 new signal" in js(qtbot, gui, BANNER)
    js(qtbot, gui, "document.getElementById('cogent-next-new').click(); 1")
    assert js(qtbot, gui, "document.querySelector('tr.cogent-current').id") == NEW_SIGNAL


def test_signal_page_applies_the_notification_to_new_rows(qtbot, app):
    gui = app[0].app                                      # still on the signal page of the test above
    before = js(qtbot, gui, "document.getElementById('VIN_INDEX_os_notify_no_of_events').value")
    js(qtbot, gui, "document.getElementById('cogent-new-notify').value = '200ms_Delay_g2';"
                   "document.getElementById('cogent-apply-notify').click(); 1")
    assert js(qtbot, gui, "document.getElementById('%s_os_notify_no_of_events').value" % NEW_SIGNAL) == "200ms_Delay_g2"
    assert js(qtbot, gui, "document.getElementById('VIN_INDEX_os_notify_no_of_events').value") == before


def test_saving_clears_the_announcement(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, "BackEnd.Can_dbc0_sig_SaveButton(%s)" % json.dumps((fx.data_dir / "CanDbcSigConfiguration.data").read_text(encoding="utf-8")))
    assert js(qtbot, gui, "document.getElementById('new-banner') === null")
    navigate(qtbot, gui, MSG_LINK)
    assert "No new messages" in js(qtbot, gui, BANNER)


def test_banner_save_button_saves_the_page(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, MSG_LINK)
    navigate(qtbot, gui, "document.getElementById('cogent-save').click()")
    assert gui.template[0] == "Tool_Index_Page.html"            # Save and Back returns to the home page
