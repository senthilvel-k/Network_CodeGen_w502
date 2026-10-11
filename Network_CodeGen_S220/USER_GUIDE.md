# CoGeNT user guide

CoGeNT generates the CAN network C code of an ECU (interaction layer, VNIM, CAN driver receive rules and
dispatch tables, NM parameters, resources) from a CAN database (DBC) and the settings you make on its pages.
This guide is also shown in the tool: Help in the left menu.

## Start CoGeNT

- Packaged tool: run `CoGeNT.exe` in the CoGeNT folder.
- From the source folder: run `.venv\Scripts\python.exe CoGeNT.pyw` in `Network_CodeGen_S220`.

Use the project's `.venv` Python. The Microsoft Store Python (what `python` may start) keeps PySide6 in a
private folder that Qt's browser engine is not allowed to read, which shows "Qt6WebEngineCore.dll was not
found".

The left menu is on every page: Home, TX/RX messages, TX/RX signals, Receive FIFO, Re-apply edits, Help.
An orange badge next to an entry tells you something needs attention there ("2 new", "over").

## Workflow at a glance

1. Home: select the DBC file and the node name, press Load DBC.
2. Check the banner "New in this DBC" and the receive-rule card.
3. TX/RX messages: review the green (new) rows, press Save and Back.
4. TX/RX signals: review the green rows, press Save and Back.
5. Receive FIFO: if the card says the rules are over the limit, apply the pre-selected ID blocks.
6. Home: press Generate code. The files are written to a new folder `CODE_GEN\<date_time>`.
7. Read `MANUAL_ACTIONS.md` in that folder.
8. Re-apply edits: re-apply your hand edits from your workspace to the new files.
9. Home: press Save configuration to keep all settings for next time.

## Load a DBC

On Home, enter the DBC file (or press Browse) and the node name (the ECU, for example `SMART_CORE`), then
press Load DBC. CoGeNT checks that the file exists and that the node is in the DBC; if not, the message lists
the nodes the DBC defines.

After loading, the home page shows:

- New in this DBC: messages and signals that have no saved settings yet, with links to the pages.
- CAN receive rules: how many receive rules the DBC needs with your settings, out of 192, with a bar per
  receive FIFO. Red means over the limit.

## TX/RX messages page

One row per message of the node: Tx messages first, then Rx messages. For each message you set whether it is
enabled, its type (Appl, NM or Diag) and the Rx options (key message, notification during IGN OFF, node,
node absent and timeout DTC IDs). Press Save and Back to store the settings (`data\CanDbcMsgConfiguration.data`).

Rows without saved settings are green. The banner at the top counts them:

- Next new jumps to the next green row and outlines it.
- Only new hides all other rows (press again to show all).
- Save and Back in the banner saves the page.

A message that has no saved settings counts as not received in the receive-rule card until you save the page.

## TX/RX signals page

The signals of the enabled application (Appl) messages: init value, debounce, notification, content error
check and DTC, green drive. Save the message page first; the signal page uses its settings. New signals are
green, with the same banner as on the message page. The init value of a new signal is the DBC start value
(for example 0x1F4 for a cell temperature with start value 500).

When many signals are new (for example after enabling BMS19_100 and BMS20_100), set their notification in one
step: choose it in "Notification for new rows" in the banner and press Apply to new rows. Only the green rows
change; check them, then press Save and Back.

## Multiplexed messages

A multiplexed message carries a multiplexor signal (M in the DBC) and signals that are only valid for one
multiplexor value (m0, m1, ...). CoGeNT generates received multiplexed messages when their Rx enable is on:

- VCU5_500 keeps its layout (multiplexed signals from bit 0, multiplexor in byte 7).
- Every other one, such as BMS19_100 and BMS20_100, is generated in the layout of the S2XX code: one struct
  per multiplexor value inside a union (of the multiplexed bytes when the multiplexor has a byte of its own,
  of whole frames when it shares a byte with a multiplexed signal), one stored value per signal, a PreCopy
  that checks only the signals of the received value, data-changed flags in their own area after the
  others (`IL_MUX_MSG_OFFSET_ID`, computed so it never overlaps the other flags), and a notification to the
  host for every received frame.

To generate BMS19_100 and BMS20_100: tick their Rx enable on TX/RX messages, Save and Back; on TX/RX signals
set the notification of the new rows (the S2XX BMS signals use 200ms_Delay_g1) and check the init values,
Save and Back; Generate code. Their `additional_rx_messages` entries on Receive FIFO are then no longer
needed (`MANUAL_ACTIONS.md` says so).

Not generated (Generate code stops and names the message): transmitted multiplexed messages, Motorola
multiplexed signals, multiplexed signals longer than 32 bits, more than one multiplexor, a DLC above 8.

