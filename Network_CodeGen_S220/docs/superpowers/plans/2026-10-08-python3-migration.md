# CoGeNT Python 3 Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run CoGeNT (DBC → CAN C-code generator) on Python 3.12 with PySide6, producing output files byte-identical to today's Python 2.7 tool.

**Architecture:** First freeze current behavior. A headless harness drives the exact `BackEnd.code_gen` pipeline, and a test-only Python 2.7 interpreter produces expected outputs for 6 real DBC/config fixtures. Then port the parser and generators until the byte-comparison tests pass. Finally, replace htmlPy/PySide (Qt 4 WebKit) with a small htmlPy-compatible shim on PySide6 QtWebEngine + QWebChannel. HTML/JS pages stay as they are. Behavior fixes are a separate, opt-in final task.

**Tech Stack:** CPython 3.12.10 x64, PySide6 6.11.2 (QtWebEngine, QWebChannel), Jinja2 3.1.6, pytest 9.1.1, pytest-qt 4.5.0, pywinauto 0.6.9, PyInstaller 6.22.3, Git 2.56. Test oracle: CPython 2.7.18 x64.

**Spec:** `docs/superpowers/specs/2026-10-08-python3-migration-analysis.md`

## Global Constraints

- Primary runtime: CPython **3.12.10 x64** (python.org build) in `.venv312\`. The code must also import cleanly on 3.14.
- Runtime dependencies: exactly `PySide6==6.11.2`, `Jinja2==3.1.6`. Nothing else at runtime.
- Generated files (`can_rxrule.cfg`, `nw_can_dll.h`, `nw_il_msg.h`, `nw_il_par.h`, `nw_il_par.c`, `nw_vnim_app_signals_par.c`, `nw_vnim_app_signals_par.h`, `vnim.msg.resource`, `vnim.txrx.resource`, `nw_host_mgr_txrx.resource`, `nw_nm_par.h`) must be **byte-identical** to the Python 2.7 oracle. The only exception is an order-only difference that the user has explicitly accepted in `tests/accepted_order_diffs.json`.
- Tasks 1–8 are a migration only: no user-visible behavior changes. Behavior fixes happen only in Task 9, item by item, after the user approves each one.
- Python 2.7.18 is a **test-only oracle**. It is never shipped and never added to PATH, and it runs only on local files.
- Platform: Windows 10 x64. Paths can contain spaces and `&` (for example `DBC\S220&S237_...dbc`).
- Leave `html\*.html`, `js\*.js` and `style\` content unchanged. The only JS change is replacing `binder.js` with `cogent_gui\bridge.js`.
- Never write into `venv\`, `dist\`, `build\` or existing `*.pyc`. Run every Python 2.7 command with `-B`.
- Character encodings: DBC input and C/HTML/JS outputs use `latin-1` (byte-transparent, which matches Python 2 `str`). JSON `.data` files use `utf-8`.

## Review Focus

1. **A DBC containing bytes that cp1252 cannot decode** (the BAIC DBC has 286 high bytes). The parser must read it without `UnicodeDecodeError`. This is pinned in Task 3 (`test_parser_reads_dbc_with_undefined_cp1252_bytes`).
2. **Generate run twice in one session.** The second run must give identical files, and `sys.stdout` must be restored after each run. This is pinned in Task 4 (`test_generation_is_repeatable_in_process`).
3. **Windows path typed with backslashes or a quote** into the DBC field must reach `upload_dbc` unchanged. This is pinned in Task 6 (`test_form_submit_preserves_backslashes_and_quotes`).
4. **A generation failure** (saved data missing a key). The user must see the error alert, `errorlog.txt` must exist, and the Message page must still open afterwards. This is pinned in Task 7 (`test_generation_error_then_message_page_still_opens`).
5. **A rendered page larger than 2 MB** (`CAN_DBC_sig.html` is 3.4 MB) must display completely. This is pinned in Task 6 (`test_template_larger_than_2mb_loads`).

---

## File Structure

| Path | Status | Responsibility |
|---|---|---|
| `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini` | Create | Repo hygiene, pinned dependencies, pytest config. |
| `tools/gen_harness.py` | Create | **Py2/Py3-compatible** headless runner that mirrors `BackEnd.code_gen` and the page generators. |
| `tools/dump_dbc.py` | Create | Py2/Py3-compatible JSON dump of `dbc_parser` results. |
| `tools/build_fixtures.py` | Create | Extracts `data/*.data` from `.cfg` archives and copies the DBCs into `tests/fixtures/<name>/`. |
| `tools/make_expected.py` | Create | Runs the harness with Python 2.7 against the baseline tag and writes `tests/expected/<name>/`. |
| `tools/compare_legacy.py` | Create | One-off check: harness output vs `CODE_GEN\DBC_40024_2` (header-normalized). |
| `tools/find_divisions.py` | Create | Lists every `/` operator token (excludes strings and comments). |
| `tools/apply_output_helpers.py` | Create | Mechanical rewrite of the `open("./CODE_GEN/..")` + `sys.stdout = f` pairs. |
| `tests/support.py`, `tests/conftest.py` | Create | Shared helpers: fixture loading, harness invocation, byte comparison with diff. |
| `tests/test_generation_golden.py`, `tests/test_parser_parity.py`, `tests/test_parser_encoding.py`, `tests/test_pages_golden.py`, `tests/test_repeatable.py` | Create | Generation regression suite. |
| `tests/gui/test_webgui.py`, `tests/gui/test_gui_generate.py` | Create | In-process Qt tests (pytest-qt). |
| `tests/e2e/test_exe_smoke.py` | Create | Windows GUI test of the packaged exe (pywinauto, UIA). |
| `cogent_io.py` | Create | `open_output` / `close_output` for generators (encoding plus stdout restore). |
| `cogent_gui/__init__.py`, `cogent_gui/webgui.py`, `cogent_gui/bridge.js` | Create | htmlPy-compatible layer on PySide6. |
| `Dbc_Parser.pyw` → `Dbc_Parser.py` | Rename + modify | Py3 port. |
| `can_rx_filt_gen.py`, `msg.py`, `il_par_h_generation.py`, `il_par_c_generation.py`, `vnim_app_signals_par.py` | Modify | Py3 port. |
| `Can_dbc_gen.pyw` → `Can_dbc_gen.py`, `Can_filter_python_gen.pyw` → `Can_filter_python_gen.py` | Rename + modify | Py3 port. |
| `back_end.pyw` → `back_end.py`, `CoGeNT.pyw` | Rename/modify | Port onto `cogent_gui.webgui`. |
| `CoGeNT.spec` | Create | PyInstaller build (replaces `setup.py`/py2exe). |

Out of scope (left untouched; listed for the user): `w601_parser_gen.py` and `*_template.py` (Android HAL path, commented out in `code_gen`), `Configuration_Read_Parse_HTML.py` (dev-time xls→html), `ff\`, `testing\`, `setup.py`.

---

### Task 0: Repository baseline and toolchain

**Files:**
- Create: `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini`

**Interfaces:**
- Produces: git tag `py27-baseline` (untouched legacy source); `.venv312\Scripts\python.exe` (Python 3.12 + dev deps); `C:\Python27\python.exe` (oracle).

- [ ] **Step 1: Install Python 3.12.10 x64 (python.org) into `C:\Python312`** (per-user, no PATH change)

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Downloads\pyinst" | Out-Null
Invoke-WebRequest https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe -OutFile "$env:USERPROFILE\Downloads\pyinst\python-3.12.10-amd64.exe"
Start-Process "$env:USERPROFILE\Downloads\pyinst\python-3.12.10-amd64.exe" -Wait -ArgumentList '/quiet','InstallAllUsers=0','PrependPath=0','Include_launcher=0','Include_test=0','TargetDir=C:\Python312'
C:\Python312\python.exe --version
```
Expected: `Python 3.12.10`

- [ ] **Step 2: Install the Python 2.7.18 x64 oracle into `C:\Python27`** (this also makes the old `venv\` start again)

```powershell
Invoke-WebRequest https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi -OutFile "$env:USERPROFILE\Downloads\pyinst\python-2.7.18.amd64.msi"
Start-Process msiexec.exe -Wait -ArgumentList '/i',"$env:USERPROFILE\Downloads\pyinst\python-2.7.18.amd64.msi",'/passive','TARGETDIR=C:\Python27'
C:\Python27\python.exe -B -c "import sys; print(sys.version)"
```
Expected: `2.7.18 (v2.7.18:..., ...) [MSC v.1500 64 bit (AMD64)]`. Leave "Add python.exe to Path" off (it is off by default).

Optional, only to reproduce the legacy GUI by hand: `venv\Scripts\python.exe -m pip install "Jinja2==2.11.3" "MarkupSafe==1.1.1"`, then `venv\Scripts\python.exe CoGeNT.pyw`.

- [ ] **Step 3: Create the dev venv and install pinned packages**

`requirements.txt`:
```text
PySide6==6.11.2
Jinja2==3.1.6
```
`requirements-dev.txt`:
```text
-r requirements.txt
pytest==9.1.1
pytest-qt==4.5.0
pywinauto==0.6.9
pyinstaller==6.22.3
```
```powershell
C:\Python312\python.exe -m venv .venv312
.venv312\Scripts\python.exe -m pip install --upgrade pip
.venv312\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv312\Scripts\python.exe -c "import PySide6, jinja2; from PySide6 import QtWebEngineWidgets, QtWebChannel; print(PySide6.__version__, jinja2.__version__)"
```
Expected: `6.11.2 3.1.6`

- [ ] **Step 4: Add `.gitignore` and `pytest.ini`**

`.gitignore`:
```text
venv/
.venv*/
build/
dist/
__pycache__/
*.pyc
CODE_GEN/errorlog.txt
.idea/workspace.xml
```
`pytest.ini`:
```ini
[pytest]
testpaths = tests
qt_api = pyside6
markers =
    gui: in-process Qt GUI tests (needs an interactive desktop session)
    e2e: packaged-exe Windows GUI tests (pywinauto, UIA)
