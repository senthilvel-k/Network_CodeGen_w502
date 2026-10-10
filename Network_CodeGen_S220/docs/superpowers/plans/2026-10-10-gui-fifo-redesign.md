# GUI receive FIFO, indicators, re-apply edits, restyle, help - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make CoGeNT's receive-FIFO handling, new-item detection, re-application of hand edits and help available in a restyled GUI, with no hand-edited configuration files.

**Architecture:** Qt-free logic in `cogent_fifo` (config API, pre-selection, per-block problems), `cogent_project` (cached DBC lists, tolerant planning, view dicts for the GUI, new items) and `cogent_carry` (three-way re-application with derived-value rules and checks). `back_end.py` exposes slots; Jinja templates in `html/` render pages; `style/cogent.css` restyles over the existing w3 classes. Live previews use QWebChannel slot return values (`@Slot(str, result=str)`, JS callback as last argument).

**Tech Stack:** Python 3.12, PySide6 6.11 (QtWebEngine, QWebChannel), Jinja2, pytest + pytest-qt, git (`git merge-file`), PyInstaller.

**Spec:** `docs/superpowers/specs/2026-10-10-gui-fifo-redesign-design.md`

## Global Constraints

- Generated C code byte-identical to before for the same inputs (golden/legacy tests stay green).
- Page generator output byte-identical except the explicit label fixes: "Message Timout ID" -> "Message Timeout ID", "Messsage Type" -> "Message Type", "byte_order"/"Byte_order" -> "Byte order".
- Element ids/names used by tests and saved data stay unchanged (`file_path`, `ch0_node_name`, `form_submit`, `ch0_dbc_file`, `code_generate`, `save_cofiguration`, `load_cofiguration`, `a[href="BackEnd.Can_dbc0_msg"]`, `a[href="BackEnd.Can_dbc0_sig"]`, `tx_table`, `rx_table`).
- `D:\networkgen\dc.app.scl.vehiclecomm` is only read; nothing private is committed (public repository).
- FIFO limits default 192 total / 64 per FIFO; `IL_MUX_MSG_OFFSET_ID` conflicts use the safe value.
- New runtime modules are added to `CoGeNT.spec` hidden imports and `tests/gui/gui_support.py` APP_ITEMS/APP_MODULES; `USER_GUIDE.md` is bundled.

## Review Focus

1. No DBC loaded, or the pages not saved for the loaded DBC: home card shows guidance, nothing crashes. (Task 3 tests `test_card_without_dbc`, `test_card_counts_unsaved_messages_as_disabled`.)
2. A kept merge block that does not fit the new DBC (no received member, DLC mismatch): flagged on the FIFO page, not applied in the preview; code gen error points to Receive FIFO. (Task 2 `test_view_flags_invalid_kept_block`, Task 3 `test_codegen_invalid_block_points_to_fifo_page`.)
3. Messages without saved settings (new in the DBC): counted as disabled in the view and listed; code gen asks to save the page. (Task 2 `test_tolerant_planning_reports_unconfigured`.)
4. Over the limit even with every candidate selected: page says so and names the other options. (Task 1 `test_preselect_reports_when_candidates_are_not_enough`.)
5. Re-apply with an output folder inside the workspace or not empty: refused with a clear message, workspace untouched. (Task 6 `test_reapply_refuses_output_inside_workspace`.)

---

### Task 1: FIFO configuration API, pre-selection, per-block problems (`cogent_fifo.py`)

**Files:** Modify `cogent_fifo.py`; Test `tests/test_fifo.py`

**Interfaces (produces):**
- `config_from_dict(raw: dict, source: str = None) -> FifoConfig` (raises `FifoConfigError`; `load_config` uses it)
- `config_to_dict(cfg: FifoConfig) -> dict` (`{"max_rx_rules", "max_rules_per_fifo", "merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}], "additional_rx_messages": [...]}`; limits only when not default)
- `save_config(data_dir: str, cfg: FifoConfig) -> str` (writes JSON, returns path)
- `block_problems(categories: dict, block: MergeBlock) -> list[str]` (same rules as `merge_blocks`, one block)
- `preselect(plan_fn, config: FifoConfig, candidates: list[MergedGroup]) -> (list[MergeBlock], bool)`; `plan_fn(cfg) -> RxPlan`; adds candidates (largest saving first, then lowest base) until `check_limits` is empty; returns (added blocks, fits).

