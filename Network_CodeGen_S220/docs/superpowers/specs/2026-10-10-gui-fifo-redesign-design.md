# GUI: receive FIFO, new-item indicators, re-apply edits, clearer errors, restyle, help

Status: approved by the user on 2026-10-10 ("proceed and complete after proper testing").
Builds on branch `fifo-multiplexing` (FIFO planning in `cogent_fifo`, `tools/carry_forward.py`).

## Goal

Everything needed to go from a new DBC to code that matches the user's workspace is done in the GUI:
no hand-edited configuration files, the receive-rule usage (max 192) is always visible, merges are
suggested and applied with a click, new messages/signals cannot be missed, the user's other hand edits
are re-applied from the GUI, errors say what to do and where, the GUI looks modern and is spelled
correctly, and a Help page plus `USER_GUIDE.md` explain the whole tool.

Root cause of the error that triggered this (2026-10-10): loading an older `.cfg` archive renamed
`data/CanFifoConfiguration.data` to `.previous` (behaviour added on this branch), so code gen ran without
merges: 41490 needs 211 rules without merges, 186 with them.

## Decisions (user)

- Home page shows a FIFO card; a separate "Receive FIFO" page manages merges.
- Over the limit: CoGeNT pre-selects the fewest blocks needed (blocks already configured are kept),
  the user confirms with Apply.
- Loading an archive without FIFO settings keeps the current merges (blocks that do not fit the DBC
  are flagged on the FIFO page).
- All pages restyled, table layouts kept.
- Re-apply hand edits from the GUI.
- `IL_MUX_MSG_OFFSET_ID` conflicts are resolved with the safe value (first data-changed flag byte after
  the generated ones).

## Components

1. `cogent_fifo` (extend): `config_from_dict` / `config_to_dict` / `save_config` so the GUI can validate
   and store settings; `preselect` (fewest candidate blocks so the plan fits); `block_problems` (per-block
   validity for a DBC).
2. `cogent_project` (new, no Qt): cached DBC message lists; tolerant planning (messages without saved
   settings count as disabled and are reported); `fifo_view(...)` = everything the card/page show
   (counts per FIFO, limits, fits, merged blocks with members and problems, candidates with members,
   layer, DLC, rules saved, pre-selection, receive-only messages and choices); `new_items(...)` = messages
   (`<NAME>_rx_enable` / `<NAME>_tx_enable` missing) and signals (`<SIG>_rx_init_value` /
   `<SIG>_tx_init_value` missing) without saved settings - the same rule as the green rows.
3. `cogent_carry` (new, from `tools/carry_forward.py`, which becomes a thin CLI):
   - `can_rxrule.cfg` and `nw_can_dll.h` are always taken from the new generation (they are produced by
     the FIFO settings; a three-way merge of them produced a duplicated dispatch table for 41490); the
     dropped edit regions are reported for review.
   - Derived-value conflicts resolved automatically: `IL_RX_NUM_*` (new + your delta),
     `IL_MUX_MSG_OFFSET_ID` / `IL_NUM_OF_RX_DATA_CHANGED_FLAG` (safe value), `VNIM_*_MESSAGE` handle
     numbering (merged enum order), `vnim_msg_byte_position` / `vnim_msg_bit_mask` (one entry per message).
   - Post-merge checks: conflict markers, definitions duplicated by the merge, handle order = enum order =
     receive-table order, per-message tables = message count, `IL_RX_NUM_MESSAGES` = message count.
4. GUI (`back_end.py`, templates, `style/cogent.css`):
   - Home: sidebar (Home, Messages, Signals, Receive FIFO, Re-apply edits, Help) with "new" badges;
     DBC card; new-items banner; FIFO card (total/192, bar per FIFO, state, link); action buttons.
   - Receive FIFO page: usage, merged blocks (members, remove, problems), candidate blocks with
     checkboxes (pre-selected), live preview (`fifo_preview` slot returns JSON), receive-only messages
     (add/remove), limits (advanced), Apply saves.
   - Message / signal pages: banner "N new ... (green rows)", "Next new" and "Only new" buttons.
   - Re-apply edits page: three folders (previous generation, workspace, output) with Browse, Run,
     results table, conflicts list, open output folder; "Keep a copy of CODE_GEN" button.
   - Errors: short reason and where to fix it in the GUI; details in the log. FIFO overflow and invalid
     blocks point to "Receive FIFO".
   - Restyle: modern theme over the existing w3 classes, same ids/names (tests, saved data), labels
     fixed ("Save configuration", "Load configuration", "Generate code", "Browse", page titles,
     "Message Timeout ID", "Message Type", "Byte order").
5. Help: `USER_GUIDE.md` is the single source; the Help page renders it (small Markdown renderer,
   `cogent_help.py`).

## Constraints

- Generated C code and the page generator output stay byte-identical except the listed label fixes
  (golden tests keep running; the label fixes are an explicit, tested mapping).
- The reference workspace is only read. Nothing private is committed (repository is public).
- Packaged exe includes the new modules and `USER_GUIDE.md`.

## Testing

Unit tests (FIFO view, pre-selection, per-block problems, tolerant planning, new items, config
round trip, carry rules and checks, Markdown renderer); reference tests (40024 reproduction, 41490
automatic re-application = the verified manual result; skipped without the workspace/DBC); GUI tests
(card states, FIFO page pre-select/apply/generate, flagged block, new-item banners and Next button,
re-apply page, help page, labels, old archive keeps merges); exe e2e after rebuild; full suites.
