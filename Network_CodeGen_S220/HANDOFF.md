# CoGeNT (Network_CodeGen_S220): developer handoff

Last updated 2026-10-09. Repository `senthilvel-k/Network_CodeGen_w502`; the application lives in
`Network_CodeGen_S220/`. State described here: `main` = `a7bc740` (merge of PR #1, branch
`py3-migration` @ `ad5fbd0`). The files under `Network_CodeGen_S220/` are identical to `ad5fbd0`,
the commit all test results below were produced on.

---

## 1. What the tool does

CoGeNT reads a CAN database (`.dbc`) for one ECU node (normally `SMART_CORE`), lets the user configure
messages and signals in an HTML GUI, and generates the CAN interaction-layer C sources for that ECU:

| Generated file (in `CODE_GEN\`) | Generator |
|---|---|
| `can_rxrule.cfg`, `nw_can_dll.h` | `can_rx_filt_gen.py` (`filter_gen`) |
| `nw_il_msg.h` | `msg.py` (`msg_struct_generation`) |
| `nw_il_par.h` | `il_par_h_generation.py` |
| `nw_il_par.c` | `il_par_c_generation.py` |
| `nw_vnim_app_signals_par.c/.h`, `vnim.msg.resource`, `vnim.txrx.resource`, `nw_host_mgr_txrx.resource`, `nw_nm_par.h` | `vnim_app_signals_par.py` |

User workflow (index page `html/Tool_Index_Page.html`): select DBC + node, press **Load DBC**, open
**+ TX/RX Message Configurations** and press **Save and Back**, then **+ TX/Rx signal Configurations**
and **Save and Back**, then press **code gen**. **save_cofiguration** / **load_cofiguration** zip/unzip
`html/`, `data/` and `js/` into `Config\<timestamp>.cfg`.

The tool was migrated from Python 2.7 (htmlPy + PySide 1.2.4 / Qt 4 WebKit, py2exe) to
**Python 3.12 + PySide6 6.11.2 (QtWebEngine)**. The generated files are byte-identical to the legacy tool.

---

## 2. Architecture

```
CoGeNT.pyw ──> back_end.py ──────────────┐  BackEnd(QObject): one @Slot per button/link
                │                          │
                │ uses                     ▼
                ▼                   cogent_gui/webgui.py  (htmlPy-compatible shim)
   html/*.html (Jinja2 templates)    - renders template to %TEMP%\cogent_render_* and loads it by URL
   js/*.js, style/styl.css           - QWebChannel exposes BackEnd to JS; cogent_gui/bridge.js wires
                                       <a data-bind>/<form data-bind> to slots (no eval; QtWebKit
                                       checkbox rule: unchecked -> "")
                │
   Load DBC     ├─> Dbc_Parser.py (dbc_parser): DBC text parser; dicts are py2compat.Py2Dict
   Msg/Sig page ├─> Can_dbc_gen.py / Can_filter_python_gen.py: build html/Can*Configuration.html + js
                │   back_end appends saved data (data/*.data, JSON) -> html/CAN_DBC_msg.html / CAN_DBC_sig.html
   code gen     └─> cogent_generate.run_code_generation(dbc, node, time)
                      1. checks: DBC exists, data/CanDbcMsg|SigConfiguration.data exist + valid JSON,
                         msg.find_unsupported_multiplex()
                      2. runs the 5 generators (same order as legacy) into CODE_GEN\.staging
                         (cogent_io.open_output/close_output redirect print() into the file)
                      3. moves the 11 files into CODE_GEN only when all succeeded
                      4. on failure: CogentError -> popup; traceback -> CODE_GEN\errorlog.txt + logs\cogent.log
```

Key modules (all under `Network_CodeGen_S220/`):

| Module | Role |
|---|---|
| `CoGeNT.pyw` | Entry point (`app.bind(BackEnd()); app.start()`). |
| `back_end.py` | GUI controller: slots `upload_dbc`, `code_gen`, `Can_dbc0_msg`, `Can_dbc0_sig`, `Can_Filter`, `*_SaveButton`, `save_cfg`, `load_cfg`, `file_browse`, `default_page`, `onpageload`, `unlock`, `pythonfn` (test hook). Session state is held in name-mangled attributes (`__dbc`, `__node`, `__load`, `__msg_saved`, `__sig_saved`). |
| `cogent_gui/webgui.py`, `cogent_gui/bridge.js` | Replacement for htmlPy on PySide6 (template rendering, JS bridge, alerts, `evaluate_javascript` queued until a page has loaded). |
| `cogent_generate.py` | Code-generation pipeline used by `code_gen` (staging, checks, error translation). |
| `cogent_errors.py` | `CogentError` (operation / reason / item / hint / log path), `log_failure`, `missing_config_entry`. |
| `cogent_io.py` | `open_output`, `close_output`, `abort_output`; tracks `current_output` for messages. |
| `py2compat.py` | `Py2Dict` (CPython 2.7 dict iteration order, **32-bit** `size_t`), `py2_print` (print-statement softspace). Both are visible in the generated files. |
| `Dbc_Parser.py` | DBC parser (original logic; `get_nodes()` added). |
| `msg.py`, `il_par_h_generation.py`, `il_par_c_generation.py`, `vnim_app_signals_par.py`, `can_rx_filt_gen.py` | Generators (2to3 + `//` + encodings; `print` is `py2_print`). `msg.py` also has `multiplex_layout_problem`, `find_unsupported_multiplex`, `UnsupportedMultiplexLayout`. |
| `Can_dbc_gen.py`, `Can_filter_python_gen.py` | HTML/JS page generators. |
| `CoGeNT.spec` | PyInstaller onedir build (files beside the exe, like the old py2exe layout). |
| `tools/` | `gen_harness.py` (headless generation, Py2/Py3 compatible), `compare_legacy.py`, `build_fixtures.py`, `dump_dbc.py`, `make_expected.py` (Python 2.7 oracle), `find_divisions.py`, `apply_output_helpers.py` (one-off port tools). |
| `tests/` | pytest suite (see section 7). |

Encodings: DBC input and C/HTML/JS outputs use `latin-1` (byte pass-through, like Python 2 `str`);
`data/*.data` are UTF-8 JSON. All paths the app reads and writes (`./data`, `./html`, `./js`, `./CODE_GEN`,
`./Config`, `./logs`) are **relative to the current working directory**, which must be the app folder.

Repository layout notes:
- `CODE_GEN/` (184 tracked files) holds legacy known-good outputs. `DBC_40024_2`, `DBC_40024` and
  `DBC_S237_36144_2` were produced by the current generator source and are used as test references.
- `Config/*.cfg`: saved configurations; `DBC/`: DBC files, including
  `S2XX_SMART_CORE_SVNID_40024_25_02_2026_Edited.dbc`, copied from `D:\networkgen\DBC\DBC_V40024`.
- Legacy, not used at runtime and **not ported** (still Python 2 syntax):
  - `w601_parser_gen.py`: Android HAL path, commented out in `code_gen`, needs `cantools`.
  - `setup.py`: py2exe, replaced by `CoGeNT.spec`.
  - `ff/can_nm.py`, `ff/can_tp_diag.py`, `ff/il_tx_frame_table.py`, `ff/can_disp_drv.pyw`,
    `ff/can_il_vnim.pyw`, `testing/mailbox.py`.
  - `Configuration_Read_Parse_HTML.py`: compiles on Python 3, but its `/` divisions were not converted.
  - `binder.js` and the extension-less file `htmlPy`: old htmlPy binder, superseded by `cogent_gui/bridge.js`.
- `docs/superpowers/specs/2026-10-08-python3-migration-analysis.md` (original analysis),
  `docs/superpowers/specs/2026-10-08-error-popups.md` (popup inventory),
  `docs/superpowers/plans/2026-10-08-python3-migration.md` (migration plan).

---

## 3. Environment setup

Machine used: Windows 10 x64, Git 2.56, GitHub CLI 2.102.0 (`gh`, logged in as `senthilvel-k`).

| Item | Value |
|---|---|
| Python | 3.12.10 x64. The existing `.venv` is based on the **Microsoft Store** Python 3.12.10 (a python.org install was blocked in the session that created it). A python.org 3.12.x x64 install is preferred for new setups. |
| Runtime deps (`requirements.txt`) | `PySide6==6.11.2`, `Jinja2==3.1.6` |
| Dev deps (`requirements-dev.txt`) | `pytest==9.1.1`, `pytest-qt==4.5.0`, `pywinauto==0.6.9`, `pyinstaller==6.22.3`, `websocket-client==1.8.0` (installed alongside: shiboken6 6.11.2, MarkupSafe 3.0.4, comtypes 1.4.17) |
| Ignored folders | `.venv/`, `venv/` (old, broken Python 2.7 venv, points to missing `C:\Python27`), `dist/` and `build/` (old py2exe build, 32-bit), `dist_py3/`, `build_py3/`, `logs/`, `CODE_GEN/.staging/`, `CODE_GEN/errorlog.txt` |

Fresh setup (from `Network_CodeGen_S220`):

```bash
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe -c "import PySide6, jinja2; from PySide6 import QtWebEngineWidgets; print(PySide6.__version__, jinja2.__version__)"
```

Run the app from source (the working directory must be `Network_CodeGen_S220`):

```bash
.venv/Scripts/python.exe CoGeNT.pyw
```

Build the exe (output `dist_py3/CoGeNT/CoGeNT.exe`, about 567 MB; `html`, `js`, `style`, `data`, `cogent_gui/bridge.js` and `batman.ico` sit beside the exe):

```bash
.venv/Scripts/pyinstaller --noconfirm --clean CoGeNT.spec --distpath dist_py3 --workpath build_py3
```

Optional Python 2.7 oracle (not installed on this machine): install CPython 2.7.18 x64 (python.org MSI,
needs elevation), then `COGENT_PY27=C:\Python27\python.exe .venv/Scripts/python.exe tools/make_expected.py`.
That extracts the baseline commit `83612bb` with `git archive` into `%TEMP%\cogent_py27_baseline` and
writes `tests/expected/<fixture>/` (commit those files).

---

## 4. Features: done and remaining

Done (merged to `main`):
- Full Python 3.12 / PySide6 port of the generators, the parser, the page generators and the GUI.
- Byte-identical output to known-good legacy runs: Python 2.7 dict-order emulation (32-bit), print
  softspace, `//` for all 128 integer divisions, explicit encodings.
- htmlPy replacement (`cogent_gui`) that handles pages over 2 MB, queues bridge calls until the page
  is ready, has no `eval` (paths with `\` and `'` work), and keeps the legacy checkbox serialization.
- Code-generation pipeline with staging (no mixed old and new outputs), up-front checks, and error
  explanations. Tracebacks go to `CODE_GEN\errorlog.txt` (overwritten per failure, deleted after a
  successful run) and `logs\cogent.log` (appended).
- Reworked error popups with their root causes fixed (inventory in
  `docs/superpowers/specs/2026-10-08-error-popups.md`).
- PyInstaller packaging; headless harness and tools; 283 automated tests.

Remaining (see section 8 for the ordered list): multiplex layouts beyond VCU5_500, the Python 2.7 oracle
comparison, the optional workflow fixes (load configuration also loads the DBC; working-directory
independence), a non-blocking UI during code gen, and repository hygiene/cleanup items.

---

## 5. Known issues, root causes, and status

| # | Issue | Root cause | Status |
|---|---|---|---|
| 1 | Enabling Rx of multiplexed messages such as `BMS19_100` / `BMS20_100` (S2XX 40024 DBC; also enabled in `Config\Test.cfg`) stops code gen. | `msg.msg_struct_gen_multiplex` only supports the VCU5_500 layout: each multiplexed signal starts at bit 0 (one 8x`temp_len` grid per signal), and the multiplexor is in byte 7 (`mul_sig_index = 6`). The BMS cell temperatures start at bit 16+, so the legacy code overflowed the grid (`IndexError`). No correct output for such messages has ever existed. | **Detected before any file is written.** The popup names the message, the signal (e.g. `BMS_CELLTEMP1`, start bit 16, length 16, Intel) and the fix (untick Rx). Real support needs a C-layout decision for the union/struct and a check of the other generators' multiplex handling. |
| 2 | 144 tests skipped (`INCOMPLETE: no Python 2.7 oracle output`). | Python 2.7 could not be installed in the migration session (installer and downloaded-runtime execution were blocked). | References used instead: legacy `CODE_GEN` runs from the current source (11/11 identical for `DBC_S237_36144_2`, `DBC_40024`, `DBC_40024_2`) and pages archived inside `.cfg` files. Open item. |
| 3 | After restarting the app or loading a configuration, code gen asks to **Load DBC** and to save both pages again. | Legacy design: per-session flags `__load`, `__msg_saved`, `__sig_saved`. `load_cfg` restores the DBC path but not `__load`. Load DBC now also resets the saved flags when the DBC or node changes, because saved settings for another DBC cause `KeyError`s. | Popups explain exactly what to do. Optional fix: `load_cfg` validates and loads the DBC (old plan Task 9a). |
| 4 | Starting the app from another working directory (e.g. a shortcut with a different "Start in") reads and writes the wrong `data/`, `html/` and `CODE_GEN/`. | All paths are CWD-relative (legacy). Templates use `base_dir`, so the UI looks fine. | Open. Fix: `os.chdir(base_dir)` at the top of `CoGeNT.pyw` (Task 9b). The exe started from Explorer is fine (CWD = exe folder). |
| 5 | The GUI freezes during code gen: about 19 s for the 40024 DBC (about 1.4 s of that is the multiplex pre-check), about 10 s for 36144. | Generators run on the GUI thread inside a QWebChannel slot (same as legacy). Each `get_msg_type` re-parses the DBC. | Open. Options: run `cogent_generate` in a subprocess or worker (the generators redirect the global `sys.stdout`, so a subprocess is safest); cache the parse. |
| 6 | Signal order inside a few messages can differ from **old** (2023–early 2024) legacy outputs. | Python 2 dict order depends on interpreter bitness. Runs from 2024-06 on (including Feb 2026) match 32-bit Python 2.7; older runs match 64-bit. `py2compat.SIZE_T_BITS = 32`. | By design; set `SIZE_T_BITS = 64` only to reproduce the old 64-bit runs. |
| 7 | "Code generation failed … has no '<field>' setting for message/signal X". | A configuration saved for a different DBC revision, e.g. `Config\Config_DBC_35354_1.cfg` contains `SBW1_CRC__*` (DBC had `SBW1_CRC_`). | Explained by the popup (setting, item, data file, page to re-save). Root cause is user data, not code. |
| 8 | Unreachable legacy pages call slots that `BackEnd` does not have: `Can_DISP`, `Can_DRIVER`, `Can_IL`, `Can_NM`, `Can_VNIM`, `Can_XCVR`, `Can_dbc0`, `DIAG/DISP/DRV/FLT/IL/NM/TP/VNIM_SaveButton` (in `Home_page.html`, `Can_Filter_Config.html`, `Can{DIAG,DISP,DRV,IL,NM,TP,VNIM}Configuration.html`). | Features never implemented in this tool version. `Tool_Index_Page.html` does not link these pages. | Harmless; the bridge logs `cogent: unknown slot …` to the page console. Remove or implement. |
| 9 | `unlock` slot (password prompt) is unreachable from the UI. | No page calls `BackEnd.unlock`. | Left as is (ported to `QInputDialog`). |
| 10 | Running the app from the repo folder modifies tracked files: `data/*.data`, `html/CanDbc*Configuration.html`, `html/CAN_DBC_msg.html`, `html/CAN_DBC_sig.html`, `html/Can_filter.html`, `js/*.js`, `Config/*.cfg`, `CODE_GEN/*`. | Legacy design stores session state and generated pages inside the app folders, and these files are committed. | Open. Use a copy of the app or the exe for real work, or untrack the runtime-generated pages and data. `logs/` and `CODE_GEN/.staging/` are now git-ignored. |
| 11 | `logs\cogent.log` grows without limit. | Appends one block per failure; no rotation. | Open (low priority). |
| 12 | PyInstaller bundle is about 567 MB. | Full PySide6 including QtWebEngine; only 3 Qt modules excluded. | Open (low priority): exclude unused PySide6 modules. |
| 13 | QtWebEngine profile folder is `%LOCALAPPDATA%\python\QtWebEngine`, shared with any other Python QtWebEngine app. | Application name not set. | Open (low): `QApplication.setApplicationName("CoGeNT")` before creating the app. |
| 14 | Dead or unused code. | `Dbc_Parser.create_pickle` (never called) would pickle `Py2Dict` objects that cannot be unpickled; four generators import `Py2Dict` without using it (only `vnim_app_signals_par` uses it); `cogent_io.close_output` restores `sys.__stdout__` rather than the previous stream. | Open (minor). |
| 15 | Non-ASCII DBC identifiers would be upper-cased differently than in Python 2 (`é`→`É`). | Python 3 `str.upper()` is Unicode-aware; Python 2 byte strings were not. | Not relevant for valid DBCs (identifiers are ASCII). |
| 16 | The separate copy `D:\networkgen\Network_CodeGen_S220` (**not this repo**) shows "Code generation failed: list index out of range". | Its `Dbc_Parser.pyw` uses `if temp_sig[0].split("\|")[1].split("@")[0] == 1:`, comparing the signal *length* string with `1`, so every signal becomes Motorola and `VCU5_500` overflows. It also dropped upper-casing of signal names and the multiplex bookkeeping. Its `cogent_error.log` contains `JSONDecodeError` and `AssertionError` entries. | Do not use that copy. This repo generates the same DBC and config correctly. |
| 17 | `.venv` is based on the Microsoft Store Python. | python.org installer could not run in the migration session. | Works (tests and PyInstaller build pass); prefer a python.org base for release builds. |

Intentional behaviour changes versus the legacy tool (all covered by tests):
- File dialogs filter `*.cfg` / `*.dbc`, with an "All files" option.
- Load DBC trims whitespace and resets the saved-page flags when the DBC or node changes.
- The configuration pages require a loaded DBC; before, they built empty pages from `dbc=None`.
- Save configuration reports after writing and removes a half-written archive.
- Load configuration validates the archive before extracting, and cancel is silent.
- Browse cancel keeps the path.
- Code gen output is published atomically, and a stale `errorlog.txt` is deleted after a successful run.

Debugging aids:
- **Headless generation:**
  `.venv/Scripts/python.exe tools/gen_harness.py --dbc <dbc> --node SMART_CORE --data <folder with *.data> --out <out> [--stage code|pages|all] [--app-dir <other app folder>]`
- **Compare with a legacy run** (ignores Date/By/Traceability lines):
  `.venv/Scripts/python.exe tools/compare_legacy.py <out> CODE_GEN/DBC_40024_2`
- **Parser dump:** `.venv/Scripts/python.exe tools/dump_dbc.py <dbc> SMART_CORE`
- **Logs:** `CODE_GEN\errorlog.txt` (last code-gen failure, with traceback and DBC/node/folder),
  `logs\cogent.log` (all failures).

---

## 6. Error popups (current behaviour)

Format of every failure popup:
```
<Operation> failed while <item>.
Reason: <cause>.
<What to do>
Technical details: <log file>
```
Triggers: Load DBC with empty fields, a missing file, an unknown node (lists the nodes of the `BU_`
line) or an unreadable DBC; code gen before Load DBC, or before saving the pages (names the pages);
code gen failures (missing DBC, missing or damaged `.data`, missing setting for message/signal X,
unsupported multiplex layout, output file locked by another program, internal error); opening a page
before Load DBC; save/load configuration failures (not a zip, not a CoGeNT archive, damaged
`dbc_details.data`, unwritable `Config`). Success popups keep their legacy first line ("Database loaded
successfully", "Code Generated in CODE_GEN folder" plus file count and path, "Configuration saved
successfully" plus path, "Configuration loaded successfully" plus path and a reminder to Load DBC).
Full table: `docs/superpowers/specs/2026-10-08-error-popups.md`.

---

## 7. Tests

283 tests are collected. GUI tests need an interactive Windows desktop session; the e2e test needs the
built exe.

| File | Count | What it checks |
|---|---|---|
| `tests/test_generation_golden.py` | 129 | 33 legacy comparisons (11 files × `s237_36144_2`, `s2xx_40024`, `s2xx_40024_a`), 8 "all files generated", 88 oracle comparisons (skipped) |
| `tests/test_pages_golden.py` | 80 | 32 page comparisons vs pages archived in each fixture's `.cfg`, 48 oracle comparisons (skipped) |
| `tests/test_parser_parity.py` | 16 | 8 parser dumps (node found, IL Tx/Rx present), 8 oracle comparisons (skipped) |
| `tests/test_generation_errors.py` | 10 | pipeline: success = legacy, repeat run, multiplex rejection before writing, missing message/signal settings, damaged/missing `.data`, missing DBC, locked output file, internal error without traceback, logs |
| `tests/test_py2compat.py` | 7 | Python 2 hash, `Py2Dict` order vs legacy (incl. 32-bit case), print softspace |
| `tests/test_repeatable.py` | 3 | in-process repeat; 3 separate runs byte-identical (2 fixtures) |
| `tests/test_paths_with_spaces.py` | 1 | DBC/data/output/app folders with spaces and `&` |
| `tests/test_parser_encoding.py`, `tests/test_pages_encoding.py` | 1 + 1 | non-cp1252 bytes in DBC |
| `tests/gui/test_webgui.py` | 9 | shim: slots, queued calls, backslash/quote paths, QtWebKit checkbox rule, >2 MB page, alerts, temp cleanup, static files |
| `tests/gui/test_gui_generate.py` | 6 | full GUI flow = legacy (36144_2), real Save and Back forms keep `.data` byte-identical, repeat, Browse, save/load configuration, failure then page still opens |
| `tests/gui/test_gui_errors.py` | 18 | every reworked popup, with the real 40024 `_Edited` DBC from a folder named `input DBC (Rev 40024, it's edited)`; code gen = `CODE_GEN/DBC_40024_2` |
| `tests/e2e/test_exe_smoke.py` | 2 | packaged exe (36144_2 and 40024): Load DBC, both pages with real Save and Back, code gen, outputs = legacy. Web content driven via Chrome DevTools Protocol (`QTWEBENGINE_REMOTE_DEBUGGING`, 127.0.0.1), native alert dialogs via UI Automation. |

Fixtures (`tests/fixtures/<name>/`, rebuilt by `tools/build_fixtures.py`): `s2xx_40024`
(`CODE_GEN/DBC_40024_2` cfg + 40024 `_Edited` DBC), `s2xx_40024_a` (`CODE_GEN/DBC_40024` cfg),
`s237_36144_2`, `s237_35354` (`Config_DBC_35354_2.cfg`), `s237_35891`, `s237_36026`, `s237_36144`,
`s237_100723`.

Latest results (2026-10-08, code = `ad5fbd0`, identical to current `main`):

| Command | Result |
|---|---|
| `.venv/Scripts/python.exe -m pytest --ignore=tests/gui --ignore=tests/e2e -rs` | **104 passed, 144 skipped** (all skips = Python 2.7 oracle), 9 min 38 s |
| `.venv/Scripts/python.exe -m pytest tests/gui` | **33 passed**, 2 min 54 s |
| `.venv/Scripts/python.exe -m pytest tests/e2e` (after a PyInstaller build) | **2 passed**, 1 min 58 s |
| `python -W error -m py_compile` on all 15 runtime modules (2026-10-09) | no errors or warnings |

Other verification done:
- Your scenario: 40024 `_Edited` DBC + `CODE_GEN/DBC_40024_2` config gives 11/11 files identical to
  `CODE_GEN/DBC_40024_2` (harness, pipeline, GUI, exe).
- `Config\Test.cfg` + Rev35354 DBC now gives the multiplex explanation (`BMS19_100`) instead of `IndexError`.

Test notes:
- Run the GUI tests in their own pytest process or with `--basetemp`; the in-process app copy changes the working directory.
- A GUI code-gen click blocks the JS round trip until generation ends; helpers in `tests/gui/gui_support.py` allow 180 s.
- Older legacy runs (`CODE_GEN/DBC_S237_35354/35891/36026/36144`) were made by older generator code
  with 64-bit Python 2.7. They differ only in `nw_il_par.h` and `nw_vnim_app_signals_par.c`, matching
  source edits of 2024-07 (e.g. `#include "nw_host_mgr_if.h"`). They are informational only.

---

## 8. Next steps (in order)

1. **Decide multiplex support** for `BMS19_100`/`BMS20_100`-type messages (issue 1). Write down the
   intended C layout (union per multiplexer value with several signals at offsets, multiplexor
   position), then extend `msg.msg_struct_gen_multiplex` and `msg.multiplex_layout_problem`, check how
   `il_par_h/c` and `vnim_app_signals_par` handle multiplexed Rx messages, and add a fixture with BMS19
   enabled. Until then the popup tells users to untick it.
2. **Python 2.7 oracle** (issue 2), if allowed: install 2.7.18, run `tools/make_expected.py`, commit
   `tests/expected/`, re-run the suite (the 144 skipped tests then run).
3. **Working-directory independence** (issue 4): add `os.chdir(os.path.dirname(os.path.abspath(__file__)))`
   at the top of `CoGeNT.pyw` (before importing `back_end`), with a test that launches from another folder.
4. **Load configuration also loads the DBC** (issue 3): in `load_cfg`, run the same checks as
   `upload_dbc` and set `__load = 0` when they pass. Product decision first, because this changes the workflow.
5. **Non-blocking code gen** (issue 5): run `cogent_generate.run_code_generation` in a subprocess and
   show progress. Keep the staging and error contract.
6. **Repository hygiene** (issue 10): stop tracking runtime-generated pages and data, or document
   "run from a copy"; add a CI workflow (no GitHub Actions exist) running the non-GUI suite on `windows-latest`.
7. **Cleanups** (issues 11–14): log rotation, PyInstaller excludes, application name, unused imports,
   `create_pickle`, and removal or port of the unported legacy modules listed in section 2.
8. Retire `D:\networkgen\Network_CodeGen_S220` (issue 16) so nobody uses its broken parser.

---

## 9. Resume in a fresh session

```bash
cd "D:/networkgen/Network_CodeGen_w502"
git fetch origin
git switch main
git pull --ff-only
cd Network_CodeGen_S220
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe -m pytest --ignore=tests/gui --ignore=tests/e2e -rs -q
.venv/Scripts/python.exe -m pytest tests/gui -q
.venv/Scripts/pyinstaller --noconfirm --clean CoGeNT.spec --distpath dist_py3 --workpath build_py3
.venv/Scripts/python.exe -m pytest tests/e2e -q
.venv/Scripts/python.exe CoGeNT.pyw
```

If `.venv` is missing (fresh clone), first run the setup in section 3. Start new work on a branch
(`git switch -c <topic>`), and open PRs with `gh pr create --base main`.
