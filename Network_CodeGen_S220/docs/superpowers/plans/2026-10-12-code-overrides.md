# Code overrides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** the remaining S2XX hand edits become settings of a "Code overrides" page (or automatic fixes), so
Generate code reproduces the official workspace from the 40024 DBC except for a documented list.

**Architecture:** `cogent_overrides.py` loads and validates `data\CanOverrideConfiguration.data`, holds the
active overrides during a generation (set by `cogent_generate`), applies the receive timeouts to the parsed
DBC messages (`Dbc_Parser.get_msg_type`) and provides the message order key. Small hooks in
`il_par_h_generation.py` (Tx frame/periodic tables, callbacks), `vnim_app_signals_par.py` (NM table, host
forwarding, REM block), `il_par_c_generation.py` (CRANK fix) and the sorts of the four generators. A new GUI
page edits the file.

**Tech Stack:** Python 3.12 (`.venv`), pytest (`gui`, `e2e` markers), PySide6, PyInstaller.

**Spec:** `docs/superpowers/specs/2026-10-12-code-overrides-design.md`

## Global Constraints

- Without an overrides file every generated file is byte-identical to today (golden tests), except the
  CRANK_COUNT compile fix, applied to the legacy references in the golden test.
- The workspace is only read; no workspace content is committed (public repository).
- Never commit the user's runtime `data/`, `html/CAN_DBC*`, `html/CanDbc*`, `js/CanDbc*` changes or `CODE_GEN/`
  run folders.
- New modules go into `CoGeNT.spec` hidden imports, `tests/gui/gui_support.py` and
  `tests/test_paths_with_spaces.py` app lists.
- Scripts with backslashes are written with the Write tool (not shell heredocs).

## Review Focus

1. Overrides file with an unknown message name or a non-number: generation stops and names the setting.
2. A Tx override for a disabled message: ignored (the message has no table row).
3. Empty settings page saved: no file content beyond `{}`; output unchanged.
4. numeric_order prefix that matches no message: no change.
5. host_forward prefix with a message that has no notification block (delayed group): the REM block still
   lists it; its indication is generated as before.

---

### Task 1: `cogent_overrides.py` (load, validate, activate, order key, DBC message hook)

Tests `tests/test_overrides.py`: load of a full file; defaults for a missing file; validation errors
(unknown attribute, negative/non-integer numbers, nm_tx row without message); `order_key` with and without
prefixes (REM_MSG_2 < REM_MSG_10 only with the prefix; BMS19_100 < BMS1_10 unchanged); `apply_message`
sets `GenMsgCycleTime` of an Rx message with a timeout; `activate`/`deactivate`.

### Task 2: receive timeout and order in the generators

`Dbc_Parser.get_msg_type` calls `cogent_overrides.apply_message` for every message; `cogent_generate`
activates the overrides around the generators and validates names against the DBC (CogentError naming the
file and entry). The four generators sort with `cogent_overrides.order_key`. Tests in
`tests/test_overrides_generation.py` (40024 fixture): TC_NSM timeout 100 gives `100*MSG_TIMEOUT_ERROR_COUNT`
and both VNIM cases; REM_MSG handles and enum in numeric order; without the file every output equals the
plain generation.

### Task 3: Tx attribute, period/offset, confirmation callbacks (`il_par_h_generation.py`)

Tests: EX_SUMMARY_RESPONSE_0 Event + 0/0 gives `(IL_TX_ATTR_EVENT)`, NULL pointer, row 0/0; MCM_SP Event keeps
its row; REM_ACK_MSG Periodic+Event; MCM_PKE_SP offset 0; IC10_200 confirmation gives TXC_NOTIFY, the two
pointers and the two externs.

### Task 4: NM transmit table (`vnim_app_signals_par.nm_par_gen`)

Test: the 5 configured rows in order with labels, IDs, buffers and handles +1..+5.

### Task 5: host forwarding and the REM block (`vnim_app_signals_par.py`)

Test: REM_MSG_0 indication calls `host_update_msg(VNIM_REM_MSG_0);` and has no os_notify for it;
the REM MACROS block after the IS_*_DLC_FAULT defines lists REM_MSG_0..15 = 0..15.

### Task 6: CRANK_COUNT stray lines

Test: EMS46_500_PreCopy contains `// rValue |= ... CRANK_COUNT_IBS_1 ...`; golden test transform for legacy
references; brace/parenthesis balance unchanged.

### Task 7: MANUAL_ACTIONS.md

Tests: disabled additional message says to enable its Rx; merged block dispatch reported done when a
workspace nw_can_dll.c (from `data\ReapplyEdits.data` "edited") maps every member ID, MANUAL otherwise.

### Task 8: GUI page "Code overrides"

`html/Overrides.html`, `back_end` slots `overrides_page`, `overrides_save(json)`, sidebar entry in both shells,
USER_GUIDE section. GUI tests: page lists the saved rows; Save writes the file; invalid input is named.

### Task 9: reference, configuration files, verification, PR

`tests/test_overrides_reference.py` (local only): 40024 + max-match settings equals the workspace except the
spec list. Write `S2XX_40024_max_match.cfg` / `S2XX_41490_max_match.cfg` (local_reports), docs, full suites
(non-GUI, GUI, exe rebuild, e2e), push the branch and open the PR (no merge).