## Receive FIFO

The microcontroller accepts at most 192 CAN receive rules, 64 in each of its 3 receive FIFOs. Each received
message normally needs one rule. When there are more, CoGeNT stops before writing any file and the home card
turns red.

An aligned block of IDs (for example 0x4F0 to 0x4FF) can be received through one rule instead
("FIFO multiplexing"). The lowest-ID message of the block keeps the rule and the dispatch entry, and your
hand-written `nw_can_dll.c` must hand each ID to its own message. CoGeNT writes that C code to
`MANUAL_ACTIONS.md` of the generation. A block can only be combined when all its received messages use the same
layer (application, NM or Diag) and the same DLC.

The Receive FIFO page shows:

| Part | What it does |
|---|---|
| Receive rules with your selection | Total and bar per FIFO for the selection on the page; updates when you tick or untick |
| Combined ID blocks (saved) | The blocks in use; Remove takes one out; a block that does not fit this DBC is marked "Not applied" with the reason |
| Suggested blocks to combine | Every block that could be combined, with its messages, layer, DLC and the rules it saves. When the rules do not fit, CoGeNT ticks the fewest blocks needed |
| Add a block by ID | Enter the first ID (hex) and the size (8, 16 or 32 IDs) |
| Receive-only messages | Messages that must be received although their Rx enable is off, because their code is hand-written (for example BMS19_100, BMS20_100) |
| Controller limits | Change only if your microcontroller accepts more rules |

Check the messages of each ticked block, then press Apply. The settings are saved with the project
(`data\CanFifoConfiguration.data`, stored in configuration archives), so you never edit a file by hand.
Back without saving leaves the saved settings unchanged.

Combined blocks change two generated files: `can_rxrule.cfg` (one rule with mask `0xC00007F0` for a 16-ID
block) and `nw_can_dll.h` (one dispatch entry per block).

## Generate code

Press Generate code on Home. CoGeNT checks the inputs, plans the receive rules and runs the generators into a
staging folder. Only when everything succeeded it becomes a new folder `CODE_GEN\<date_time>` (for example
`CODE_GEN\11-10-2026_15-34-54`), so a failed run leaves nothing behind and earlier runs are never changed.
Home shows the last generation with an Open folder button.

Each run folder is laid out like your repository, so you can copy its folders over the repository root
(`dc.app.scl.vehiclecomm`) or compare them file by file:

| In the run folder | Content |
|---|---|
| `<date_time>.cfg` | The configuration of this run (as Save configuration writes it); Load configuration restores it |
| `MANUAL_ACTIONS.md`, `fifo_plan.json` | Reports (below) |
| `app.nos.arch3\src\` | `can_rxrule.cfg`, `nw_can_dll.h`, `nw_il_msg.h`, `nw_il_par.h`, `nw_il_par.c`, `nw_nm_par.h` |
| `app.vnim.arch3\src\` | `nw_vnim_app_signals_par.c` |
| `app.vnim.arch3\` | `nw_vnim_app_signals_par.h`, `vnim.msg.resource`, `vnim.txrx.resource` |
| `app.host.manager\` | `nw_host_mgr_txrx.resource` |

| File | Content |
|---|---|
| `can_rxrule.cfg`, `nw_can_dll.h` | CAN receive rules and dispatch tables |
| `nw_il_msg.h`, `nw_il_par.h`, `nw_il_par.c` | Interaction layer |
| `nw_vnim_app_signals_par.h`, `nw_vnim_app_signals_par.c` | VNIM |
| `vnim.msg.resource`, `vnim.txrx.resource`, `nw_host_mgr_txrx.resource` | Resources |
| `nw_nm_par.h` | Network management parameters |
| `MANUAL_ACTIONS.md` | What CoGeNT did for the receive rules and what you must still do by hand |
| `fifo_plan.json` | Every receive rule, the merged blocks and the limits |

`MANUAL_ACTIONS.md` lists each item with the file and location, the current value, the required change, why
CoGeNT cannot do it, dependencies, steps and how to verify it. MANUAL items are edits in files CoGeNT does not
generate (for example `nw_can_dll.c`); REVIEW items are behaviour you should confirm (for example IDs a combined
block accepts although no message uses them).

## Re-apply edits

If you change generated files by hand in your project (your workspace), Re-apply edits brings those changes
into a new generation. It needs Git for Windows.

| Folder | What to choose |
|---|---|
| Previous generation | The run folder your workspace edits started from, for example `CODE_GEN\26-02-2026_12-10-10` (older flat folders such as `CODE_GEN\DBC_40024` work too) |
| Your workspace | Your project folder; each generated file is found there by its name |
| New generation | Normally the latest run folder (filled in for you) |
| Output folder | A new folder (default `MERGED\<DBC>_<date>`); it must not be inside the other three |

Press Re-apply my edits. The three input folders are only read. For each file, your changes (previous
generation to workspace) are applied to the new file:

- `can_rxrule.cfg` and `nw_can_dll.h` are taken from the new generation, because the Receive FIFO settings
  produce them.
- Where only white space differs, your formatting is kept; where only the Date/By/Traceability header
  differs, the new header is kept.
- Values derived from the message list are recomputed: `IL_RX_NUM_*` (your change on top of the new value),
  `IL_MUX_MSG_OFFSET_ID` and `IL_NUM_OF_RX_DATA_CHANGED_FLAG` (first free flag byte), the `VNIM_*_MESSAGE`
  handle numbers, and the arrays `vnim_msg_byte_position` and `vnim_msg_bit_mask`.
- Messages you added by hand (for example BMS19_100 and BMS20_100 in the 40024 workspace): when the new
  generation produces them, your hand code is not re-applied and the generated code is used once; when the
  new DBC does not have them, their hand code is left out. The report lists them under "Messages you added
  by hand".
- The result is checked: no conflict marker, no definition lost or doubled, tables with one entry per message,
  handles in the right order.

The page lists every file and a Manual Action Required list. `CARRY_FORWARD.md` in the output folder describes
each item in full. Typical items:

- "the new generation changed lines you edited": open the file at the line, keep the right content, delete
  the conflict marker lines.
- "your file comes from another generation": your file was generated from an older DBC; check that its
  differences are edits you want to keep.

The result is written in the same folders as your repository. Every run folder stays in `CODE_GEN`, so the
generation you took into your workspace is the Previous generation next time.

## Save and load configurations

Save configuration stores the pages and all settings, including the Receive FIFO settings, as an archive in
the `Config` folder. Load configuration restores an archive; then press Load DBC before you open a page or
generate. Loading an older archive that has no Receive FIFO settings keeps your current ones.

## New DBC version checklist

1. Load the new DBC and look at the "New in this DBC" banner.
2. Save the message page and the signal page after checking the green rows.
3. If the receive-rule card is red, open Receive FIFO, check the pre-selected blocks and press Apply.
4. Generate code and work through `MANUAL_ACTIONS.md`.
5. Re-apply edits with the previous generation and your workspace; resolve the listed items.
6. Copy the result into your workspace, build and test on the target (one frame per combined ID).
7. Note the run folder you took into your workspace (the Previous generation next time) and save the configuration.

## Error messages

Every error says what failed, why, and what to do. Details for the tool maintainer are in
`CODE_GEN\errorlog.txt` (code generation) and `logs\cogent.log`.

| Message | What to do |
|---|---|
| CAN receive rules are needed, but the controller accepts 192 | Open Receive FIFO, check the ticked blocks, press Apply, generate again |
| Merge block ... no enabled received message / different DLC / mixes message layers | Open Receive FIFO and remove or change the block marked "Not applied" |
| The saved configuration has no setting for message/signal X | Open the page named in the message, press Save and Back, generate again |
| Message X is multiplexed ... and ... | The reason names what CoGeNT cannot generate (see Multiplexed messages); untick the message's Rx enable, or correct the DBC |
| CODE_GEN\<date_time> could not be created | Check that CODE_GEN is writable and not locked by another program, generate again |
| Node is not defined in the DBC | Use one of the nodes the message lists |
| Re-apply: output folder is inside ... / is not empty | Choose a new output folder |
| Git is needed for re-applying edits | Install Git for Windows |

## Command-line tools

From `Network_CodeGen_S220` with the project's Python:

```
.venv\Scripts\python.exe tools\compare_reference.py --generated CODE_GEN\<date_time> --reference <workspace> --plan CODE_GEN\<date_time>\fifo_plan.json --report compare.md
.venv\Scripts\python.exe tools\carry_forward.py --base CODE_GEN\<earlier run> --edited <workspace> --new CODE_GEN\<date_time> --out <new folder>
```

compare_reference lists, per file, whether the generated file matches your workspace (exactly, apart from white
space and revision notes, or not), compares the receive rules and dispatch entries, and checks that your
`nw_can_dll.c` maps every combined ID. carry_forward does the same as the Re-apply edits page.

## Files and folders

| Path | Content |
|---|---|
| `data\*.data` | The saved settings of the loaded project (pages, Receive FIFO, Re-apply folders) |
| `Config\*.cfg` | Saved configuration archives |
| `CODE_GEN\<date_time>` | One folder per Generate code run: configuration, reports, generated files in the repository folders |
| `MERGED` | Default output of Re-apply edits |
| `logs\cogent.log` | Technical details of failures |