- [ ] Tests: dict round trip; `config_from_dict` errors name the setting; `save_config` + `load_config` round trip; `block_problems` empty / no member / DLC / layer; `preselect` on 40024 picks 0x4F0 then 0x3D0 and fits (186 with BMS19/20); `test_preselect_reports_when_candidates_are_not_enough` (synthetic 300 unrelated IDs: fits=False).
- [ ] Implement by moving the body of `load_config` after JSON parsing into `config_from_dict`; `block_problems` reuses the checks in `merge_blocks` (refactor them into it).
- [ ] Run `tests/test_fifo.py`; commit.

### Task 2: Project view logic (`cogent_project.py`)

**Files:** Create `cogent_project.py`; Test `tests/test_project.py`

**Interfaces (produces):**
- `class CachedDbc(dbc_path, node)`: `get_msg_type(kind, direction)` returns deep copies of lists cached per (path, mtime, node); module-level cache `cached_dbc(dbc, node)`.
- `class TolerantConfig(dict)`: missing `_rx_enable`/`_tx_enable` -> `''`, missing `_msg_type_no_of_events` -> `'Appl'`; records message names in `.missing`.
- `fifo_view(dbc, node, msg_cfg: dict, config: FifoConfig) -> dict` with keys: `total`, `max_rx_rules`, `max_rules_per_fifo`, `fifo_counts` [3], `fits`, `problems` [str], `merged` [{`base`,`mask`,`label`,`members`:[{`id`,`name`}],`problems`:[str],`applied`:bool}], `candidates` [{`base`,`mask`,`label`,`members`,`layer`,`dlc`,`saves`,`preselected`}], `receive_only` [{`name`,`id`,`problem`}], `receive_only_choices` [{`name`,`id`}], `unconfigured` [names], `preselect_fits` bool.
- `new_items(dbc, node, msg_cfg, sig_cfg) -> {"messages": [{"name","direction"}], "signals": [{"name","message","direction"}]}`.

- [ ] Tests: `test_tolerant_planning_reports_unconfigured` (drop AMP-like keys from 40024 config: view counts them disabled and lists them); `test_view_40024_reference_config` (184, fits, two merged blocks applied); `test_view_without_config_preselects` (40024, no config: 209 over, preselected 0x4F0 and 0x3D0, `preselect_fits`); `test_view_flags_invalid_kept_block` (block 0x7F0 with no member: `applied` False, problem text, plan without it); `test_new_items` (remove two message keys and a signal key: listed with direction).
- [ ] Implement; run; commit.

### Task 3: Receive FIFO page, home card, clearer errors, archives keep merges (`back_end.py`, templates)

**Files:** Modify `back_end.py`, `cogent_generate.py`, `cogent_fifo.py` (`overflow_hint` text); Create `html/Fifo.html`; Modify `html/Tool_Index_Page.html`; Tests `tests/gui/test_gui_fifo.py`, update `tests/gui/test_gui_errors.py`, `tests/test_fifo_pipeline.py`.

**Interfaces:**
- Slots: `fifo_page()`, `fifo_preview(str) -> str` (input: config dict JSON; output: `fifo_view` JSON), `fifo_apply(str) -> str` (validate, `save_config`, return view JSON; on error returns `{"error": text}`).
- `default_page()` renders `Tool_Index_Page.html` with context `{"loaded": bool, "fifo": view or None, "new": new_items or None, "dbc_name": str}`.
- `_set_aside_fifo_config` replaced by `_fifo_note(archive_names) -> str` that keeps the file and returns a note.
- Overflow `CogentError`: reason `"<n> CAN receive rules are needed; the controller accepts <max> (FIFO 0/1/2: a/b/c)"`, hint `"Nothing was changed. Open 'Receive FIFO' (left menu, or the receive-rule card on the home page): the blocks to combine are pre-selected. Press Apply, then Generate code again."`; full list of messages/candidates only in the log (`err.details`).

- [ ] GUI tests: `test_card_without_dbc`; `test_card_counts_unsaved_messages_as_disabled`; `test_card_over_limit_links_fifo_page`; `test_fifo_page_preselects_and_apply_fixes_codegen` (40024 fixture without config: page shows 0x4F0/0x3D0 ticked, Apply, card fits, Generate code succeeds with 184+... rules); `test_fifo_page_preview_updates_total` (untick a block -> total changes via slot); `test_codegen_overflow_message_is_short_and_points_to_fifo`; `test_codegen_invalid_block_points_to_fifo_page`; `test_load_old_archive_keeps_merges`.
- [ ] Implement; run GUI + pipeline tests; commit.

### Task 4: New-item indicators

**Files:** Modify `back_end.py` (msg/sig page assembly, home context), `html/Tool_Index_Page.html`; Test `tests/gui/test_gui_new_items.py`