```

- [ ] **Step 5: Initialize Git and tag the untouched legacy source**

```powershell
git init
git add -A
git commit -m "chore: baseline of legacy Python 2.7 CoGeNT tool"
git tag py27-baseline
git status --short
```
Expected: clean tree. `git ls-files venv dist build | Measure-Object` reports 0.

---

### Task 1: Headless harness, fixtures, and harness self-check

**Files:**
- Create: `tools/gen_harness.py`, `tools/dump_dbc.py`, `tools/build_fixtures.py`, `tools/compare_legacy.py`
- Create (generated): `tests/fixtures/<name>/{fixture.json,data/*.data,<dbc>}`

**Interfaces:**
- Produces: `gen_harness.py --dbc PATH --node NAME --data DIR --out DIR --stage {code,pages,all} [--app-dir DIR]` (exit 0 on success, 1 with a traceback on stderr). `gen_harness.run(dbc, node, data_dir, out_dir, stage, app_dir)`. Constants `CODE_FILES`, `PAGE_FILES`. `dump_dbc.py DBC NODE` prints sorted JSON to stdout. `tests/fixtures/<name>/fixture.json` = `{"dbc": "<file name>", "node": "<node>", "source_cfg": "<repo-relative cfg>"}`.

- [ ] **Step 1: Write `tools/gen_harness.py`** (must run on Python 2.7 and 3.12)

```python
# -*- coding: utf-8 -*-
"""Headless driver for the CoGeNT pipeline. Mirrors BackEnd.code_gen() and the
page generators. Must stay Python 2.7 + 3.x compatible (it is also the oracle runner)."""
from __future__ import print_function

import argparse
import os
import shutil
import sys
import tempfile
import traceback

DEFAULT_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXED_TIME = "2000-01-01 00:00"
TEST_USER = "cogent-test"

CODE_FILES = [
    "can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
    "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
    "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h",
]
PAGE_FILES = [
    "html/CanDbcMsgConfiguration.html", "js/CanDbcMsgConfiguration.js",
    "html/CanDbcSigConfiguration.html", "js/CanDbcSigConfiguration.js",
    "html/CanFilterconfiguration.html", "js/CanFilterconfiguration.js",
]

# Same order and calls as back_end.BackEnd.code_gen
CODE_PLAN = [
    ("can_rx_filt_gen", ["filter_gen"]),
    ("msg", ["msg_struct_generation"]),
    ("il_par_h_generation", ["il_par_h_gen_function"]),
    ("il_par_c_generation", ["il_par_c_gen_function"]),
    ("vnim_app_signals_par", ["vnim_app_c_gen", "vnim_app_h_gen", "vnim_resource_gen", "nm_par_gen"]),
]


def _run_code(dbc, node, real_stdout):
    for module_name, funcs in CODE_PLAN:
        mod = __import__(module_name)
        mod.set_file_node_il(dbc, node)
        mod.set_init_global(FIXED_TIME)
        for name in funcs:
            getattr(mod, name)()
            sys.stdout = real_stdout


def _run_pages(dbc, node, real_stdout):
    dbc_gen = __import__("Can_dbc_gen")
    filt = __import__("Can_filter_python_gen")
    dbc_gen.html_mes(dbc, node)
    dbc_gen.html_sig(dbc, node)
    filt.html(dbc, node)
    sys.stdout = real_stdout


def run(dbc, node, data_dir, out_dir, stage="code", app_dir=DEFAULT_APP_DIR):
    dbc = os.path.abspath(dbc).replace("\\", "/")
    app_dir = os.path.abspath(app_dir)
    work = tempfile.mkdtemp(prefix="cogent_")
    old_cwd, real_stdout = os.getcwd(), sys.stdout
    os.environ["LOGNAME"] = TEST_USER  # getpass.getuser() checks LOGNAME first
    try:
        shutil.copytree(os.path.abspath(data_dir), os.path.join(work, "data"))
        for sub in ("html", "js"):
            shutil.copytree(os.path.join(app_dir, sub), os.path.join(work, sub))
        if app_dir not in sys.path:
            sys.path.insert(0, app_dir)
        os.chdir(work)
        try:
            if stage in ("code", "all"):
                _run_code(dbc, node, real_stdout)
            if stage in ("pages", "all"):
                _run_pages(dbc, node, real_stdout)
        finally:
            sys.stdout = real_stdout
            os.chdir(old_cwd)
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)
        if stage in ("code", "all"):
            for name in CODE_FILES:
                shutil.copy2(os.path.join(work, "CODE_GEN", name), os.path.join(out_dir, name))
        if stage in ("pages", "all"):
            for rel in PAGE_FILES:
                shutil.copy2(os.path.join(work, rel), os.path.join(out_dir, os.path.basename(rel)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dbc", required=True)
    p.add_argument("--node", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--stage", choices=["code", "pages", "all"], default="code")
    p.add_argument("--app-dir", default=DEFAULT_APP_DIR)
    a = p.parse_args(argv)
    try:
        run(a.dbc, a.node, a.data, a.out, a.stage, a.app_dir)
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Write `tools/dump_dbc.py`** (Python 2.7 + 3)

```python
# -*- coding: utf-8 -*-
"""Dump dbc_parser results as sorted JSON (oracle comparison of the parser)."""
from __future__ import print_function

import json
import os
import sys

APP_DIR = os.environ.get("COGENT_APP_DIR",
                         os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, APP_DIR)
from Dbc_Parser import dbc_parser  # noqa: E402


def dump(dbc, node):
    result = {"node_ok": dbc_parser(dbc, node).check__node(),
              "enums": dbc_parser(dbc, node).get_enum_values()}
    for msg_type in ("GenMsgILSupport", "ALL"):
        for direction in ("tx", "rx"):
            key = "%s/%s" % (msg_type, direction)
            result[key] = dbc_parser(dbc, node).get_msg_type(msg_type, direction)
    return result


if __name__ == "__main__":
    kwargs = {"encoding": "latin-1"} if sys.version_info[0] == 2 else {}
    print(json.dumps(dump(sys.argv[1], sys.argv[2]), sort_keys=True, indent=1, **kwargs))
```

- [ ] **Step 3: Write `tools/build_fixtures.py`** (Python 3)

```python
"""Build tests/fixtures/<name>/ from saved .cfg archives + DBC files in the repo."""
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "fixtures"
FIXTURES = [
    ("s2xx_40024", "CODE_GEN/DBC_40024_2/26-02-2026_17-37-49.cfg",
     "CODE_GEN/DBC_40024_2/S2XX_SMART_CORE_SVNID_40024_25_02_2026.dbc", "SMART_CORE"),
    ("s237_35354", "Config/Config_DBC_35354_1.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev35354_180923_Edited.dbc", "SMART_CORE"),
    ("s237_35891", "Config/Config_DBC_35891.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev35891_111223_Edited.dbc", "SMART_CORE"),
    ("s237_36026", "Config/Config_DBC_36026.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36026_110124_Edited.dbc", "SMART_CORE"),
    ("s237_36144", "Config/Config_DBC_36144.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc", "SMART_CORE"),
    ("s237_100723", "Config/Config_S237_Common_DBC_Itr12.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_100723_Edited.dbc", "SMART_CORE"),
]


def build(name, cfg, dbc, node):
    dst = OUT / name
    if dst.exists():
        shutil.rmtree(dst)
    (dst / "data").mkdir(parents=True)
    with zipfile.ZipFile(ROOT / cfg) as z:
        members = [m for m in z.namelist() if m.startswith("data/") and m.endswith(".data")]
        for m in members:
            (dst / "data" / Path(m).name).write_bytes(z.read(m))
    if not (dst / "data" / "CanDbcMsgConfiguration.data").exists():
        raise SystemExit(f"{cfg}: no data/CanDbcMsgConfiguration.data")
    shutil.copy2(ROOT / dbc, dst / Path(dbc).name)
    meta = {"dbc": Path(dbc).name, "node": node, "source_cfg": cfg}
    (dst / "fixture.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{name}: {len(members)} data files")


if __name__ == "__main__":
    for row in FIXTURES:
        build(*row)
```
Run: `.venv312\Scripts\python.exe tools\build_fixtures.py`
Expected: 6 lines, each `<name>: 4 data files`.

- [ ] **Step 4: Write `tools/compare_legacy.py`** (Python 3; header-normalized compare against a real previous GUI run)

```python
"""Compare harness output with a legacy CODE_GEN run, ignoring Date/By/Traceability lines."""
import re
import sys
from pathlib import Path

HEADER = re.compile(rb"^(Date|By|Traceability)[ \t]*:.*$", re.M)


def norm(path):
    return HEADER.sub(lambda m: m.group(1) + b": <normalized>", path.read_bytes())


def main(actual_dir, legacy_dir):
    bad = 0
    for f in sorted(Path(legacy_dir).iterdir()):
        a = Path(actual_dir) / f.name
        if f.suffix == ".cfg" and f.name != "can_rxrule.cfg":
            continue  # saved config archive, not an output
        if f.suffix == ".dbc" or f.suffix == ".ini":
            continue
        same = a.exists() and norm(a) == norm(f)
        bad += not same
        print(f"{'OK  ' if same else 'DIFF'} {f.name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
```

- [ ] **Step 5: Self-check the harness with the oracle against the legacy run**

```powershell
C:\Python27\python.exe -B tools\gen_harness.py --dbc "tests\fixtures\s2xx_40024\S2XX_SMART_CORE_SVNID_40024_25_02_2026.dbc" --node SMART_CORE --data tests\fixtures\s2xx_40024\data --out "$env:TEMP\cogent_selfcheck" --stage code
.venv312\Scripts\python.exe tools\compare_legacy.py "$env:TEMP\cogent_selfcheck" CODE_GEN\DBC_40024_2
```
Expected: exit 0 from the harness, then 11 `OK` lines. If there are `DIFF` lines, the likely cause is the DBC itself: the run used `..._Edited.dbc`, but the repo copy lacks `_Edited`. Diff the two outputs (`git diff --no-index`). Record the result in `tests/fixtures/README.md`. Continue in either case, because the oracle (not this legacy run) is the reference.

- [ ] **Step 6: Commit**

```powershell
git add tools tests/fixtures
git commit -m "test: add headless generation harness and DBC/config fixtures"
```

---

### Task 2: Python 2.7 expected outputs and the golden test suite (red on Python 3)

**Files:**
- Create: `tools/make_expected.py`, `tests/support.py`, `tests/conftest.py`, `tests/test_generation_golden.py`, `tests/test_parser_parity.py`, `tests/test_pages_golden.py`, `tests/accepted_order_diffs.json`
- Create (generated): `tests/expected/<name>/{code/*,pages/*,parser.json}`

**Interfaces:**
- Consumes: `gen_harness.py` CLI, `dump_dbc.py`, `tests/fixtures/*/fixture.json` (Task 1).
- Produces: `tests.support`: `ROOT`, `FIXTURES`, `EXPECTED`, `CODE_FILES`, `PAGE_FILES`, `Fixture(name, dir, dbc, node, data_dir)`, `load_fixture(name) -> Fixture`, `fixture_names() -> list[str]`, `run_harness(python, fx, out, stage) -> None`, `assert_same_file(actual: Path, expected: Path, key: tuple[str, str]) -> None`. The `generated(name, stage) -> Path` pytest fixture (session-cached).

- [ ] **Step 1: Write `tools/make_expected.py`**. It runs the oracle against a worktree of tag `py27-baseline`, so it still works after the source is ported.

```python
"""Generate tests/expected/<fixture>/ with the Python 2.7 oracle on the py27-baseline tag."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY27 = os.environ.get("COGENT_PY27", r"C:\Python27\python.exe")
BASE = ROOT / ".baseline-worktree"


def main():
    if not BASE.exists():
        subprocess.run(["git", "worktree", "add", "--detach", str(BASE), "py27-baseline"], check=True, cwd=ROOT)
    harness = ROOT / "tools" / "gen_harness.py"
    dump = ROOT / "tools" / "dump_dbc.py"
    for fdir in sorted((ROOT / "tests" / "fixtures").iterdir()):
        meta_file = fdir / "fixture.json"
        if not meta_file.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        exp = ROOT / "tests" / "expected" / fdir.name
        dbc = fdir / meta["dbc"]
        for stage in ("code", "pages"):
            subprocess.run([PY27, "-B", str(harness), "--dbc", str(dbc), "--node", meta["node"],
                            "--data", str(fdir / "data"), "--out", str(exp / stage),
                            "--stage", stage, "--app-dir", str(BASE)], check=True)
        env = dict(os.environ, COGENT_APP_DIR=str(BASE))
        out = subprocess.run([PY27, "-B", str(dump), str(dbc), meta["node"]],
                             check=True, capture_output=True, env=env).stdout
        (exp / "parser.json").write_bytes(out)
        print(f"{fdir.name}: ok")


if __name__ == "__main__":
    sys.exit(main())
```
Add `.baseline-worktree/` to `.gitignore`.

Run: `.venv312\Scripts\python.exe tools\make_expected.py`
Expected: 6 lines `<name>: ok`. Each `tests/expected/<name>/code` holds 11 files, `pages` holds 6, plus `parser.json`.

- [ ] **Step 2: Write `tests/support.py`**

```python
import difflib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
EXPECTED = ROOT / "tests" / "expected"
HARNESS = ROOT / "tools" / "gen_harness.py"
DUMP = ROOT / "tools" / "dump_dbc.py"
ACCEPTED = ROOT / "tests" / "accepted_order_diffs.json"

CODE_FILES = [
    "can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
    "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
    "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h",
]
PAGE_FILES = [
    "CanDbcMsgConfiguration.html", "CanDbcMsgConfiguration.js",
    "CanDbcSigConfiguration.html", "CanDbcSigConfiguration.js",
    "CanFilterconfiguration.html", "CanFilterconfiguration.js",
]


@dataclass(frozen=True)
class Fixture:
    name: str
    dir: Path
    dbc: Path
    node: str
    data_dir: Path


def fixture_names():
    if not FIXTURES.exists():
        return []
    return sorted(p.name for p in FIXTURES.iterdir() if (p / "fixture.json").exists())


def load_fixture(name):
    d = FIXTURES / name
    meta = json.loads((d / "fixture.json").read_text(encoding="utf-8"))
    return Fixture(name, d, d / meta["dbc"], meta["node"], d / "data")


def run_harness(python, fx, out, stage):
    cmd = [str(python), "-B", str(HARNESS), "--dbc", str(fx.dbc), "--node", fx.node,
           "--data", str(fx.data_dir), "--out", str(out), "--stage", stage]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        pytest.fail(f"harness failed for {fx.name}/{stage}:\n{r.stderr[-4000:]}")


def _accepted():
    if not ACCEPTED.exists():
        return set()
    return {tuple(x) for x in json.loads(ACCEPTED.read_text(encoding="utf-8"))}


def assert_same_file(actual, expected, key):
    a, e = actual.read_bytes(), expected.read_bytes()
    if a == e:
        return
    al = a.decode("latin-1").splitlines()
    el = e.decode("latin-1").splitlines()
    order_only = sorted(al) == sorted(el)
    if order_only and tuple(key) in _accepted():
        return
    diff = "\n".join(list(difflib.unified_diff(el, al, "expected(py27)", "actual", lineterm="", n=2))[:80])
    kind = "ORDER-ONLY" if order_only else "CONTENT"
    pytest.fail(f"{actual.name} differs ({kind}) for {key}:\n{diff}")


HEADER_DATE_BY = re.compile(rb"^(Date|By)[ \t]*:.*$", re.M)


def normalize_date_by(data):
    return HEADER_DATE_BY.sub(lambda m: m.group(1) + b": <normalized>", data)
```

- [ ] **Step 3: Write `tests/conftest.py`**

```python
import os
import sys

import pytest

os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from support import load_fixture, run_harness  # noqa: E402


@pytest.fixture(scope="session")
def generated(tmp_path_factory):
    cache = {}

    def get(name, stage):
        if (name, stage) not in cache:
            out = tmp_path_factory.mktemp(f"{name}_{stage}") / "out"
            run_harness(sys.executable, load_fixture(name), out, stage)
            cache[(name, stage)] = out
        return cache[(name, stage)]

    return get
```

- [ ] **Step 4: Write the golden tests**

`tests/test_generation_golden.py`:
```python
import pytest

from support import CODE_FILES, EXPECTED, assert_same_file, fixture_names


@pytest.mark.parametrize("fname", CODE_FILES)
@pytest.mark.parametrize("name", fixture_names())
def test_code_output_matches_py27(generated, name, fname):
    expected = EXPECTED / name / "code" / fname
    if not expected.exists():
        pytest.skip("run tools/make_expected.py")
    assert_same_file(generated(name, "code") / fname, expected, (name, fname))
```
`tests/test_pages_golden.py`:
```python
import pytest

from support import EXPECTED, PAGE_FILES, assert_same_file, fixture_names


@pytest.mark.parametrize("fname", PAGE_FILES)
@pytest.mark.parametrize("name", fixture_names())
def test_page_output_matches_py27(generated, name, fname):
    expected = EXPECTED / name / "pages" / fname
    if not expected.exists():
        pytest.skip("run tools/make_expected.py")
    assert_same_file(generated(name, "pages") / fname, expected, (name, fname))
```
`tests/test_parser_parity.py`:
```python
import json
import subprocess
import sys

import pytest

from support import DUMP, EXPECTED, fixture_names, load_fixture


@pytest.mark.parametrize("name", fixture_names())
def test_parser_matches_py27(name):
    fx = load_fixture(name)
    r = subprocess.run([sys.executable, "-B", str(DUMP), str(fx.dbc), fx.node], capture_output=True)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[-4000:]
    assert json.loads(r.stdout) == json.loads((EXPECTED / name / "parser.json").read_bytes())
```
`tests/accepted_order_diffs.json`:
```json
[]
```

- [ ] **Step 5: Run the suite on Python 3 and confirm it is red for the right reason**

Run: `.venv312\Scripts\python.exe -m pytest tests -q -x --ignore=tests/gui --ignore=tests/e2e`
Expected: FAIL. The first failure is the harness or `dump_dbc` reporting `SyntaxError: Missing parentheses in call to 'print'` (or `AttributeError: '_io.TextIOWrapper' object has no attribute 'next'` from `Dbc_Parser`).

- [ ] **Step 6: Commit**

```powershell
git add tools/make_expected.py tests .gitignore
git commit -m "test: golden byte-comparison suite against Python 2.7 oracle"
```

---

### Task 3: Port `Dbc_Parser` to Python 3

**Files:**
- Rename: `Dbc_Parser.pyw` → `Dbc_Parser.py` (`git mv`)
- Modify: `Dbc_Parser.py` (the 3 `open(self.dbc,'r')` calls and the 4 `temp_file.next()` calls)
- Test: `tests/test_parser_encoding.py`, `tests/test_parser_parity.py`

**Interfaces:**
- Produces: `Dbc_Parser.dbc_parser(dbc, node)` with an unchanged public API (`get_msg_type`, `check__node`, `check_parsing`, `get_enum_values`, `msg_name`, `mes_count`, `get_IL_rx_id`).

- [ ] **Step 1: Write the failing encoding test** `tests/test_parser_encoding.py`

```python
import sys

from support import ROOT

DBC = ROOT / "DBC" / "S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc"


def test_parser_reads_dbc_with_undefined_cp1252_bytes(tmp_path):
    dbc = tmp_path / "weird.dbc"
    dbc.write_bytes(DBC.read_bytes() + b'\r\nCM_ "bytes \x81\x8d\x90 not in cp1252";\r\n')
    sys.path.insert(0, str(ROOT))
    from Dbc_Parser import dbc_parser
    assert dbc_parser(str(dbc), "SMART_CORE").check_parsing() is True
    assert dbc_parser(str(dbc), "SMART_CORE").check__node() is True
```

- [ ] **Step 2: Run it to verify it fails**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_parser_encoding.py tests/test_parser_parity.py -q`
Expected: FAIL (`check_parsing() is False`, because `.next()` raises inside the guarded call; parity fails with `AttributeError`).

- [ ] **Step 3: Port**

```powershell
git mv Dbc_Parser.pyw Dbc_Parser.py
.venv312\Scripts\python.exe -W ignore -m lib2to3 -f next -w -n --no-diffs Dbc_Parser.py
```
Then, in `Dbc_Parser.py`, replace each of the 3 occurrences of
```python
temp_file=open(self.dbc,'r')
```
with
```python
temp_file=open(self.dbc,'r',encoding='latin-1')
```
Verify: `Select-String Dbc_Parser.py -Pattern "open\(self.dbc"` shows 3 lines, all with `encoding='latin-1'`. `Select-String Dbc_Parser.py -Pattern "\.next\("` shows nothing.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_parser_encoding.py tests/test_parser_parity.py -q`
Expected: 7 passed.

- [ ] **Step 5: Commit**

```powershell
git add -A Dbc_Parser.py Dbc_Parser.pyw tests/test_parser_encoding.py
git commit -m "port: Dbc_Parser to Python 3 (next(), latin-1 DBC decoding)"
```

---

### Task 4: Port the five code generators

**Files:**
- Create: `cogent_io.py`, `tools/find_divisions.py`, `tools/apply_output_helpers.py`, `tests/test_repeatable.py`
- Modify: `can_rx_filt_gen.py`, `msg.py`, `il_par_h_generation.py`, `il_par_c_generation.py`, `vnim_app_signals_par.py`

**Interfaces:**
- Consumes: `Dbc_Parser.dbc_parser` (Task 3).
- Produces: `cogent_io.open_output(file_name: str) -> TextIO` (creates `./CODE_GEN`, opens `./CODE_GEN/<file_name>` as latin-1 for writing, sets `sys.stdout`). `cogent_io.close_output(f) -> None` (closes `f` and restores `sys.stdout = sys.__stdout__`). The generator module functions keep their names (`set_file_node_il`, `set_init_global`, `filter_gen`, `msg_struct_generation`, `il_par_h_gen_function`, `il_par_c_gen_function`, `vnim_app_c_gen`, `vnim_app_h_gen`, `vnim_resource_gen`, `nm_par_gen`).

- [ ] **Step 1: Write the failing repeatability test** `tests/test_repeatable.py`

```python
import importlib.util
import sys

from support import CODE_FILES, ROOT, load_fixture


def _harness():
    spec = importlib.util.spec_from_file_location("gen_harness", ROOT / "tools" / "gen_harness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_generation_is_repeatable_in_process(tmp_path):
    h, fx = _harness(), load_fixture("s237_36144")
    before = sys.stdout
    h.run(str(fx.dbc), fx.node, str(fx.data_dir), str(tmp_path / "a"), "code")
    assert sys.stdout is before
    h.run(str(fx.dbc), fx.node, str(fx.data_dir), str(tmp_path / "b"), "code")
    assert sys.stdout is before
    for name in CODE_FILES:
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes(), name
```

- [ ] **Step 2: Run the golden and repeatability tests to verify they fail**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_generation_golden.py tests/test_repeatable.py -q -x`
Expected: FAIL with `SyntaxError` (print statement) from `can_rx_filt_gen.py`.

- [ ] **Step 3: Convert `print` statements**

```powershell
.venv312\Scripts\python.exe -W ignore -m lib2to3 -f print -w -n --no-diffs can_rx_filt_gen.py msg.py il_par_h_generation.py il_par_c_generation.py vnim_app_signals_par.py
foreach ($f in 'can_rx_filt_gen.py','msg.py','il_par_h_generation.py','il_par_c_generation.py','vnim_app_signals_par.py') { .venv312\Scripts\python.exe -m py_compile $f }
```
Expected: no output from `py_compile`.

- [ ] **Step 4: Create `cogent_io.py`**

```python
"""Output helpers for the code generators: fixed encoding and guaranteed stdout restore."""
import os
import sys

CODE_GEN_DIR = './CODE_GEN'


def open_output(file_name):
    if not os.path.exists(CODE_GEN_DIR):
        os.mkdir(CODE_GEN_DIR)
    f = open(CODE_GEN_DIR + '/' + file_name, 'w', encoding='latin-1')
    sys.stdout = f
    return f


def close_output(f):
    f.close()
    sys.stdout = sys.__stdout__
```

- [ ] **Step 5: Rewrite the open/redirect/close sites** with `tools/apply_output_helpers.py`

```python
"""Replace  f=open("./CODE_GEN/X",'w') + sys.stdout = f  with  f=open_output("X"),
and f.close() with close_output(f); add the import. Prints counts for review."""
import re
import sys
from pathlib import Path

EOL = r"[ \t]*(?=\r?$)"
OPEN = re.compile(r"""^(?P<ind>[ \t]*)f\s*=\s*open\(\s*["']\./CODE_GEN/(?P<name>[^"']+)["']\s*,\s*["']w\+?["']\s*\)[ \t]*\r?\n[ \t]*sys\.stdout\s*=\s*f""" + EOL, re.M)
CLOSE = re.compile(r"^(?P<ind>[ \t]*)f\.close\(\)" + EOL, re.M)
DATA = re.compile(r"""open\((?P<arg>\w+_data_dir\s*\+\s*["'][^"']+\.data["'])\s*,\s*'r'\)""")
IMPORT_OS = re.compile(r"^import os(?P<nl>\r?\n)", re.M)

for path in map(Path, sys.argv[1:]):
    with open(path, encoding="latin-1", newline="") as fh:   # keep CRLF/LF exactly
        src = fh.read()
    src, n_open = OPEN.subn(lambda m: f'{m["ind"]}f=open_output("{m["name"]}")', src)
    src, n_close = CLOSE.subn(lambda m: f'{m["ind"]}close_output(f)', src)
    src, n_data = DATA.subn(lambda m: f"open({m['arg']},'r',encoding='utf-8')", src)
    src, n_imp = IMPORT_OS.subn(lambda m: "import os" + m["nl"] + "from cogent_io import open_output, close_output" + m["nl"], src, count=1)
    with open(path, "w", encoding="latin-1", newline="") as fh:
        fh.write(src)
    print(f"{path}: open_output={n_open} close_output={n_close} data_reads={n_data} import_added={n_imp}")
```
Run:
```powershell
.venv312\Scripts\python.exe tools\apply_output_helpers.py can_rx_filt_gen.py msg.py il_par_h_generation.py il_par_c_generation.py vnim_app_signals_par.py
Select-String can_rx_filt_gen.py,msg.py,il_par_h_generation.py,il_par_c_generation.py,vnim_app_signals_par.py -Pattern 'CODE_GEN/|sys\.stdout'
```
Expected: in each file, `open_output` count == `close_output` count, both are ≥ 1, and `import_added=1`. After the rewrite, the `Select-String` shows no `open("./CODE_GEN/...` and no `sys.stdout = f` lines. If a count mismatches, open that file at the remaining `f.close()` / `open(` line and fix it by hand using the same two forms.

Note: the script keeps the source's line endings. Output files are still written with Windows `\r\n` because `open_output` uses the default newline translation (this matches Python 2 text mode).

- [ ] **Step 6: Fix integer division.** List every `/` operator.

`tools/find_divisions.py`:
```python
"""List '/' and '/=' operator tokens (strings and comments excluded)."""
import sys
import tokenize

for path in sys.argv[1:]:
    with open(path, "rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type == tokenize.OP and tok.string in ("/", "/="):
                print(f"{path}:{tok.start[0]}:{tok.start[1] + 1}: {tok.line.strip()}")
```
Run: `.venv312\Scripts\python.exe tools\find_divisions.py can_rx_filt_gen.py msg.py il_par_h_generation.py il_par_c_generation.py vnim_app_signals_par.py`
Expected: about 95 hits (il_par_c ≈ 47, il_par_h ≈ 28, msg ≈ 18, can_rx_filt_gen 2).

For **each** hit, change `/` to `//` (and `/=` to `//=`). Every expected operand is an `int` (bit position, `len()`, signal length). If an operand could be a DBC factor or offset (a float in the DBC), do **not** change it; stop and list it for review. Re-run the finder.
Expected: 0 hits, or only the reviewed float sites.

- [ ] **Step 7: Fix the remaining Python 2-only call**

In `vnim_app_signals_par.py`, replace
```python
diag_id=max(list_dict.iterkeys(), key=lambda k: list_dict[k])
```
with
```python
diag_id=max(list_dict.keys(), key=lambda k: list_dict[k])
```
Check: `Select-String *.py -Pattern 'iteritems|iterkeys|itervalues|has_key|xrange|basestring|unicode\(' | ? Filename -in 'can_rx_filt_gen.py','msg.py','il_par_h_generation.py','il_par_c_generation.py','vnim_app_signals_par.py'`
Expected: no matches.

- [ ] **Step 8: Run the golden and repeatability tests**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_generation_golden.py tests/test_repeatable.py -q`
Expected: 67 passed (6 × 11 + 1).

Triage rules for failures (fix in source, then re-run):
- `CONTENT` diff showing `.0` in numbers, or `TypeError: list indices must be integers`: a missed `/`. Go back to Step 6.
- `CONTENT` diff with a missing or extra space at a line end: a `print x,` softspace difference (2 sites in `vnim_app_signals_par.py`). Replace that pair with an explicit `sys.stdout.write(...)` that reproduces the oracle bytes.
- `TypeError: '<' not supported between instances`: Python 2 compared mixed types. Make the sort key explicit (for example `key=lambda x: int(x['Endbit'])`) so that it yields the oracle order.
- `ORDER-ONLY` diff: an unsorted `for k in <dict>` loop now follows Python 3 insertion order. First try to make the loop reproduce the oracle order deterministically (for example, if the oracle order equals `sorted(...)` order, sort it). If no deterministic rule reproduces it, **stop and ask the user** whether to accept the new order. Only then add `["<fixture>", "<file>"]` to `tests/accepted_order_diffs.json`.

- [ ] **Step 9: Commit**

```powershell
git add cogent_io.py tools/find_divisions.py tools/apply_output_helpers.py tests/test_repeatable.py can_rx_filt_gen.py msg.py il_par_h_generation.py il_par_c_generation.py vnim_app_signals_par.py tests/accepted_order_diffs.json
git commit -m "port: code generators to Python 3 with byte-identical output"
```

---

### Task 5: Port the page generators

**Files:**
- Rename + modify: `Can_dbc_gen.pyw` → `Can_dbc_gen.py`, `Can_filter_python_gen.pyw` → `Can_filter_python_gen.py`
- Test: `tests/test_pages_golden.py` (from Task 2)

**Interfaces:**
- Produces: `Can_dbc_gen.html_mes(dbc, node)`, `Can_dbc_gen.html_sig(dbc, node)`, `Can_filter_python_gen.html(dbc, node)`, all unchanged.

- [ ] **Step 1: Run the page tests to verify they fail**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_pages_golden.py -q -x`
Expected: FAIL (harness `--stage pages` raises a Python 3 error from `Can_dbc_gen`).

- [ ] **Step 2: Rename and convert**

```powershell
git mv Can_dbc_gen.pyw Can_dbc_gen.py
git mv Can_filter_python_gen.pyw Can_filter_python_gen.py
.venv312\Scripts\python.exe -W ignore -m lib2to3 -f print -f next -f has_key -w -n --no-diffs Can_dbc_gen.py Can_filter_python_gen.py
Select-String Can_dbc_gen.py,Can_filter_python_gen.py -Pattern "open\("
```

- [ ] **Step 3: Set explicit encodings on every `open(` listed in Step 2.** Use `encoding='latin-1'` for `.html` and `.js` reads and writes, and `encoding='utf-8'` for `.data` reads. For example:
```python
file1=open(html_dir+'Tool_Index_Page.html','r',encoding='latin-1')
html= open(html_dir+'CanDbcMsgConfiguration.html', 'w',encoding='latin-1')
jscript = open(java_dir+'CanDbcMsgConfiguration.js', 'w',encoding='latin-1')
vnim_cfg_file = open(data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
```
Then run `.venv312\Scripts\python.exe tools\find_divisions.py Can_dbc_gen.py Can_filter_python_gen.py` and apply the same `//` rule as Task 4 Step 6.

- [ ] **Step 4: Run the page tests**

Run: `.venv312\Scripts\python.exe -m pytest tests/test_pages_golden.py -q`
Expected: 36 passed. Triage failures with the Task 4 Step 8 rules.

- [ ] **Step 5: Commit**

```powershell
git add -A Can_dbc_gen.py Can_dbc_gen.pyw Can_filter_python_gen.py Can_filter_python_gen.pyw
git commit -m "port: HTML/JS page generators to Python 3"
```

---

### Task 6: htmlPy-compatible GUI shim on PySide6

**Files:**
- Create: `cogent_gui/__init__.py` (empty), `cogent_gui/webgui.py`, `cogent_gui/bridge.js`
- Test: `tests/gui/test_webgui.py`

**Interfaces:**
- Produces, in `cogent_gui.webgui`: `Object` (= `QObject`), `Slot` (= `PySide6.QtCore.Slot`), and `settings.DISABLE/ENABLE`. `AppGUI(title="", maximized=False)` provides:
  - Attributes: `.window: QMainWindow`, `.web_app: QWebEngineView`, `.page`, `.template_path: str`, `.static_path: str`, `.maximized: bool`, `.allow_overwrite`, `.alerts: list[str]`, `.console: list[tuple]`, `.alert_handler: Callable[[str], None] | None`.
  - Methods: `.bind(obj, variable_name=None)`, the `.template` property `(name, context)`, `.evaluate_javascript(js) -> None` (queued until the current load finishes), `.right_click_setting(value)`, `.start() -> int`.
  - JS side: `window.<BoundName>.<slot>(...)` is usable at any time (calls are queued until the channel is ready), and `window.__cogentReady === true` once ready.

- [ ] **Step 1: Write the failing shim tests** `tests/gui/test_webgui.py`

```python
import json

import pytest
from PySide6.QtCore import QObject, Slot

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


def test_staticfile_filter_points_to_static_path(qtbot, gui):
    (gui.tmp / "s.css").write_text("#m{width:123px}", encoding="utf-8")
    show(qtbot, gui, "f.html", '<link rel="stylesheet" href="{{\'s.css\'|staticfile}}"><body><div id="m"></div></body>')
    assert js(qtbot, gui, "getComputedStyle(document.getElementById('m')).width") == "123px"
```

- [ ] **Step 2: Run them to verify they fail**

Run: `.venv312\Scripts\python.exe -m pytest tests/gui/test_webgui.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'cogent_gui'`.

- [ ] **Step 3: Write `cogent_gui/bridge.js`**. It replaces htmlPy's `binder.js` with the same `data-bind` semantics, but without `eval`, with `getAttribute`, and with a `MutationObserver`.

```javascript
(function () {
  "use strict";
  var names = window.__cogentObjects || [];
  var ready = false, queue = [], objects = {};

  function callSlot(objName, method, args) {
    var target = objects[objName];
    if (!target || typeof target[method] !== "function") {
      console.error("cogent: unknown slot " + objName + "." + method);
      return;
    }
    target[method].apply(target, args);
  }

  names.forEach(function (objName) {
    window[objName] = new Proxy({}, {
      get: function (_t, method) {
        return function () {
          var args = Array.prototype.slice.call(arguments);
          if (ready) { callSlot(objName, method, args); } else { queue.push([objName, method, args]); }
        };
      }
    });
  });

  new QWebChannel(qt.webChannelTransport, function (channel) {
    objects = channel.objects;
    ready = true;
    var pending = queue; queue = [];
    pending.forEach(function (c) { callSlot(c[0], c[1], c[2]); });
    window.__cogentReady = true;
  });

  function resolveSlot(path) {
    var parts = String(path || "").split(".");
    if (parts.length !== 2 || names.indexOf(parts[0]) < 0) {
      console.error("cogent: not a bound slot: " + path);
      return null;
    }
    return function () { window[parts[0]][parts[1]].apply(null, arguments); };
  }

  function linkBind(e) {
    e.preventDefault();
    var anchor = e.currentTarget;
    if (anchor.getAttribute("data-bind") !== "true") { return true; }
    var slot = resolveSlot(anchor.getAttribute("href"));
    if (!slot) { return false; }
    var params = anchor.getAttribute("data-params");
    if (params !== null) { slot(params); } else { slot(); }
    return false;
  }

  function formBind(e) {
    e.preventDefault();
    var form = e.currentTarget;
    if (form.getAttribute("data-bind") !== "true") { return true; }
    var slot = resolveSlot(form.getAttribute("action"));
    if (!slot) { return false; }
    var formdata = {};
    for (var i = 0, ii = form.length; i < ii; ++i) {
      var input = form[i];
      if (input.name && input.type !== "file") { formdata[input.name] = input.value; }
    }
    var params = form.getAttribute("data-params");
    if (params !== null) { slot(JSON.stringify(formdata), params); } else { slot(JSON.stringify(formdata)); }
    return false;
  }

  function bindAll() {
    var anchors = document.getElementsByTagName("a");
    for (var i = anchors.length - 1; i >= 0; i--) {
      if (!anchors[i].classList.contains("htmlpy-activated")) {
        anchors[i].onclick = linkBind;
        anchors[i].classList.add("htmlpy-activated");
      }
    }
    var forms = document.getElementsByTagName("form");
    for (var f = forms.length - 1; f >= 0; f--) {
      if (!forms[f].classList.contains("htmlpy-activated")) {
        forms[f].onsubmit = formBind;
        forms[f].classList.add("htmlpy-activated");
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindAll();
    new MutationObserver(bindAll).observe(document.body, { childList: true, subtree: true });
    document.body.classList.add("htmlPy-active");
  });
})();
```
`<input type="file">` appears only in `Home_page.html` and `Tool_Index_Page_1.html`, which the app never renders. File inputs are therefore excluded from the payload (as in the legacy binder), and no `GUIHelper.file_dialog` is provided.

- [ ] **Step 4: Write `cogent_gui/webgui.py`**

```python
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
        self._render_dir = tempfile.mkdtemp(prefix="cogent_render_")

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
```

- [ ] **Step 5: Run the shim tests**

Run: `.venv312\Scripts\python.exe -m pytest tests/gui/test_webgui.py -q`
Expected: 7 passed.

- [ ] **Step 6: Commit**

```powershell
git add cogent_gui tests/gui/test_webgui.py
git commit -m "feat: htmlPy-compatible GUI shim on PySide6 QtWebEngine/QWebChannel"
```

---

### Task 7: Port `back_end` and `CoGeNT` onto the shim; in-process GUI generation test

**Files:**
- Rename + modify: `back_end.pyw` → `back_end.py`
- Modify: `CoGeNT.pyw`
- Test: `tests/gui/test_gui_generate.py`

**Interfaces:**
- Consumes: `cogent_gui.webgui` (Task 6), the generators (Tasks 4–5), and `tests.support` (Task 2).
- Produces: `back_end.app: webgui.AppGUI` and `back_end.BackEnd` with the same slot names and signatures as before.

- [ ] **Step 1: Write the failing GUI tests** `tests/gui/test_gui_generate.py`

```python
import importlib
import json
import os
import shutil
import sys

import pytest

from support import CODE_FILES, EXPECTED, ROOT, load_fixture, normalize_date_by

pytestmark = pytest.mark.gui
APP_ITEMS = ["CoGeNT.pyw", "back_end.py", "Dbc_Parser.py", "Can_dbc_gen.py", "Can_filter_python_gen.py",
             "can_rx_filt_gen.py", "msg.py", "il_par_h_generation.py", "il_par_c_generation.py",
             "vnim_app_signals_par.py", "cogent_io.py", "batman.ico", "cogent_gui", "html", "js", "style"]


@pytest.fixture(scope="module")
def app_copy(tmp_path_factory):
    home = tmp_path_factory.mktemp("cogent_home")
    for item in APP_ITEMS:
        src = ROOT / item
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, home / item)
    fx = load_fixture("s237_36144")
    shutil.copytree(fx.data_dir, home / "data")
    old = os.getcwd()
    os.chdir(home)
    sys.path.insert(0, str(home))
    os.environ["LOGNAME"] = "cogent-test"
    back_end = importlib.import_module("back_end")
    back_end.app.alert_handler = lambda msg: None
    yield back_end, home, fx
    os.chdir(old)
    sys.path.remove(str(home))


def js(qtbot, gui, expr):
    box = []
    gui.page.runJavaScript(expr, 0, box.append)
    qtbot.waitUntil(lambda: bool(box), timeout=10000)
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
    qtbot.waitUntil(lambda: text in gui.alerts, timeout=timeout)


def test_full_generate_flow_matches_oracle(qtbot, app_copy):
    back_end, home, fx = app_copy
    gui = back_end.app
    qtbot.addWidget(gui.window)
    with qtbot.waitSignal(gui.page.loadFinished, timeout=30000):
        gui.template = ("Tool_Index_Page.html", {})
    wait_ready(qtbot, gui)

    dbc = fx.dbc.as_posix()
    # upload_dbc only alerts; it does not change the page, so no loadFinished to wait for
    js(qtbot, gui, f"document.getElementById('file_path').value={json.dumps(dbc)};"
                   f"document.getElementById('ch0_node_name').value={json.dumps(fx.node)};"
                   "document.getElementById('form_submit').click(); 1")
    wait_alert(qtbot, gui, "Database loaded successfully")

    msg_data = (fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8")
    sig_data = (fx.data_dir / "CanDbcSigConfiguration.data").read_text(encoding="utf-8")
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()")
    navigate(qtbot, gui, f"BackEnd.Can_dbc_msg_SaveButton({json.dumps(msg_data)})")
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_sig\"]').click()")
    navigate(qtbot, gui, f"BackEnd.Can_dbc0_sig_SaveButton({json.dumps(sig_data)})")

    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    wait_alert(qtbot, gui, "Code Generated in CODE_GEN folder")
    for name in CODE_FILES:
        actual = normalize_date_by((home / "CODE_GEN" / name).read_bytes())
        expected = normalize_date_by((EXPECTED / fx.name / "code" / name).read_bytes())
        assert actual == expected, name


def test_generation_error_then_message_page_still_opens(qtbot, app_copy):
    back_end, home, fx = app_copy
    gui = back_end.app
    (home / "data" / "CanDbcMsgConfiguration.data").write_text("{}", encoding="utf-8")
    gui.alerts.clear()
    navigate(qtbot, gui, "BackEnd.default_page()")
    navigate(qtbot, gui, "document.querySelector('input[name=code_generate]').click()")
    wait_alert(qtbot, gui, "ERROR! Please check the database file")
    assert (home / "CODE_GEN" / "errorlog.txt").exists()
    assert not getattr(sys.stdout, "closed", False)  # stdout not left on a generator file
    gui.alerts.clear()
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.Can_dbc0_msg\"]').click()")
    assert not any("@1" in a for a in gui.alerts)
    assert gui.template[0] == "CAN_DBC_msg.html"
```
The second test depends on the first, which leaves the gates satisfied. Run the file in order (the default).

- [ ] **Step 2: Run them to verify they fail**

Run: `.venv312\Scripts\python.exe -m pytest tests/gui/test_gui_generate.py -q -x`
Expected: FAIL with `ModuleNotFoundError: No module named 'back_end'` (it is still `.pyw` and uses `htmlPy`).

- [ ] **Step 3: Port `back_end`**

```powershell
git mv back_end.pyw back_end.py
.venv312\Scripts\python.exe -W ignore -m lib2to3 -f print -f unicode -w -n --no-diffs back_end.py
```
Then make these exact edits in `back_end.py`:

1. Imports (top of file):
```python
from cogent_gui import webgui as htmlPy
import json
import os
from PySide6 import QtGui, QtWidgets
```
   Delete the two function-local `from PySide import QtGui` lines (in `load_cfg` and `file_browse`).
2. In `load_cfg` and `file_browse`, replace `QtGui.QMainWindow()` with `QtWidgets.QMainWindow()`, and replace the dialog calls with:
```python
file_val = QtWidgets.QFileDialog.getOpenFileName(window, "Select file", ".", "Config files (*.cfg);;All files (*.*)")[0]
```
```python
file_val = QtWidgets.QFileDialog.getOpenFileName(window, "Select file", ".", "DBC files (*.dbc);;All files (*.*)")[0]
```
3. In `unlock`, replace the two lines `app.evaluate_javascript("var pass=prompt(...)")` and `self.__password=app.evaluate_javascript("pass")` with:
```python
self.__password, _ok = QtWidgets.QInputDialog.getText(app.window, "Unlock", "Enter the password to unlock", QtWidgets.QLineEdit.EchoMode.Password)
```
4. In `Can_dbc0_msg`, delete the debug line `print(final_data)` (formerly `print final_data`). It printed about 0.8 MB to stdout and caused failure causes 2 and 3; it has no other effect.
5. In `code_gen`, wrap the generator block so that stdout is always restored, and write the error log next to the outputs:
```python
                except Exception as e:
                    import sys
                    sys.stdout = sys.__stdout__
                    if not os.path.exists('./CODE_GEN'):
                        os.mkdir('./CODE_GEN')
                    f = open('./CODE_GEN/errorlog.txt', 'w')
                    f.write(str(e))
                    f.close()
```
   (This keeps the legacy content of `errorlog.txt`. Adding a traceback is Task 9.)
6. File encodings: add `encoding='latin-1'` to every `open(` of `.html`/`.js` and to the `.data` reads that are concatenated into pages (byte pass-through). Add `encoding='utf-8'` to `.data` writes in the `*_SaveButton` slots and `upload_dbc`, and to `.data` reads that are parsed with `json.loads`.
7. Bottom of file:
```python
app = htmlPy.AppGUI(title="CoGeNT")
app.maximized = True

base_dir=os.path.abspath(os.path.dirname(__file__))

app.template_path = os.path.join(base_dir, "html/")
app.static_path = os.path.join(base_dir, "style/")
app.window.setWindowIcon(QtGui.QIcon(os.path.join(base_dir, "batman.ico")))
app.right_click_setting(htmlPy.settings.DISABLE)
app.bind(BackEnd())
app.allow_overwrite=True
app.template = ("Tool_Index_Page.html", {})
```

`CoGeNT.pyw` becomes:
```python
from back_end import BackEnd
from back_end import app


if __name__ == "__main__":
    app.bind(BackEnd())
    app.start()
```
Verify: `.venv312\Scripts\python.exe -m py_compile back_end.py CoGeNT.pyw` (no output).

- [ ] **Step 4: Run the GUI tests**

Run: `.venv312\Scripts\python.exe -m pytest tests/gui -q`
Expected: 9 passed.

- [ ] **Step 5: Manual launch check**

Run: `.venv312\Scripts\pythonw.exe CoGeNT.pyw`
Expected: a maximized "CoGeNT" window with the batman icon and the styled index page. The DBC and node fields are pre-filled from `data\dbc_details.data`. Right-click shows no menu. Close it.

- [ ] **Step 6: Full suite + commit**

Run: `.venv312\Scripts\python.exe -m pytest -q --ignore=tests/e2e`
Expected: all pass.
```powershell
git add -A back_end.py back_end.pyw CoGeNT.pyw tests/gui/test_gui_generate.py
git commit -m "port: back_end/CoGeNT GUI onto PySide6 shim"
```

---

### Task 8: PyInstaller build and Windows GUI end-to-end test

**Files:**
- Create: `CoGeNT.spec`, `tests/e2e/test_exe_smoke.py`
- Delete: nothing (`setup.py` stays for reference until the user retires it)

**Interfaces:**
- Consumes: the ported app (Task 7), fixtures and expected outputs (Task 2).
- Produces: `dist\CoGeNT\CoGeNT.exe`, with `html\`, `js\`, `style\`, `data\`, `cogent_gui\bridge.js` and `batman.ico` placed next to the exe (same layout as the py2exe build).

- [ ] **Step 1: Write the failing E2E test** `tests/e2e/test_exe_smoke.py`

```python
import os
import re
import shutil
import time

import pytest

from support import CODE_FILES, ROOT, load_fixture

pywinauto = pytest.importorskip("pywinauto")
from pywinauto import Application  # noqa: E402

pytestmark = pytest.mark.e2e
EXE_DIR = ROOT / "dist" / "CoGeNT"


def _wait_alert(app, text, timeout=240):
    deadline = time.time() + timeout
    while time.time() < deadline:
        for w in app.windows():
            try:
                texts = " ".join(c.window_text() for c in w.descendants())
            except Exception:
                continue
            if text in texts:
                w.child_window(title="OK", control_type="Button").click_input()
                return
        time.sleep(0.5)
    raise AssertionError(f"alert containing {text!r} not seen")


def _type(edit, value):
    edit.click_input()
    edit.type_keys("^a{BACKSPACE}", set_foreground=True)
    edit.type_keys(re.sub(r"([{}+^%~()])", r"{\1}", value), with_spaces=True, set_foreground=True)


def test_exe_generates_code(tmp_path):
    if not (EXE_DIR / "CoGeNT.exe").exists():
        pytest.skip("build first: pyinstaller CoGeNT.spec")
    home = tmp_path / "CoGeNT"
    shutil.copytree(EXE_DIR, home)
    fx = load_fixture("s237_36144")
    shutil.copytree(fx.data_dir, home / "data", dirs_exist_ok=True)
    shutil.copy2(fx.dbc, tmp_path / "fixture.dbc")
    env_flag = "--force-renderer-accessibility --disable-gpu"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = env_flag
    app = Application(backend="uia").start(str(home / "CoGeNT.exe"), work_dir=str(home), timeout=60)
    try:
        win = app.window(title="CoGeNT")
        win.wait("visible ready", timeout=60)
        _type(win.child_window(auto_id="file_path", control_type="Edit"), (tmp_path / "fixture.dbc").as_posix())
        _type(win.child_window(auto_id="ch0_node_name", control_type="Edit"), fx.node)
        win.child_window(title_re=r"\s*Load DBC\s*", control_type="Button").click_input()
        _wait_alert(app, "Database loaded successfully")
        for link in (r"\+ TX/RX Message Configurations", r"\+ TX/Rx signal Configurations"):
            win.child_window(title_re=link, control_type="Hyperlink").click_input()
            win.child_window(title="Save and Back", control_type="Button").wait("visible", timeout=240).click_input()
            win.child_window(title_re=r"\s*code gen\s*", control_type="Button").wait("visible", timeout=240)
        win.child_window(title_re=r"\s*code gen\s*", control_type="Button").click_input()
        _wait_alert(app, "Code Generated in CODE_GEN folder")
        for name in CODE_FILES:
            assert (home / "CODE_GEN" / name).stat().st_size > 0, name
        assert not (home / "CODE_GEN" / "errorlog.txt").exists()
    finally:
        app.kill()
```

- [ ] **Step 2: Run it to verify it skips or fails**

Run: `.venv312\Scripts\python.exe -m pytest tests/e2e -q -rs`
Expected: SKIPPED `build first: pyinstaller CoGeNT.spec`.

- [ ] **Step 3: Write `CoGeNT.spec`**

```python
# PyInstaller spec: onedir, files beside the exe (matches the old py2exe layout and the
# CWD-relative ./html ./data ./CODE_GEN paths the app uses).
block_cipher = None
datas = [("html", "html"), ("js", "js"), ("style", "style"), ("data", "data"),
         ("batman.ico", "."), ("cogent_gui/bridge.js", "cogent_gui")]
hidden = ["Dbc_Parser", "Can_dbc_gen", "Can_filter_python_gen", "can_rx_filt_gen", "msg",
          "il_par_h_generation", "il_par_c_generation", "vnim_app_signals_par", "cogent_io"]

a = Analysis(["CoGeNT.pyw"], pathex=["."], datas=datas, hiddenimports=hidden,
             excludes=["tkinter", "PySide6.Qt3DCore", "PySide6.QtQuick3D", "PySide6.QtMultimedia"])
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="CoGeNT", icon="batman.ico",
          console=False, contents_directory=".")
coll = COLLECT(exe, a.binaries, a.datas, name="CoGeNT")
```

- [ ] **Step 4: Build, then run the E2E test**

```powershell
.venv312\Scripts\pyinstaller --noconfirm --clean CoGeNT.spec
.venv312\Scripts\python.exe -m pytest tests/e2e -q
```
Expected: the build ends with `Build complete!`, then `1 passed`. If a locator fails, dump the UIA tree with `.venv312\Scripts\python.exe -c "from pywinauto import Application; a=Application(backend='uia').connect(title='CoGeNT'); a.window(title='CoGeNT').print_control_identifiers(depth=12)"` (with the exe running). Then adjust only the failing `child_window(...)` arguments to the names and auto_ids it shows. The test intent (load → save msg → save sig → generate → 11 files) must stay the same.

- [ ] **Step 5: Manual Windows GUI checklist** (record the results in the PR description)

1. Double-click `dist\CoGeNT\CoGeNT.exe` from Explorer. The window opens maximized with the icon, title "CoGeNT", and styled page.
2. **Browse ..** opens a dialog filtered to `*.dbc`. Choosing a file puts its path in the field.
3. Enter the node `SMART_CORE` and click **Load DBC**. Expect "Database loaded successfully".
4. **+ TX/RX Message Configurations** shows the tables, with rows colored as before. **Save and Back** returns to the index.
5. Do the same for signals. Then **code gen** shows "Code Generated in CODE_GEN folder", and 11 files appear in `CODE_GEN\`.
6. **save_cofiguration** creates `Config\<timestamp>.cfg`. **load_cofiguration** with that file shows "Configuration loaded successfully".
7. Click **code gen** again right away. It is still gated as before ("Please Click load button..." until Load DBC), and it does not crash.

- [ ] **Step 6: Commit**

```powershell
git add CoGeNT.spec tests/e2e
git commit -m "build: PyInstaller packaging and pywinauto end-to-end GUI test"
```

---

### Task 9 (opt-in): Fix generation failure causes

Each item is separate. Ask the user before each one. Each item gets its own failing test and its own commit. Cause numbers refer to spec section 4. Tasks 6–7 already remove causes 1, 2, 3 and 5.

- [ ] **9a, cause 4 (session gates): restore `__load` from a valid `load_cfg`.**
Test (in `tests/gui/test_gui_generate.py`): call `BackEnd.load_cfg` with `QFileDialog.getOpenFileName` monkeypatched to return a `.cfg` built from the fixture. Then `BackEnd.code_gen()`. Expect no "Please Click load button" alert. Fix: in `load_cfg`, after reading `dbc_details`, run the same `dbc_parser(...).check__node()/check_parsing()` validation as `upload_dbc`, and set `self.__load = 0` when it passes.
- [ ] **9b, cause 8 (CWD-relative paths): resolve data, outputs and config against the app folder.**
Test: launch with `cwd` set to another folder. Outputs must appear in `<app>\CODE_GEN`. Fix: `os.chdir(base_dir)` at the top of `CoGeNT.pyw` before importing `back_end`. This one line keeps every relative path intact.
- [ ] **9c, causes 7 and 10 (opaque errors): write the full traceback to `CODE_GEN\errorlog.txt`, and name the missing key in the alert.**
Test: data `{}` gives an alert containing `KeyError` and the message name, and the log contains `Traceback`. Fix: `traceback.format_exc()` in the `except`; alert `'ERROR! ' + json.dumps(type(e).__name__ + ': ' + str(e))`.
- [ ] **9d, cause 9 (stale outputs): generate into a temporary folder and move it into `CODE_GEN` only on success.**
Test: a failing generation leaves pre-existing `CODE_GEN` files byte-identical. Fix: in `code_gen`, point `cogent_io.CODE_GEN_DIR` at `./CODE_GEN/.tmp`, and on success replace the files in `./CODE_GEN`.
- [ ] **9e, cause 11 (latent crashes): fix `default_page` (`self.__node = 'None'`) and `onpageload` (initialize `dbc_name = node_name = ''`), and build the JS with `json.dumps(...)`.**
Test: `BackEnd.default_page()` with a fresh `BackEnd` and an empty `dbc_details` shows the index page with no console error.
- [ ] **9f, cause 6 (absolute DBC paths in .cfg): if the stored path is missing, look for the same file name next to the `.cfg` and in `DBC\`.**
Test: load a `.cfg` whose `ch0_file` is `G:/missing/<name>.dbc` while `<name>.dbc` exists in `DBC\`. The DBC field shows the local path.

---

## Self-Review (done)

- **Spec coverage.** Versions and installs: Task 0. Inventory and trace: spec sections 2–3. Failure causes: spec section 4 plus Task 9 (each cause maps to a task or item). Compatibility (print, `/`, `next`, iter*, encoding, ordering, stdout): Tasks 3–5. Library replacements (htmlPy, PySide, py2exe): Tasks 6–8. Automated generation tests: Tasks 1–5. Windows GUI test: Tasks 7–8. "No source change yet": nothing in the app source is touched before the user approves this plan.
- **Placeholder scan.** None. Task 8 Step 4 has a defined fallback (dump the UIA tree, then adjust only the locator arguments) because Chromium's UIA names can only be confirmed once the exe is running.
- **Type and name consistency.** `CODE_FILES` match between `gen_harness.py` and `tests/support.py`. `PAGE_FILES` are paths in the harness and base names in `support.py`, by design (the harness copies the base names out). `open_output`/`close_output`, `AppGUI.alerts`/`alert_handler`/`page`, and `window.__cogentReady` are used consistently.
- **Review Focus.** Every listed item has its named test in its owning task.
