"""Receive FIFO in the GUI: the home card, the Receive FIFO page (pre-selection, live preview, Apply)
and the code-gen messages that point to it. Real 40024 DBC + CODE_GEN/DBC_40024_2 configuration
(209 receive rules without merging). Tests run in file order and share one app."""
import json

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert

pytestmark = pytest.mark.gui
FIXTURE = "s2xx_40024"
FIFO_FILE = "CanFifoConfiguration.data"
CARD = "document.getElementById('fifo-card').innerText"
TOTAL = "document.getElementById('fifo-total').innerText"
FIFO_LINK = "document.querySelector('a[href=\"BackEnd.fifo_page\"]').click()"
CODE_GEN_BTN = "document.querySelector('input[name=code_generate]').click()"


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE, dbc_folder="input DBC 40024")
    yield back_end, home, fx, dbc
    restore()


def wait_js(qtbot, gui, expr, expected, timeout=20000):
    seen = {}

    def check():
        seen["v"] = js(qtbot, gui, expr)
        return seen["v"] == expected
    try:
        qtbot.waitUntil(check, timeout=timeout)
    except AssertionError:
        raise AssertionError("%s: expected %r, got %r" % (expr, expected, seen.get("v")))


def load_dbc(qtbot, gui, dbc, node):
    gui.alerts.clear()
    js(qtbot, gui, "document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value=%s;"
                   "document.getElementById('form_submit').click(); 1" % (json.dumps(dbc.as_posix()), json.dumps(node)))
    wait_alert(qtbot, gui, "Database loaded successfully")
    settle(qtbot, gui)


