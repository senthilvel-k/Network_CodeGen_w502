# Receive FIFO: technical notes

How to use it: see `USER_GUIDE.md`, sections "Receive FIFO", "Generate code" and "Re-apply edits" (also the
Help page in the tool). Everything is done on the Receive FIFO page; nobody edits the settings file by hand.
This note is for developers.

## Limits and assignment

The controller accepts at most 192 CAN receive rules, checked as 64 per receive FIFO (PTR1 `0x100`, `0x200`,
`0x400`); both limits are settings. `can_rx_filt_gen.plan_rx_rules` assigns the rules as the legacy tool did:
application messages in name order, 64 to FIFO 0, 64 to FIFO 1, the rest to FIFO 2, then Diag and NM messages
to FIFO 2. Without merged blocks the output is byte-identical to the legacy tool.

## Settings file

`data/CanFifoConfiguration.data`, written by the Receive FIFO page (`cogent_fifo.save_config`) and saved in
configuration archives:

```
{
 "merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
 "additional_rx_messages": ["BMS19_100", "BMS20_100"]
}
```

Optional keys `max_rx_rules` (192) and `max_rules_per_fifo` (64) are written only when changed.
`additional_rx_messages` receives messages whose Rx enable is off (their code written by hand). Since
CoGeNT generates multiplexed receive messages such as BMS19_100 / BMS20_100 (enable their Rx instead), an
entry for an enabled message changes nothing and `MANUAL_ACTIONS.md` lists it as REVIEW.
`cogent_fifo.config_from_dict` validates everything (11-bit IDs, base aligned to the mask, no overlap, numbers).

## Merged ID blocks

A block (base, mask) is received through one rule: the lowest received ID keeps its rule slot (and FIFO) with
mask `0xC0000000 | mask`; the other members' rules and `nw_can_dll.h` dispatch entries are removed. All members
must share the layer (IL, TP, NM) and the DLC (`cogent_fifo.block_problems`). `nw_can_dll.c` is hand-written and
must map each member ID to its VNIM handle; `MANUAL_ACTIONS.md` contains the code (`cogent_fifo.dispatch_snippet`).
Candidates: aligned 16-ID blocks with at least two single-ID rules of one layer and DLC
(`suggest_merge_blocks`); the page pre-selects the fewest needed (`preselect`, largest saving first).

## Checks in the code generation

1. Before any generator runs: the plan must fit the limits (`check_limits`), otherwise a short error points to
   the Receive FIFO page and the details (overflowing messages, candidates) go to the log.
2. After generation: the staged `can_rxrule.cfg` and `nw_can_dll.h` must contain exactly the planned rules
   (`read_rule_table`, `read_dispatch_counts`) before the run folder `CODE_GEN/<date_time>` is created.
3. Every run folder holds `fifo_plan.json` and `MANUAL_ACTIONS.md`.
