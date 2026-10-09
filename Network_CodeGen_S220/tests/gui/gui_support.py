"""Shared helpers for the in-process GUI tests (real back_end pages in QtWebEngine)."""
import importlib
import time
import os
import shutil
import sys

from support import ROOT, load_fixture

APP_ITEMS = ["CoGeNT.pyw", "back_end.py", "Dbc_Parser.py", "Can_dbc_gen.py", "Can_filter_python_gen.py",
             "can_rx_filt_gen.py", "msg.py", "il_par_h_generation.py", "il_par_c_generation.py",
             "vnim_app_signals_par.py", "cogent_io.py", "cogent_errors.py", "cogent_generate.py", "cogent_fifo.py",
             "py2compat.py", "batman.ico", "cogent_gui", "html", "js", "style"]
APP_MODULES = ("back_end", "Dbc_Parser", "py2compat", "cogent_io", "cogent_errors", "cogent_generate", "cogent_fifo",
               "Can_dbc_gen", "Can_filter_python_gen", "can_rx_filt_gen", "msg", "il_par_h_generation",
               "il_par_c_generation", "vnim_app_signals_par")


def start_app_copy(tmp_path_factory, fixture_name, dbc_folder="input DBC files"):
    """Copy the app into a folder with spaces, chdir there, import back_end. Returns
    (back_end, home, fixture, dbc_path, restore)."""
    home = tmp_path_factory.mktemp("gui") / "CoGeNT app copy & spaces"
    home.mkdir()
    for item in APP_ITEMS:
        src = ROOT / item
        (shutil.copytree if src.is_dir() else shutil.copyfile)(src, home / item)
    fx = load_fixture(fixture_name)
    shutil.copytree(fx.data_dir, home / "data")
    dbc_dir = home / dbc_folder
    dbc_dir.mkdir()
    shutil.copyfile(fx.dbc, dbc_dir / fx.dbc.name)
    old_cwd, old_path = os.getcwd(), list(sys.path)
    os.chdir(home)
    sys.path.insert(0, str(home))
    for mod in APP_MODULES:
        sys.modules.pop(mod, None)
    back_end = importlib.import_module("back_end")
    back_end.app.alert_handler = lambda msg: None

    def restore():
        back_end.app.window.close()
        os.chdir(old_cwd)
        sys.path[:] = old_path

    return back_end, home, fx, dbc_dir / fx.dbc.name, restore


def js(qtbot, gui, expr, timeout=180000):
    """Evaluate expr in the page. The result arrives only after any slot it triggered has
    returned (slots run on the GUI thread), e.g. ~20 s for code generation of a large DBC."""
    box = []
    gui.page.runJavaScript(expr, 0, box.append)
    qtbot.waitUntil(lambda: bool(box), timeout=timeout)
    return box[0]


def wait_ready(qtbot, gui, timeout=20000):
    state = {"ok": False}

    def poll():
        gui.page.runJavaScript("window.__cogentReady === true", 0,
                               lambda r: state.__setitem__("ok", r is True))
        return state["ok"]

    qtbot.waitUntil(poll, timeout=timeout)


def navigate(qtbot, gui, click_expr, timeout=180000):
    with qtbot.waitSignal(gui.page.loadFinished, timeout=timeout):
        js(qtbot, gui, click_expr + "; 1")
    wait_ready(qtbot, gui)


def wait_alert(qtbot, gui, text, timeout=180000):
    qtbot.waitUntil(lambda: any(text in a for a in gui.alerts), timeout=timeout)
    return [a for a in gui.alerts if text in a][-1]


def settle(qtbot, gui, quiet_ms=2000, timeout=300):
    """Wait until every slot triggered so far has finished and shown its popups: no page load
    pending and no new popup for quiet_ms. A slot blocks the GUI thread while it runs (code gen
    ~20 s), so a wait that returns late counts as activity and restarts the quiet period."""
    deadline = time.time() + timeout
    last = (len(gui.alerts), gui._loading)
    stable_since = time.time()
    while time.time() < deadline:
        before = time.time()
        qtbot.wait(100)
        now = (len(gui.alerts), gui._loading)
        if now != last or time.time() - before > 0.5:
            last, stable_since = now, time.time()
        elif not gui._loading and (time.time() - stable_since) * 1000 >= quiet_ms:
            return
    raise AssertionError("GUI did not settle within %d s" % timeout)