def test_card_asks_to_load_a_dbc_first(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert "Load a DBC" in js(qtbot, gui, CARD)


def test_card_shows_overflow_after_load_dbc(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    load_dbc(qtbot, gui, dbc, fx.node)
    card = js(qtbot, gui, CARD)
    assert js(qtbot, gui, TOTAL) == "209"
    assert "17 rules over the limit" in card and "Receive FIFO" in card
    assert js(qtbot, gui, "document.querySelectorAll('#fifo-card .cg-bar').length") == 3


def test_fifo_page_preselects_the_blocks_needed(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, FIFO_LINK)
    assert gui.template[0] == "Fifo.html"
    checked = js(qtbot, gui, "Array.from(document.querySelectorAll('input.cand:checked'))"
                             ".map(function (c) { return c.dataset.label; }).join(',')")   # arrays do not cross runJavaScript
    assert checked == "0x4F0-0x4FF,0x3D0-0x3DF"
    wait_js(qtbot, gui, TOTAL, "182")
    assert "Fits" in js(qtbot, gui, "document.getElementById('fifo-state').innerText")


def test_unticking_a_block_updates_the_preview(qtbot, app):
    gui = app[0].app
    js(qtbot, gui, "document.querySelector('input.cand[data-label=\"0x3D0-0x3DF\"]').click(); 1")
    wait_js(qtbot, gui, TOTAL, "194")
    assert "2 rules over the limit" in js(qtbot, gui, "document.getElementById('fifo-state').innerText")
    js(qtbot, gui, "document.querySelector('input.cand[data-label=\"0x3D0-0x3DF\"]').click(); 1")
    wait_js(qtbot, gui, TOTAL, "182")


def test_invalid_block_by_id_is_explained_on_the_page(qtbot, app):
    gui = app[0].app
    js(qtbot, gui, "document.getElementById('add-base').value='0x3D1'; document.getElementById('add-block').click(); 1")
    wait_js(qtbot, gui, "document.getElementById('add-error').innerText.indexOf('not aligned') >= 0", True)
    wait_js(qtbot, gui, TOTAL, "182")          # the rejected block is not part of the proposal


def test_apply_saves_and_returns_to_a_fitting_home_card(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, "document.getElementById('fifo-apply').click()")
    assert gui.template[0] == "Tool_Index_Page.html"
    assert js(qtbot, gui, TOTAL) == "182"
    assert "Fits" in js(qtbot, gui, CARD)
    saved = json.loads((home / "data" / FIFO_FILE).read_text(encoding="utf-8"))
    assert saved["merge_blocks"] == [{"base": "0x4F0", "mask": "0x7F0"}, {"base": "0x3D0", "mask": "0x7F0"}]


def test_generate_code_after_apply(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    for link, save in (("BackEnd.Can_dbc0_msg", "BackEnd.Can_dbc_msg_SaveButton"), ("BackEnd.Can_dbc0_sig", "BackEnd.Can_dbc0_sig_SaveButton")):
        navigate(qtbot, gui, "document.querySelector('a[href=\"%s\"]').click()" % link)
        name = "CanDbcMsgConfiguration.data" if "msg" in save else "CanDbcSigConfiguration.data"
        navigate(qtbot, gui, "%s(%s)" % (save, json.dumps((fx.data_dir / name).read_text(encoding="utf-8"))))
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    text = wait_alert(qtbot, gui, "Code generated in CODE_GEN")
    assert "182 of 192" in text and "Manual action required" in text
    settle(qtbot, gui)


def test_home_shows_the_last_generation_and_opens_it(qtbot, app, monkeypatch):
    from support import latest_run
    back_end, home, fx, dbc = app
    gui = back_end.app
    run = latest_run(home)
    assert (run / (run.name + ".cfg")).is_file() and (run / "app.host.manager" / "nw_host_mgr_txrx.resource").is_file()
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert ("CODE_GEN\\" + run.name) in js(qtbot, gui, "document.getElementById('last-run').innerText")
    opened = []
    monkeypatch.setattr(back_end.os, "startfile", opened.append, raising=False)
    js(qtbot, gui, "document.getElementById('open-last-run').click(); 1")
    qtbot.waitUntil(lambda: opened == [str(run)], timeout=10000)


def test_overflow_at_code_gen_is_short_and_points_to_receive_fifo(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / FIFO_FILE).write_text("{}", encoding="utf-8")
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    text = wait_alert(qtbot, gui, "Code generation failed")
    assert "209 CAN receive rules are needed" in text and "accepts 192" in text
    assert "Receive FIFO" in text and "Apply" in text
    assert "these do not fit" not in text and len(text) < 500
    assert "these do not fit" in (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")
    settle(qtbot, gui)


def test_flagged_block_at_code_gen_points_to_receive_fifo(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / FIFO_FILE).write_text(json.dumps({"merge_blocks": [{"base": "0x000", "mask": "0x7F0"}]}), encoding="utf-8")
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert "0x000-0x00F" in js(qtbot, gui, CARD)
    gui.alerts.clear()
    navigate(qtbot, gui, CODE_GEN_BTN)
    text = wait_alert(qtbot, gui, "Code generation failed")
    assert "0x000-0x00F" in text and "Receive FIFO" in text
    settle(qtbot, gui)


def test_card_counts_messages_without_saved_settings(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    (home / "data" / FIFO_FILE).unlink()
    msg = json.loads((home / "data" / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    trimmed = {k: v for k, v in msg.items() if not k.startswith("VCU5_500_")}
    (home / "data" / "CanDbcMsgConfiguration.data").write_text(json.dumps(trimmed), encoding="utf-8")
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert js(qtbot, gui, TOTAL) == "208"
    assert "1 message has no saved settings" in js(qtbot, gui, CARD)
    (home / "data" / "CanDbcMsgConfiguration.data").write_text(json.dumps(msg), encoding="utf-8")


def test_receive_only_message_can_be_added_and_removed(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, FIFO_LINK)
    wait_js(qtbot, gui, TOTAL, "182")                       # blocks pre-selected on opening
    js(qtbot, gui, "document.getElementById('ro-select').value='BMS19_100'; document.getElementById('ro-add').click(); 1")
    wait_js(qtbot, gui, TOTAL, "183")
    assert "BMS19_100" in js(qtbot, gui, "document.getElementById('ro-list').innerText")
    js(qtbot, gui, "document.querySelector('.ro-remove[data-name=\"BMS19_100\"]').click(); 1")
    wait_js(qtbot, gui, TOTAL, "182")
    assert "BMS19_100" not in js(qtbot, gui, "document.getElementById('ro-list').innerText")
