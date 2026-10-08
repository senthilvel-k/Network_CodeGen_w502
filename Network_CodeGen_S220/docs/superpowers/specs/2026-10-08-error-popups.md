# CoGeNT error popups: root causes and messages

Date: 2026-10-08. Applies to the Python 3 app in this repo (`back_end.py`, generators).

## Reported popup

"Code generation failed: list index out of range". This text exists only in the separate copy
`D:\networkgen\Network_CodeGen_S220` (not this repo). Its `Dbc_Parser.pyw` decides byte order with
`temp_sig[0].split("|")[1].split("@")[0] == 1`, which compares the signal **length** string with the
integer 1. That is never true, so every signal is treated as Motorola. For `VCU5_500` (`VIN_DATA_0 m0 :
0|56@1+`, Intel), the Motorola layout walk in `msg.msg_struct_gen_multiplex` leaves its 7-row grid and
raises `IndexError`. This repo's parser keeps the original rule (`@1` means Intel) and, with the same DBC
and configuration, generates all 11 files byte-identical to `CODE_GEN\DBC_40024_2`.

This repo still has a related latent case: `msg_struct_gen_multiplex` only supports the `VCU5_500`
layout. Each multiplexed signal must start at bit 0 and fit bytes 0-6, and the multiplexor must lie in
byte 7 (`mul_sig_index = 6`). Enabling `BMS19_100`/`BMS20_100` (three signals per multiplexer value at
bits 16+) overflows the grid (`IndexError`), or would emit a struct that drops bits. No correct output for
such messages has ever existed, so supporting them is new C-layout design for the ECU code. This change
**detects the unsupported layout before any file is written** and names the message, the signal and the
fix.

## Message format

```
<Operation> failed while <item>.
Reason: <cause>.
<What the user can do>
Technical details: <log file>          (failures only)
```

Popups never contain a Python traceback. Every failure is logged with its traceback and context to
`logs\cogent.log` (appended). Code generation failures are also written to `CODE_GEN\errorlog.txt`
(the legacy location; overwritten, removed after a successful run).

## Popup inventory (back_end.py)

| Slot | Old popup | Root cause / fix | New behaviour |
|---|---|---|---|
| upload_dbc | "Please enter valid dbc" (shown twice) | Two checks, each alerting | One message naming the empty field(s) |
| upload_dbc | "ERROR! Please Enter Proper node name" | A missing DBC file also landed here (`check__node` swallows `FileNotFoundError`) | "DBC file not found: <path>" checked first |
| upload_dbc | "ERROR! Please Enter Proper node name" | Node not in `BU_` | Names the node, the DBC and the nodes it defines |
| upload_dbc | "ERROR! Please Enter Proper dbc(/node name)" | Parse error swallowed | Reason from the exception; logged |
| code_gen | "Please Click load button to load dbc!!" | Session gate | Explains Load DBC; names the DBC field value |
| code_gen | "Please save Filter, message and signal configurations ..." | Filter is not checked; message did not say which page | Lists the pages not yet saved in this session |
| code_gen | "ERROR! Please check the database file" (shown twice) | Any exception; `errorlog.txt` got only `str(e)`; partial outputs left in CODE_GEN | Generation runs into `CODE_GEN\.staging` and replaces outputs only on success. Message names the output file being generated, the missing configuration entry (message/signal and field) or other cause, and the page to fix. Unsupported multiplex layouts are detected up front |
| Can_dbc0_msg | "... @1" | With no `CanDbcMsgConfiguration.data`, `None.close()` raised after the page was built; other failures hidden by bare `except` | Missing data means an empty configuration (`{}`); real failures reported with reason |
| Can_dbc0_msg/sig | "... @2" / "@4" | No DBC loaded | "Press Load DBC first"; also required when only a stale path from `dbc_details.data` is known (the page was built from `dbc=None`, i.e. empty) |
| Can_dbc0_sig | "... @3" | Missing `CanDbcSigConfiguration.data` produced `data= ];` (broken page); other failures hidden | Missing data means `{}`; reasons reported |
| Can_dbc0_sig | "Please save message configuration ..." | Gate | Clearer wording |
| Can_Filter | "... @5" after every successful open | `try:` commented out, the alert always ran | Alert only on failure, with reason |
| Can_Filter | "... @6" | No DBC loaded | As @2 |
| load_cfg | "please choose proper config file" | Cancel, not a zip, archive without `data/dbc_details.data`, damaged JSON, all through a bare `except` | Cancel shows nothing; each cause named with the file |
| save_cfg | "Configuration saved successfully" shown before writing | Alert ran first | Alert after the archive is written, with its path; failures reported |
| file_browse | (no popup) cancel cleared the DBC field | Empty dialog result written to the field | Cancel keeps the field |
| default_page / onpageload | (no popup) `TypeError` / `NameError`; paths with `'` broke the JS | Wrong variable (`__dbc='None'`), unset names, string-built JS | Values passed with `json.dumps`; missing values shown empty |
| unlock | password messages | UI never calls it | Unchanged |

Success messages keep their original first line ("Database loaded successfully", "Code Generated in
CODE_GEN folder", "Configuration saved successfully", "Configuration loaded successfully"). They may add a
second line with the path.
