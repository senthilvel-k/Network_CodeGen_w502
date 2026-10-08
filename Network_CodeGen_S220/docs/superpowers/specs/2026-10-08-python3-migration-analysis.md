# CoGeNT (Network_CodeGen_S220): Python 2.7 to Python 3 migration analysis

Date: 2026-10-08. Status: analysis only. No application source has been changed.

## 1. Environment check (this machine)

| Tool | Found | Notes |
|---|---|---|
| Git | **2.56.0.windows.2** (`C:\Program Files\Git\cmd\git.exe`) | OK. The project folder is **not** a Git repository yet. |
| Python (PATH `python`) | **3.12.10** 64-bit, Microsoft Store build (`...\WindowsApps\PythonSoftwareFoundation.Python.3.12_...`) | Usable, but the Store sandbox redirects AppData writes. A python.org build is recommended for venv and PyInstaller work. |
| Python (`py` launcher) | **3.14** 64-bit (`...\AppData\Local\Python\pythoncore-3.14-64`), plus the 3.12 Store build | Python install manager is present. |
| Python 2.7 | **Not installed.** `venv\pyvenv.cfg` points to `C:\Python27\python.exe`, which does not exist. | The bundled `venv\` (virtualenv 20.13, 2.7.18, **x64**) is broken. |
| Packages in `venv\` | htmlPy 2.0.3, PySide 1.2.4 (Qt 4.8 + QtWebKit), pip 20.3.4 | **Jinja2 is missing** (htmlPy requires `Jinja2>=2.6`), so `import htmlPy` fails even after Python 2.7 is restored. |
| Global 3.12 packages | Jinja2 3.1.6, MarkupSafe 3.0.4, cantools 44.2.1, xlrd 2.0.2, PyQt5 5.15.11 and PyQtWebEngine 5.15.7 | No pytest, PySide6, pywinauto or PyInstaller. |
| `dist\CoGeNT.exe` | py2exe build from 2020-07-09, **32-bit** Python 2.7 | Older than the 2023/2024 source edits. Do not use it as a reference for current behavior. |

## 2. Application inventory

**Runtime path.** `CoGeNT.pyw` imports `back_end.pyw`. At import time, `back_end` creates `htmlPy.AppGUI` (PySide QtWebKit `QWebView`), binds `BackEnd(htmlPy.Object)` as the JS object `BackEnd`, and renders `html/Tool_Index_Page.html` through Jinja2.

| Area | Files | Role |
|---|---|---|
| GUI / controller | `CoGeNT.pyw`, `back_end.pyw` (760 lines) | Slots called from JS. Holds session state (`__load`, `__msg_saved`, `__sig_saved`, ...). |
| JS bridge | `binder.js` (copied into htmlPy as `htmlPy/binder.js`; the stray root file `htmlPy` is a copy of it) | Rewrites `<a data-bind>` and `<form data-bind>` into `eval("BackEnd.slot('json')")` calls. |
| DBC parser | `Dbc_Parser.pyw` (622) | Hand-written line parser: messages, signals, attributes, multiplexing. |
| Page generators | `Can_dbc_gen.pyw` (707), `Can_filter_python_gen.pyw` (203) | Build `html/CanDbc*Configuration.html` and `js/*.js` from the DBC. |
| Code generators (the "code gen" button) | `can_rx_filt_gen.py`, `msg.py`, `il_par_h_generation.py`, `il_par_c_generation.py`, `vnim_app_signals_par.py` | Write the C/resource files through `print` with `sys.stdout` redirected. |
| Unused / dev-time | `w601_parser_gen.py` + `*_template.py` (Android HAL, uses `cantools`), `Configuration_Read_Parse_HTML.py` (uses `xlrd` on `Candriver_Config.xls`), `ff\`, `testing\` | Not on the Generate path. The w601 call in `code_gen` is commented out. |
| Templates / static | `html\*.html` (19, up to 3.4 MB), `js\*.js` (10, up to 1 MB), `style\styl.css`, `batman.ico` | Jinja2 templates; `{{'styl.css'|staticfile}}`. |
| State / config | `data\*.data` (JSON), `Config\*.cfg` (zip of html/data/js), `U321.ini`, `.pa` files | `dbc_details.data` stores an **absolute** DBC path. |
| Build | `setup.py` (py2exe), `build\`, `dist\` | Legacy. |
| Reference outputs | `CODE_GEN\<run>\*` (15 previous runs). `CODE_GEN\DBC_40024_2` also holds its `.cfg` and `.dbc`. | Useful as test oracles; see section 7. |

Several HTML pages (`Home_page.html`, `Can*Configuration.html`) call slots that don't exist on `BackEnd` (`Can_DRIVER`, `DRV_SaveButton`, `Can_IL`, ...). Those are dead UI paths today.

## 3. Trace: Generate button to output files

```
html/Tool_Index_Page.html
  <input type="button" value="  code gen " onclick="BackEnd.code_gen()">
        |  (htmlPy: QWebFrame.addToJavaScriptWindowObject("BackEnd", BackEnd()))
        v
back_end.pyw:174  BackEnd.code_gen()
  gate 1: self.__load == 0            <- set only by upload_dbc() ("Load DBC") in THIS session
  gate 2: __msg_saved == 0 and __sig_saved == 0
                                      <- set only by Can_dbc_msg_SaveButton / Can_dbc0_sig_SaveButton in THIS session
  try:
    t = now().strftime("%Y-%m-%d %H:%M")
    can_rx_filt_gen : set_file_node_il(dbc,node); set_init_global(t); filter_gen()
        reads  ./data/CanDbcMsgConfiguration.data
        writes ./CODE_GEN/can_rxrule.cfg, ./CODE_GEN/nw_can_dll.h
    msg             : msg_struct_generation()      -> ./CODE_GEN/nw_il_msg.h
    il_par_h_generation : il_par_h_gen_function()  -> ./CODE_GEN/nw_il_par.h
        reads  CanDbcMsgConfiguration.data + CanDbcSigConfiguration.data
    il_par_c_generation : il_par_c_gen_function()  -> ./CODE_GEN/nw_il_par.c
    vnim_app_signals_par: vnim_app_c_gen()   -> nw_vnim_app_signals_par.c
                          vnim_app_h_gen()   -> nw_vnim_app_signals_par.h
                          vnim_resource_gen()-> vnim.msg.resource, vnim.txrx.resource, nw_host_mgr_txrx.resource
                          nm_par_gen()       -> nw_nm_par.h
    alert('Code Generated in CODE_GEN folder')
  except Exception as e:
    open('./CODE_GEN/errorlog.txt','w').write(str(e)); alert('ERROR! Please check the database file') x2
  default_page()
```

Every generator follows the same pattern: `f=open("./CODE_GEN/x",'w'); sys.stdout=f; print ...; f.close()`. Each `set_file_node_il` builds a new `Dbc_Parser.dbc_parser`, and each `get_msg_type` call re-parses the DBC file (the DBC is read many times per run). A full run on the S2XX 40024 DBC produced 11 files (about 3.6 MB) in about 10 s.

## 4. Possible causes of failed generation (current Python 2.7 app)

Ranked by likelihood. Each item says what the user sees.

1. **The interpreter and dependencies are missing.** `C:\Python27` is absent, so `venv\Scripts\python.exe` cannot start. Jinja2 is also absent from `venv`, so `import htmlPy` fails. Seen as: the app does not open at all when launched from source.
2. **`sys.stdout` is never restored after generation.** After a successful Generate, `sys.stdout` is a *closed* file. The next `print` (`back_end.pyw:271`, `print final_data` in `Can_dbc0_msg`) raises `ValueError`. The bare `except` hides it. Seen as: *"Load dbc file / enter proper node name @1"* when reopening Message configuration after a generate. That blocks the save, which blocks the next generate until the app restarts. After a *failed* generate, `sys.stdout` still points at the half-written C file, so later prints corrupt that file.
3. **Running the `.pyw` under `pythonw.exe` (Python 2).** `sys.stdout` is an invalid handle there, and `print final_data` (more than 4 KB) raises `IOError: [Errno 9]`. Same *"@1"* alert: the message page never opens, so it can never be saved, and Generate then says *"Please save Filter, message and signal configurations..."*. py2exe builds hide this because py2exe swaps stdout for a blackhole.
4. **Session-only gates.** Generate needs Load DBC, then Message Save, then Signal Save, all in the *same* session. `load_cfg` and `onpageload` restore the DBC path but **not** `__load`, so after a restart or "load configuration" you get *"Please Click load button to load dbc!!"*. The prompt also mentions "Filter", but filter save is not actually checked.
5. **Windows paths typed with backslashes break the JS bridge.** `binder.js` builds `eval("BackEnd.upload_dbc('" + JSON.stringify(form) + "')")`. A typed path such as `D:\DBC\U321.dbc` loses its escaping inside the single-quoted JS literal. `json.loads` in `upload_dbc` then raises *outside* its `try`, and the slot dies silently. `__load` stays 1, and Generate keeps saying "Please Click load". A `'` in a path breaks it the same way. The Browse dialog (forward slashes) avoids this.
6. **Absolute DBC path in saved config.** `dbc_details.data` and every `.cfg` store paths such as `G:/Visteon/...` or `C:/VSANKAR1/...`. On another PC, Load fails (*"ERROR! Please Enter Proper dbc/node name"*) or generation raises `IOError`.
7. **Saved data does not match the DBC (KeyError).** Generators index the saved JSON directly, for example `filter_cfg_data[mes['Msg_name'].upper()+'_rx_enable']` at `can_rx_filt_gen.py:90`. A message in the DBC that is missing from the saved `.data` raises `KeyError`. This happens with a new DBC revision but old `.data`, or with a wrong node name. Seen as: *"ERROR! Please check the database file"*. `errorlog.txt` then contains only the bare key name (no traceback).
8. **CWD-relative paths.** `./data`, `./CODE_GEN`, `./html` and `./Config` resolve against the *current directory*, not the app folder. A shortcut whose "Start in" differs, or a launch from another folder, reads stale or missing data or writes outputs somewhere unexpected. Templates use `base_dir`, so the UI looks fine while I/O goes elsewhere.
9. **Partial or stale outputs look like success.** `./CODE_GEN` is reused and overwritten file by file. If stage 4 fails, files 1–3 are new and the rest are from an older run. Only the alert distinguishes the two.
10. **`errorlog.txt` can itself fail.** If an exception occurs before `./CODE_GEN` exists (for example, a bad DBC in `set_file_node_il`), the `open('./CODE_GEN/errorlog.txt')` inside `except` raises. The slot aborts with no alert.
11. **Latent crashes in helper slots.** `default_page()` sets `self.__dbc='None'` when `__node is None` (wrong variable), then concatenates `None` and raises `TypeError`. `onpageload()` raises `NameError` (`dbc_name` unbound) when `ch0_file` is empty.
12. **DBC parser fragility.** Lines are split on single spaces, and a message is "Tx" whenever the node name appears *anywhere* as a token on a `BO_` line. Tabs, double spaces, or a node name equal to a signal or message token change the result. Non-ASCII bytes appear in the S2XX DBCs (10 bytes in comments) and the BAIC DBC (286 bytes). In Python 2, mixing them with `unicode` node names from JSON can raise `UnicodeDecodeError`.

## 5. Python 3 compatibility findings

Automated 2to3 dry run (on a scratch copy) plus targeted greps:

| Issue | Where | Impact on Python 3 |
|---|---|---|
| `print` statements | all generators (hundreds), `back_end.pyw:271` | SyntaxError (mechanical fix). |
| **Integer `/`** | `il_par_c_generation.py` (47), `il_par_h_generation.py` (28), `msg.py` (18), `can_rx_filt_gen.py` (2), `Configuration_Read_Parse_HTML.py` (2) | **Silent wrong output**: `5/8` becomes `0.625`, and `str()` emits `1.0` into C code. Floats used as indexes raise TypeError. Each site needs `//`. |
| `file.next()` | `Dbc_Parser.pyw` (4) | AttributeError, so `next(f)`. |
| `dict.iterkeys/iteritems`, `filter()/map()` returning lists, `.pop()` on `filter` | `vnim_app_signals_par.py:…max(list_dict.iterkeys()…)`, `w601_parser_gen.py` | AttributeError/TypeError. |
| **Dict iteration order** | about 300 `for k in <dict>` loops in generators and the parser | Python 2 used hash order; Python 3.7+ uses insertion order. Unsorted loops may emit C rows in a **different order**. Must be detected by byte comparison against a Python 2 oracle and decided per case. |
| Text encoding | `open(dbc,'r')` and all writes | Python 3 decodes with cp1252 by default. Bytes 0x81/0x8D/0x8F/0x90/0x9D raise `UnicodeDecodeError`. Use `encoding='latin-1'` (byte-transparent, matches Python 2 `str`) for DBC and C output, and `utf-8` for JSON `.data`. |
| `sys.stdout` under `pythonw` | all generators | In Python 3 `sys.stdout` is `None` under pythonw; redirect and restore explicitly. |
| `u"..."`, octal `004` | `back_end.pyw`, `setup.py` | Trivial. |
| `.pyw` import | `Dbc_Parser`, `Can_dbc_gen`, `Can_filter_python_gen` | Still importable on Windows in Python 3 (`.pyw` is a source suffix). Keep the names or rename to `.py`. |

**Dependencies**

| Legacy | Status on Python 3.12 | Replacement |
|---|---|---|
| htmlPy 2.0.3 | Abandoned (2016). Imports `PySide` (Qt 4) only; no Python 3 Qt 5/6 support. | Small in-repo shim `cogent_gui/webgui.py` exposing the subset used (`Object`, `Slot`, `AppGUI.template`, `evaluate_javascript`, `bind`, `start`, `window`, `template_path`, `static_path`). |
| PySide 1.2.4 (Qt 4.8, QtWebKit) | No wheels after Python 3.4; QtWebKit is gone from Qt 5.6+. | **PySide6 6.11.2** (`cp310-abi3-win_amd64`; works on 3.12 and 3.14). QtWebEngine with QWebChannel. |
| Jinja2 2.x / MarkupSafe | Fine | Jinja2 3.1.6 / MarkupSafe 3.0.4 (already installed globally). |
| py2exe | Python 2 only | PyInstaller 6.22.3 (`--windowed`, `--collect-all PySide6` not needed; use the PySide6 hooks). |
| cantools, xlrd | Only in unused dev-time modules | cantools 44.x and xlrd 2.0.2 (2.x still reads `.xls`). Not needed at runtime. |

**Behavioral gaps between QtWebKit and QtWebEngine** that the port must handle:

- `evaluate_javascript` becomes **asynchronous** (`runJavaScript`). `unlock()` reads a JS `prompt()` result synchronously, so it must switch to `QInputDialog`.
- The JS bridge becomes **asynchronous** (QWebChannel). `onload="load()"` calls `BackEnd.onpageload()` before the channel is ready, so calls must be queued until it is ready.
- `setHtml()` is limited to **2 MB** in QtWebEngine. `CAN_DBC_sig.html` is 3.4 MB, so rendered templates must be written to a file and loaded by URL.
- Under a real `file://` base URL, `anchor.href` and `form.action` return **absolute URLs**, which breaks `eval(call + ...)`. Use `getAttribute()` and resolve the slot without `eval` (this also fixes cause 5).
- The `DOMNodeInserted` mutation event was removed in Chromium 127+. Use a `MutationObserver`.
- `QFileDialog.getOpenFileName(..., selectedFilter='*.cfg')` should use a `filter=` string in PySide6. Build JS strings with `json.dumps` instead of `'...'+path+'...'`.

## 6. Recommendation

- **Target: CPython 3.12 x64 (python.org build, 3.12.10)**. It is in security-fix support until 2028-10. Every required wheel exists for it, including PySide6 (abi3), pytest-qt 4.5.0, pywinauto 0.6.9 and PyInstaller 6.22.3. Keep the code free of 3.13+/3.14-only features, and run the suite on 3.14 as a forward check. 3.14 is not the primary target because pywinauto/comtypes and PyInstaller have the least mileage there.
- **GUI stack: PySide6 + QtWebEngine + QWebChannel behind a thin htmlPy-compatible shim.** All HTML/JS/CSS and the controller structure stay as they are. Rejected alternatives: pywebview (different bridge semantics, uses the Edge WebView2 runtime), PyQt5 (Qt 5.15 is end-of-life), and a full Qt Widgets rewrite (largest diff, and the pages are generated HTML).
- **Strategy:** freeze behavior with a Python 2.7 *test-only oracle*, port the generators until outputs are byte-identical, then port the GUI. Bug fixes for section 4 are a **separate, opt-in** phase so that "migrated" and "changed" are never mixed.

## 7. Test oracles available locally

- `CODE_GEN\DBC_40024_2\`: a full previous run with its `.cfg` (holds `data/*.data`) and a DBC. The DBC filename lacks the `_Edited` suffix recorded in the outputs' `Traceability` line, so it must be checked before it is trusted.
- `Config\*.cfg` paired with `DBC\*.dbc` by revision: 35354, 35891, 36026, 36144, and 100723 (`Config_S237_Common_DBC_Itr12.cfg`). That gives 5 more fixtures.
- Python 2.7.18 x64 installed to `C:\Python27`, used only for tests, regenerates exact expected outputs with the *current* source. The generators need only the stdlib, so the oracle needs no extra packages.
