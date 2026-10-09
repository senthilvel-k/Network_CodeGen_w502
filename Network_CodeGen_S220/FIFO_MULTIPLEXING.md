# CAN receive rules, the 192-rule limit and FIFO multiplexing

CoGeNT writes one CAN receive rule per received message into `can_rxrule.cfg` and one dispatch entry
into `nw_can_dll.h`. The platform limit is **192 receive rules**, checked by default as 64 in each of
the 3 receive FIFOs (PTR1 `0x100`, `0x200`, `0x400`). Both limits can be configured. Application
messages are assigned in name order (64 to FIFO 0,
64 to FIFO 1, the rest to FIFO 2), followed by the Diag and NM messages in FIFO 2. This order is unchanged
from the legacy tool.

## What CoGeNT does on "code gen"

1. **Before any file is written**, it plans the receive rules and checks them against the limits. If they
   do not fit, a popup says how many rules are needed, which FIFO overflows, which messages do not fit,
   and which ID blocks could be merged. Nothing in `CODE_GEN` changes.
2. It applies the merged ID blocks and the additional receive messages from
   `data\CanFifoConfiguration.data` (see below).
3. **After generating**, it checks that `can_rxrule.cfg` and `nw_can_dll.h` contain exactly the planned
   rules before it replaces the files in `CODE_GEN`.
4. It writes two reports next to the generated files:
   - `CODE_GEN\fifo_plan.json`: the limits, the rules per FIFO, every rule (ID, mask, FIFO, message,
     layer) and the merged blocks with their members and VNIM handles.
   - `CODE_GEN\MANUAL_ACTIONS.md`: what CoGeNT did automatically, and every change you still have to
     make by hand (**MANUAL**) or confirm (**REVIEW**). Each entry gives the file and location, the
     current value, the required change, why CoGeNT cannot make it, its dependencies, steps, and how to
     verify it.

   The success popup shows the rule count and, if any, the number of manual actions.

Messages are never dropped to make the rules fit. If they do not fit, you decide what to do (next section).

## data\CanFifoConfiguration.data

A JSON file in the project's `data` folder. All keys are optional. Without the file CoGeNT uses the
platform limits and merges nothing, so its output is then identical to the legacy tool, provided the
rules fit.

| Key | Default | Meaning |
|---|---|---|
| `max_rx_rules` | 192 | Receive rules the controller accepts in total. |
| `max_rules_per_fifo` | 64 | Receive rules per FIFO. |
| `merge_blocks` | `[]` | Aligned ID blocks received through **one** rule, e.g. `{"base": "0x3D0", "mask": "0x7F0"}` = IDs 0x3D0–0x3DF. |
| `additional_rx_messages` | `[]` | Application messages to receive although their Rx enable is off on the message page (their interaction-layer code is hand-written). Only the receive rule and the dispatch entry are generated. |

Example (the S2XX 40024 project; this file is in `data\`):

```json
{
 "merge_blocks": [
  {"base": "0x3D0", "mask": "0x7F0"},
  {"base": "0x4F0", "mask": "0x7F0"}
 ],
 "additional_rx_messages": ["BMS19_100", "BMS20_100"]
}
```

Rules for a merge block (CoGeNT stops with an explanation if one is broken):
- `base` and `mask` are 11-bit IDs. The base must be aligned to the mask (`base & ~mask == 0`), and blocks
  must not overlap.
- At least one received message must lie in the block.
- All received messages in the block must use the same layer (IL, TP or NM) and the same DLC, because the
  single dispatch entry checks one DLC and one layer for all of them.

What a merge block changes:
- `can_rxrule.cfg`: the block's lowest received ID keeps its rule slot (and therefore its FIFO) with mask
  `0xC0000000 | mask`, e.g. `0xC00007F0`. The rules of the other messages in the block are removed.
- `nw_can_dll.h`: only the lowest-ID message keeps a dispatch entry.
- `nw_can_dll.c` is hand-written. Its `DllDispatchReceivedMessage` must map every ID of the block to its own
  VNIM handle. `MANUAL_ACTIONS.md` contains the C code for this branch.
- The rule now accepts the whole block. IDs in the block that this ECU does not receive also reach the
  FIFO, and the dispatch code must drop them. `MANUAL_ACTIONS.md` lists these IDs under **REVIEW**.

The configuration file is saved in configuration archives (`save_cofiguration`, as `data/*.data`). When you
load an older archive that does not contain it, the current file is renamed to
`CanFifoConfiguration.data.previous`, so another project's merges are never applied by accident.

## When the rules do not fit

The popup lists candidate blocks: aligned 16-ID blocks with at least two received messages of the same
layer and DLC, sorted by the number of rules each would save. For each candidate block:
1. Check that its messages may share one rule (the IDs your network uses in that block, and the
   dispatch code you are willing to maintain).
2. Add it to `merge_blocks` and run code gen again.
3. Do the **MANUAL** and **REVIEW** items in `CODE_GEN\MANUAL_ACTIONS.md`.

Alternatives: untick Rx enable for messages the ECU does not need, or raise `max_rx_rules` /
`max_rules_per_fifo` if your controller variant allows more rules.

## Re-applying your other hand edits (hybrid workflow)

CoGeNT cannot know every edit you make after generation. Examples are code for messages whose multiplex
layout it cannot generate, or project-specific hooks. `tools\carry_forward.py` re-applies those edits to a
new generation with a three-way merge:

```
.venv\Scripts\python.exe tools\carry_forward.py --base CODE_GEN\DBC_<old> --edited <your workspace> --new CODE_GEN --out <new folder>
```

- `--base`: the generated files your workspace edits started from. Keep a copy of every generation you
  take into the workspace, as you already do with the `CODE_GEN\DBC_<version>` folders.
- `--edited`: your workspace. Each generated file is found by its name and must be unique there.
- `--new`: the new generation.
- `--out`: a new or empty folder. It must not be inside the other three, which are only read.

For every file, the edits you made (base → workspace) are applied to the new file:
- Where the generator changed the same lines and the two versions differ only in white space, your
  formatting is kept.
- Where they differ only in the header stamp (`Date`, `By`, `Traceability`), the new stamp is kept.
- Every other overlap stays in the file between conflict markers, and `CARRY_FORWARD.md` lists it under
  "Manual Action Required" with your version, the old and the new generated version, and the steps.
- If your file's header names a different DBC than the `--base` file, the report flags it. Its differences
  may then come from that older generation and not from hand edits.

Then compare the result with your workspace:

```
.venv\Scripts\python.exe tools\compare_reference.py --generated <new folder> --reference <your workspace> --plan CODE_GEN\fifo_plan.json --report compare.md
```

This lists, per file, whether it is identical, equal apart from white space and the revision-notes footer,
or different (with the first differing regions). For `can_rxrule.cfg` and `nw_can_dll.h` it also compares the
rules and dispatch entries structurally, and it checks that the workspace's `nw_can_dll.c` maps every merged ID.

Both tools run from the source checkout (`.venv`); they are not part of `CoGeNT.exe`.

## Checklist for a new DBC version

1. Load the DBC, open and save both configuration pages, and run code gen.
2. If the rules do not fit, choose merge blocks (above) and run code gen again.
3. Work through `CODE_GEN\MANUAL_ACTIONS.md`.
4. Copy `CODE_GEN` to `CODE_GEN\DBC_<version>` (the `--base` for next time).
5. Run `tools\carry_forward.py` with the previous `--base` and your workspace, and resolve what
   `CARRY_FORWARD.md` lists.
6. Run `tools\compare_reference.py`, build the project, and test on the target (one frame per merged ID).
