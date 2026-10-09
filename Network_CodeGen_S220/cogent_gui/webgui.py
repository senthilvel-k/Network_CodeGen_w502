"""Minimal htmlPy-compatible layer on PySide6 QtWebEngine + QWebChannel."""
import json
import os
import sys
import tempfile

import jinja2
from PySide6.QtCore import QFile, QIODevice, QObject, Qt, QUrl, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineScript, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow

Object = QObject
__all__ = ["Object", "Slot", "AppGUI", "settings"]

_BRIDGE_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge.js")


class settings:
    DISABLE = 0
    ENABLE = 1


def _read_qrc(path):
    f = QFile(path)
    if not f.open(QIODevice.OpenModeFlag.ReadOnly):
        raise RuntimeError("cannot open " + path)
    try:
        return bytes(f.readAll()).decode("utf-8")
    finally:
        f.close()


class _Page(QWebEnginePage):
    def __init__(self, gui, parent):
        super().__init__(parent)
        self._gui = gui

    def javaScriptAlert(self, url, msg):
        self._gui.alerts.append(msg)
        if self._gui.alert_handler is not None:
            self._gui.alert_handler(msg)
        else:
            super().javaScriptAlert(url, msg)

    def javaScriptConsoleMessage(self, level, message, line, source):
        self._gui.console.append((message, line, source))


class AppGUI:
    def __init__(self, title="", maximized=False):
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.web_app = QWebEngineView(self.window)
        self.page = _Page(self, self.web_app)
        self.web_app.setPage(self.page)
        self.window.setCentralWidget(self.web_app)
        web_settings = self.page.settings()
        web_settings.setDefaultTextEncoding("utf-8")
        web_settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.channel = QWebChannel(self.page)
        self.page.setWebChannel(self.channel)
        self.page.loadFinished.connect(self._on_load_finished)
        self.maximized = maximized
        self.template_path = "."
        self.static_path = "."
        self.allow_overwrite = True
        self.alerts = []
        self.console = []
        self.alert_handler = None
        self._template = None
        self._objects = {}
        self._loading = False
        self._pending_js = []
        # Removed automatically at interpreter exit (rendered pages can be several MB).
        self._render_tmp = tempfile.TemporaryDirectory(prefix="cogent_render_", ignore_cleanup_errors=True)
        self._render_dir = self._render_tmp.name

    def bind(self, obj, variable_name=None):
        name = variable_name or type(obj).__name__
        old = self._objects.get(name)
        if old is not None:
            self.channel.deregisterObject(old)
        self.channel.registerObject(name, obj)
        self._objects[name] = obj
        self._install_bridge()

    def _install_bridge(self):
        scripts = self.page.scripts()
        for old in scripts.find("cogent-bridge"):
            scripts.remove(old)
        with open(_BRIDGE_JS, encoding="utf-8") as fh:
            bridge = fh.read()
        source = (_read_qrc(":/qtwebchannel/qwebchannel.js")
                  + "\nwindow.__cogentObjects = " + json.dumps(sorted(self._objects)) + ";\n"
                  + bridge)
        script = QWebEngineScript()
        script.setName("cogent-bridge")
        script.setSourceCode(source)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(False)
        scripts.insert(script)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template_tuple):
        name, context = template_tuple
        static_path = self.static_path
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_path))
        env.filters["staticfile"] = lambda p: QUrl.fromLocalFile(os.path.join(static_path, p)).toString()
        html = env.get_template(name).render(**context)
        target = os.path.join(self._render_dir, name)
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(html)
        self._template = template_tuple
        self._loading = True
        self._pending_js = []
        self.web_app.load(QUrl.fromLocalFile(target))

    def _on_load_finished(self, ok):
        self._loading = False
        pending, self._pending_js = self._pending_js, []
        for source in pending:
            self.page.runJavaScript(source, QWebEngineScript.ScriptWorldId.MainWorld)

    def evaluate_javascript(self, javascript_string):
        if self._loading:
            self._pending_js.append(javascript_string)
        else:
            self.page.runJavaScript(javascript_string, QWebEngineScript.ScriptWorldId.MainWorld)

    def right_click_setting(self, value):
        policy = (Qt.ContextMenuPolicy.NoContextMenu if value == settings.DISABLE
                  else Qt.ContextMenuPolicy.DefaultContextMenu)
        self.web_app.setContextMenuPolicy(policy)

    def start(self):
        if self.maximized:
            self.window.showMaximized()
        else:
            self.window.show()
        return self.qt_app.exec()
