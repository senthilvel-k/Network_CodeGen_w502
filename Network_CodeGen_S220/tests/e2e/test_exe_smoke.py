"""Windows GUI end-to-end test of the packaged exe (PyInstaller onedir in dist_py3/CoGeNT).

The real CoGeNT.exe runs as a separate process. Native Qt windows and the JavaScript alert
dialogs are found and dismissed through Windows UI Automation (pywinauto). Web content is
driven through the Chrome DevTools Protocol on 127.0.0.1, because QtWebEngine's UI Automation
bridge exposes page elements read-only (ValuePattern.SetValue / Invoke do nothing), and real
mouse/keyboard simulation would interfere with the user's desktop session.

Flow: Load DBC -> TX/RX message page -> Save and Back -> signal page -> Save and Back ->
code gen -> CODE_GEN compared with the known-good legacy run."""
import json
import os
import shutil
import socket
import time
import urllib.request

import pytest

from support import CODE_FILES, LEGACY_REFS, ROOT, load_fixture, normalize_header

pywinauto = pytest.importorskip("pywinauto")
websocket = pytest.importorskip("websocket")
from pywinauto import Application  # noqa: E402

pytestmark = pytest.mark.e2e
EXE_DIR = ROOT / "dist_py3" / "CoGeNT"
# s2xx_40024: the real "_Edited" 40024 DBC with the configuration saved in CODE_GEN/DBC_40024_2
FIXTURES = ["s237_36144_2", "s2xx_40024"]
# 40024 needs 209 receive rules without merging; with the merges of the S2XX workspace it needs 184.
FIFO_CONFIGS = {"s2xx_40024": {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
                               "additional_rx_messages": ["BMS19_100", "BMS20_100"]}}
FIFO_FILES = ["can_rxrule.cfg", "nw_can_dll.h"]


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Cdp:
    """Minimal Chrome DevTools Protocol client for the QtWebEngine page target."""

    def __init__(self, port, timeout=120):
        deadline = time.time() + timeout
        while True:
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=5))
                page = next(t for t in targets if t.get("type") == "page")
                break
            except Exception:
                if time.time() > deadline:
                    raise
                time.sleep(1)
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60)
        self.next_id = 0

    def eval(self, expression):
        self.next_id += 1
        self.ws.send(json.dumps({"id": self.next_id, "method": "Runtime.evaluate",
                                 "params": {"expression": expression, "returnByValue": True}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.next_id:
                return msg.get("result", {}).get("result", {}).get("value")

    def wait(self, expression, timeout=300):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if self.eval(expression) is True:
                    return
            except Exception:
                pass
            time.sleep(0.5)
        raise AssertionError(f"timed out waiting for: {expression}")

    def close(self):
        self.ws.close()


def _dismiss_alert(main_window, text, timeout=300):
    """Find the native "Javascript Alert" dialog (UIA lists it as an owned window under the
    CoGeNT main window), check its text, press OK through UIA Invoke."""
    deadline = time.time() + timeout
    seen = []
    while time.time() < deadline:
        dialog = main_window.child_window(title_re="^Javascript Alert", control_type="Window")
        if dialog.exists(timeout=1):
            texts = [c.window_text() for c in dialog.descendants()]
            seen.append(texts)
            if any(text in t for t in texts):
                ok = [b for b in dialog.descendants(control_type="Button") if b.window_text().replace("&", "") == "OK"]
                ok[0].invoke()
                return
        time.sleep(0.5)
    raise AssertionError(f"alert containing {text!r} not seen; dialogs seen: {seen[-3:]}")


def _on_page(cdp, page_name):
    cdp.wait(f"location.href.endsWith('/{page_name}') && window.__cogentReady === true")


@pytest.mark.parametrize("fixture_name", FIXTURES)
def test_exe_generates_code_like_legacy(tmp_path, fixture_name):
    if not (EXE_DIR / "CoGeNT.exe").exists():
        pytest.skip("build first: pyinstaller CoGeNT.spec --distpath dist_py3 --workpath build_py3")
    home = tmp_path / "CoGeNT exe copy"
    shutil.copytree(EXE_DIR, home)
    fx = load_fixture(fixture_name)
    shutil.rmtree(home / "data")                    # the fixture's data folder is the whole project configuration
    shutil.copytree(fx.data_dir, home / "data")
    if fixture_name in FIFO_CONFIGS:
        (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps(FIFO_CONFIGS[fixture_name]), encoding="utf-8")
    dbc = tmp_path / "input DBC" / fx.dbc.name
    dbc.parent.mkdir()
    shutil.copyfile(fx.dbc, dbc)
    port = _free_port()
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = f"127.0.0.1:{port}"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
    app = Application(backend="uia").start(f'"{home / "CoGeNT.exe"}"', work_dir=str(home), timeout=60)
    cdp = None
    try:
        win = app.window(title="CoGeNT")
        win.wait("visible ready", timeout=120)
        assert win.is_maximized()
        cdp = Cdp(port)
        _on_page(cdp, "Tool_Index_Page.html")

        cdp.eval(f"document.getElementById('file_path').value={json.dumps(dbc.as_posix())};"
                 f"document.getElementById('ch0_node_name').value={json.dumps(fx.node)};"
                 "document.getElementById('form_submit').click(); true")
        _dismiss_alert(win, "Database loaded successfully")

        for link, page in (("BackEnd.Can_dbc0_msg", "CAN_DBC_msg.html"), ("BackEnd.Can_dbc0_sig", "CAN_DBC_sig.html")):
            cdp.eval(f"document.querySelector('a[href=\"{link}\"]').click(); true")
            _on_page(cdp, page)
            cdp.eval("document.getElementById('form_submit').click(); true")   # "Save and Back"
            _on_page(cdp, "Tool_Index_Page.html")

        cdp.eval("document.querySelector('input[name=code_generate]').click(); true")
        _dismiss_alert(win, "Code Generated in CODE_GEN folder")
        assert not (home / "CODE_GEN" / "errorlog.txt").exists()
        legacy_dir = LEGACY_REFS[fixture_name][0]
        for name in CODE_FILES:
            assert (home / "CODE_GEN" / name).stat().st_size > 0, name
            if fixture_name in FIFO_CONFIGS and name in FIFO_FILES:
                continue                            # merged ID blocks: checked against the plan below
            assert normalize_header((home / "CODE_GEN" / name).read_bytes()) == \
                normalize_header((legacy_dir / name).read_bytes()), name
        plan = json.loads((home / "CODE_GEN" / "fifo_plan.json").read_text(encoding="utf-8"))
        assert plan["total_rules"] <= 192
        assert (home / "CODE_GEN" / "MANUAL_ACTIONS.md").exists()
        if fixture_name in FIFO_CONFIGS:
            assert plan["fifo_counts"] == [64, 64, 56]
    finally:
        if cdp:
            cdp.close()
        app.kill()
        os.environ.pop("QTWEBENGINE_REMOTE_DEBUGGING", None)