- [ ] Home banner "New in this DBC: N messages (...), M signals" with buttons to the pages; sidebar badges.
- [ ] Message/signal pages: banner `#cogent-new-banner` with count, `Next new` (`#cogent-next-new`, scrolls to and outlines the next green row) and `Only new` (`#cogent-only-new`, hides other rows; toggle). Rows marked with class `cogent-new` by the existing highlight loop.
- [ ] Tests: banner text and counts on home and message page; Next scrolls (row has class `cogent-current`); Only new hides non-new rows; no banner when nothing is new.
- [ ] Commit.

### Task 5: Re-apply engine (`cogent_carry.py`)

**Files:** Create `cogent_carry.py` (logic moved from `tools/carry_forward.py`); Modify `tools/carry_forward.py` (CLI wrapper); Tests `tests/test_carry_forward.py`, `tests/test_reference_workspace.py`.

**Interfaces:** `carry_forward(base, edited, new, out) -> list[dict]` (unchanged fields + `rules_applied` [str] + `checks` [str]); `report(results, ...) -> str`; `FIFO_FILES = ("can_rxrule.cfg", "nw_can_dll.h")`; `UsageError`.

- [ ] Rules (each with a synthetic test): FIFO files taken from new (+ dropped regions reported); numeric delta for `IL_RX_NUM_*`; mux rule (`IL_MUX_MSG_OFFSET_ID` = new `IL_NUM_OF_RX_DATA_CHANGED_FLAG`, total `(G + extra)`); handle renumber from merged enum; per-message arrays rebuilt for N messages.
- [ ] Checks (each tested): markers, duplicated definitions, handle/enum/rx-table order, per-message macro tables = N, `IL_RX_NUM_MESSAGES` = N.
- [ ] Reference test (skipped without workspace/DBC/fixture): 40024 reproduction still exact (except stamp); 41490 automatic result = `local_reports`-verified manual resolution rules (no conflicts, all checks OK, values 195/163).
- [ ] Commit.

### Task 6: Re-apply edits page

**Files:** Create `html/Reapply.html`; Modify `back_end.py`; Test `tests/gui/test_gui_reapply.py`

**Interfaces:** slots `reapply_page()`, `reapply_browse(str)` (field id -> folder dialog), `reapply_run(str)` (JSON of three paths; saves them to `data/ReapplyEdits.data`; renders results), `reapply_open(str)` (opens folder), `keep_codegen_copy()` (copies CODE_GEN files to `CODE_GEN/<dbc stem>_<yyyy-mm-dd_hhmm>`).

- [ ] Tests: run with synthetic folders shows per-file table and conflict list; `test_reapply_refuses_output_inside_workspace`; paths remembered; keep copy creates folder with the 11 files.
- [ ] Commit.

### Task 7: Restyle and labels

**Files:** Create `style/cogent.css`; Modify all templates, `back_end.py` (inject stylesheet + header into assembled pages), `Can_dbc_gen.py`, `Can_filter_python_gen.py` (label fixes, titles), `tests/test_pages_golden.py` (explicit label mapping).

- [ ] Tests: labels on home ("Generate code", "Save configuration", "Load configuration", "Browse"), titles, no "cofiguration"/"Timout"/"Messsage" text visible on any page; golden page tests pass with the mapping.
- [ ] Commit.

### Task 8: User guide and Help page

**Files:** Create `USER_GUIDE.md`, `cogent_help.py`, `html/Help.html`; Modify `back_end.py` (`help_page()`), `CoGeNT.spec` (bundle guide); Tests `tests/test_help.py`, GUI test help page.

- [ ] Renderer supports headings, paragraphs, bullet/numbered lists, tables, fenced code, inline code, bold, links; escapes HTML.
- [ ] Guide covers: start, Load DBC, message/signal pages and new items, receive FIFO, generate, outputs and MANUAL_ACTIONS, re-apply edits, save/load configuration, errors and fixes, command-line tools. `FIFO_MULTIPLEXING.md` points to it.
- [ ] Commit.

### Task 9: Packaging, full verification, docs

- [ ] `CoGeNT.spec` hidden imports (`cogent_project`, `cogent_carry`, `cogent_help`) and datas (`USER_GUIDE.md`); rebuild; e2e (both fixtures) passes.
- [ ] Full suites: non-GUI, GUI, e2e; `py_compile -W error`; manual launch check of the GUI (screenshot).
- [ ] Restore the user's `data/CanFifoConfiguration.data` from `.previous` (created by the old set-aside behaviour).
- [ ] HANDOFF.md update; commit; push to the open PR branch only if asked.
