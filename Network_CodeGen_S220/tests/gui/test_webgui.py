import json
import sys

import pytest
from PySide6.QtCore import QObject, Slot

from support import ROOT

sys.path.insert(0, str(ROOT))

pytestmark = pytest.mark.gui

from cogent_gui import webgui  # noqa: E402


class Probe(QObject):
    def __init__(self):
        super().__init__()
        self.calls = []

    @Slot()
    def ping(self):
        self.calls.append(("ping",))

    @Slot(str)
    def got(self, value):
        self.calls.append(("got", value))


def js(qtbot, gui, expr):
    box = []
    gui.page.runJavaScript(expr, 0, box.append)
    qtbot.waitUntil(lambda: bool(box), timeout=10000)
    return box[0]


def wait_js_true(qtbot, gui, expr, timeout=20000):
    state = {"ok": False}

    def poll():
        gui.page.runJavaScript(expr, 0, lambda r: state.__setitem__("ok", r is True))
        return state["ok"]

    qtbot.waitUntil(poll, timeout=timeout)


@pytest.fixture
def gui(qtbot, tmp_path):
    g = webgui.AppGUI(title="T")
    g.template_path = str(tmp_path)
    g.static_path = str(tmp_path)
    g.alert_handler = lambda msg: None
    probe = Probe()
    g.bind(probe, "Probe")
    g.probe = probe
    g.tmp = tmp_path
    qtbot.addWidget(g.window)
    return g


def show(qtbot, gui, name, html):
    (gui.tmp / name).write_text(html, encoding="utf-8")
    with qtbot.waitSignal(gui.page.loadFinished, timeout=20000):
        gui.template = (name, {})
    wait_js_true(qtbot, gui, "window.__cogentReady === true")


def test_link_calls_slot_with_params(qtbot, gui):
    show(qtbot, gui, "a.html", '<body><a id="l" href="Probe.got" data-bind="true" data-params="x1">go</a></body>')
    js(qtbot, gui, "document.getElementById('l').click(); 1")
    qtbot.waitUntil(lambda: ("got", "x1") in gui.probe.calls)


def test_call_before_channel_ready_is_queued(qtbot, gui):
    show(qtbot, gui, "b.html", '<body onload="Probe.ping()">x</body>')
    qtbot.waitUntil(lambda: ("ping",) in gui.probe.calls)


def test_form_submit_preserves_backslashes_and_quotes(qtbot, gui):
    show(qtbot, gui, "c.html", '<body><form id="f" action="Probe.got" data-bind="true">'
         '<input name="ch0_file" id="p"><input type="submit" id="s"></form></body>')
    path = "D:\\DBC\\U321 it's.dbc"
    js(qtbot, gui, f"document.getElementById('p').value={json.dumps(path)};document.getElementById('s').click();1")
    qtbot.waitUntil(lambda: any(c[0] == "got" for c in gui.probe.calls))
    payload = [c[1] for c in gui.probe.calls if c[0] == "got"][0]
    assert json.loads(payload) == {"ch0_file": path}


def test_form_checkbox_values_follow_checked_state_like_qtwebkit(qtbot, gui):
    """QtWebKit (Qt 4.8) returned checked ? "on" : "" for a checkbox without a value attribute;
    the saved .data files depend on it (Chromium would always return "on")."""
    show(qtbot, gui, "g.html", '<body><form action="Probe.got" data-bind="true">'
         '<input type="checkbox" name="a" id="a"><input type="checkbox" name="b" id="b">'
         '<input type="checkbox" name="c" value="x"><input type="submit" id="s"></form></body>')
    js(qtbot, gui, "document.getElementById('a').checked=true; document.getElementById('s').click(); 1")
    qtbot.waitUntil(lambda: any(c[0] == "got" for c in gui.probe.calls))
    payload = [c[1] for c in gui.probe.calls if c[0] == "got"][0]
    assert payload == '{"a":"on","b":"","c":"x"}'


def test_template_larger_than_2mb_loads(qtbot, gui):
    show(qtbot, gui, "big.html", "<body>" + "<p>x</p>" * 450_000 + '<div id="end">e</div></body>')
    assert js(qtbot, gui, "document.getElementById('end') !== null") is True


def test_evaluate_javascript_after_template_targets_new_page(qtbot, gui):
    (gui.tmp / "d.html").write_text('<body><input id="v"></body>', encoding="utf-8")
    with qtbot.waitSignal(gui.page.loadFinished, timeout=20000):
        gui.template = ("d.html", {})
        gui.evaluate_javascript("document.getElementById('v').value='set';")
    wait_js_true(qtbot, gui, "document.getElementById('v').value === 'set'")


def test_alert_is_recorded(qtbot, gui):
    show(qtbot, gui, "e.html", "<body>x</body>")
    gui.evaluate_javascript("alert('hello')")
    qtbot.waitUntil(lambda: "hello" in gui.alerts)


def test_rendered_pages_temp_dir_is_removed_when_app_exits(tmp_path):
    """Each launch renders pages (up to ~4 MB) into a temp folder; it must not accumulate."""
    import os
    import subprocess
    (tmp_path / "p.html").write_text("<body>x</body>", encoding="utf-8")
    script = (
        "import sys; sys.path.insert(0, sys.argv[1])\n"
        "from PySide6.QtCore import QTimer\n"
        "from cogent_gui import webgui\n"
        "g = webgui.AppGUI(title='T'); g.template_path = sys.argv[2]\n"
        "g.page.loadFinished.connect(lambda ok: QTimer.singleShot(0, g.qt_app.quit))\n"
        "g.template = ('p.html', {})\n"
        "print(g._render_dir, flush=True)\n"
        "g.start()\n")
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu")
    r = subprocess.run([sys.executable, "-c", script, str(ROOT), str(tmp_path)], capture_output=True,
                       text=True, timeout=120, env=env)
    assert r.returncode == 0, r.stderr[-2000:]
    render_dir = r.stdout.strip().splitlines()[0]
    assert os.path.basename(render_dir).startswith("cogent_render_")
    assert not os.path.exists(render_dir)


def test_staticfile_filter_points_to_static_path(qtbot, gui):
    (gui.tmp / "s.css").write_text("#m{width:123px}", encoding="utf-8")
    show(qtbot, gui, "f.html", '<link rel="stylesheet" href="{{\'s.css\'|staticfile}}"><body><div id="m"></div></body>')
    assert js(qtbot, gui, "getComputedStyle(document.getElementById('m')).width") == "123px"
