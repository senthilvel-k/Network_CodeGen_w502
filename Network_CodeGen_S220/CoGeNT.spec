# PyInstaller spec: onedir, files beside the exe (matches the old py2exe layout and the
# CWD-relative ./html ./data ./CODE_GEN paths the app uses).
# Build:  .venv\Scripts\pyinstaller --noconfirm --clean CoGeNT.spec --distpath dist_py3 --workpath build_py3
block_cipher = None
datas = [("html", "html"), ("js", "js"), ("style", "style"), ("data", "data"),
         ("batman.ico", "."), ("cogent_gui/bridge.js", "cogent_gui")]
hidden = ["Dbc_Parser", "Can_dbc_gen", "Can_filter_python_gen", "can_rx_filt_gen", "msg",
          "il_par_h_generation", "il_par_c_generation", "vnim_app_signals_par", "cogent_io", "py2compat",
          "cogent_errors", "cogent_generate"]

a = Analysis(["CoGeNT.pyw"], pathex=["."], datas=datas, hiddenimports=hidden,
             excludes=["tkinter", "PySide6.Qt3DCore", "PySide6.QtQuick3D", "PySide6.QtMultimedia"])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="CoGeNT", icon="batman.ico",
          console=False, contents_directory=".")
coll = COLLECT(exe, a.binaries, a.datas, name="CoGeNT")
