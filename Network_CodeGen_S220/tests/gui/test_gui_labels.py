"""Labels, titles and layout of every page: correct spelling, the CoGeNT sidebar on the configuration
pages, no leftovers of the legacy labels. Tests share one app."""
import json

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert

pytestmark = pytest.mark.gui
FIXTURE = "s237_36144_2"
BAD = ["cofiguration", "Timout", "Messsage", "byte_order", "Byte_order", "Browse ..", "+ TX/R",
       "run code gen", "running code gen", "code gen "]   # "code generator" is fine
TEXT = "document.body.innerText"


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE)
    yield back_end, home, fx, dbc
    restore()


def no_bad_words(qtbot, gui):
    text = js(qtbot, gui, TEXT)
    values = js(qtbot, gui, "Array.from(document.querySelectorAll('input[type=button],input[type=submit]'))"
                            ".map(function (b) { return b.value; }).join('|')")
    found = [w for w in BAD if w in text or w in values]
    assert found == [], found


def test_home_page_labels(qtbot, app):
    back_end, home, fx, dbc = app
    gui = back_end.app
    navigate(qtbot, gui, "BackEnd.default_page()")
    assert js(qtbot, gui, "document.title") == "CoGeNT - Home"
    values = js(qtbot, gui, "Array.from(document.querySelectorAll('input[type=button],input[type=submit]'))"
                            ".map(function (b) { return b.value; }).join('|')")
    assert values == "Browse|Load DBC|Generate code|Save configuration|Load configuration"
    no_bad_words(qtbot, gui)
    js(qtbot, gui, "document.getElementById('file_path').value=%s;document.getElementById('ch0_node_name').value=%s;"
                   "document.getElementById('form_submit').click(); 1" % (json.dumps(dbc.as_posix()), json.dumps(fx.node)))
    wait_alert(qtbot, gui, "Database loaded successfully")
    settle(qtbot, gui)


@pytest.mark.parametrize("link, title, wanted", [
    ("BackEnd.Can_dbc0_msg", "CoGeNT - TX/RX messages", "Message Timeout ID"),
    ("BackEnd.Can_dbc0_sig", "CoGeNT - TX/RX signals", "Byte order"),
])
def test_configuration_pages_have_the_cogent_layout_and_labels(qtbot, app, link, title, wanted):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.default_page()")
    navigate(qtbot, gui, "document.querySelector('a[href=\"%s\"]').click()" % link)
    assert js(qtbot, gui, "document.title") == title
    assert wanted in js(qtbot, gui, TEXT)
    assert js(qtbot, gui, "document.querySelectorAll('.cg-side #nav-fifo').length") == 1      # CoGeNT sidebar
    assert js(qtbot, gui, "document.querySelectorAll('.w3-sidenav').length") == 0            # legacy sidebar gone
    no_bad_words(qtbot, gui)
    fx = app[2]
    name = "CanDbcMsgConfiguration.data" if link.endswith("msg") else "CanDbcSigConfiguration.data"
    slot = "BackEnd.Can_dbc_msg_SaveButton" if link.endswith("msg") else "BackEnd.Can_dbc0_sig_SaveButton"
    navigate(qtbot, gui, "%s(%s)" % (slot, json.dumps((fx.data_dir / name).read_text(encoding="utf-8"))))


def test_filter_page_labels(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.Can_Filter()")
    assert js(qtbot, gui, "document.title") == "CoGeNT - Filter"
    assert "Message Type" in js(qtbot, gui, TEXT)
    no_bad_words(qtbot, gui)
    navigate(qtbot, gui, "BackEnd.default_page()")


@pytest.mark.parametrize("slot, title", [("BackEnd.fifo_page()", "CoGeNT - Receive FIFO"),
                                         ("BackEnd.reapply_page()", "CoGeNT - Re-apply edits")])
def test_new_pages_labels(qtbot, app, slot, title):
    gui = app[0].app
    navigate(qtbot, gui, slot)
    assert js(qtbot, gui, "document.title") == title
    no_bad_words(qtbot, gui)


def test_back_button_shows_the_home_page_with_its_cards(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "BackEnd.BackButton('{}')")
    assert js(qtbot, gui, "document.getElementById('fifo-total') !== null")


def test_help_page_shows_the_user_guide_with_contents(qtbot, app):
    gui = app[0].app
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.help_page\"]').click()")
    assert js(qtbot, gui, "document.title") == "CoGeNT - Help"
    assert "CoGeNT user guide" in js(qtbot, gui, "document.getElementById('help-text').innerText")
    toc = js(qtbot, gui, "document.getElementById('help-toc').innerText")
    assert "Receive FIFO" in toc and "Re-apply edits" in toc and "Error messages" in toc
    assert js(qtbot, gui, "document.querySelectorAll('#help-text table').length") >= 5
    no_bad_words(qtbot, gui)
