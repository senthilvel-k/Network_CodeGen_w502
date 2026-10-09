"""CAN receive-rule / FIFO planning for can_rxrule.cfg and nw_can_dll.h.

The controller has three receive FIFOs (PTR1 0x100, 0x200, 0x400) with at most 64 receive rules
each, 192 in total. can_rx_filt_gen assigns one rule per received message (application messages in
name order: 64 to FIFO 0, 64 to FIFO 1, the rest to FIFO 2, then Diag and NM messages to FIFO 2).

"FIFO multiplexing" (as done by hand for S2XX/40024): an aligned block of CAN IDs is received
through ONE rule whose mask ignores the low ID bits (e.g. 0x3D0 with mask 0x7F0 accepts 0x3D0-0x3DF).
The block's lowest-ID message keeps its rule slot and dispatch entry; the other messages of the block
are removed from can_rxrule.cfg and nw_can_dll.h. nw_can_dll.c (hand-written) must then map each
received ID of the block to its VNIM handle; dispatch_snippet() gives that code.

Configuration: data/CanFifoConfiguration.data (JSON), all keys optional:
  max_rx_rules            total receive rules the controller accepts (default 192)
  max_rules_per_fifo      receive rules per FIFO (default 64)
  merge_blocks            [{"base": "0x3D0", "mask": "0x7F0"}, ...]  ID blocks received through one rule
  additional_rx_messages  ["BMS19_100", ...]  receive these application messages although their
                          page setting is off (their IL/VNIM code is hand-written)
Without the file the generated files are identical to the legacy tool."""
import json
import os
import re
from dataclasses import dataclass, field

CONFIG_FILE = 'CanFifoConfiguration.data'
FIFO_PTR1 = (0x100, 0x200, 0x400)
STANDARD_ID_MASK = 0x7FF
RULE_MASK_FLAGS = 0xC0000000   # RTR and IDE bits always compared (as in the generated masks)
KNOWN_KEYS = ('max_rx_rules', 'max_rules_per_fifo', 'merge_blocks', 'additional_rx_messages')


class FifoConfigError(ValueError):
    """data/CanFifoConfiguration.data cannot be used."""


class FifoPlanError(ValueError):
    """The receive rules cannot be planned as configured (problems lists every reason)."""

    def __init__(self, problems):
        ValueError.__init__(self, "\n".join(problems))
        self.problems = list(problems)


@dataclass(frozen=True)
class MergeBlock:
    base: int
    mask: int

    def contains(self, can_id):
        return (can_id & self.mask) == (self.base & self.mask)

    def label(self):
        low = self.base & self.mask
        high = low | (STANDARD_ID_MASK & ~self.mask)
        return "0x%03X-0x%03X" % (low, high)


@dataclass
class FifoConfig:
    max_rx_rules: int = 192
    max_rules_per_fifo: int = 64
    merge_blocks: list = field(default_factory=list)
    additional_rx_messages: list = field(default_factory=list)
    source: str = None


@dataclass
class RxRule:
    message: dict
    kind: str          # 'IL', 'TP' or 'NM' (DLL_RX_<kind>_FRAME)
    mask: int = RULE_MASK_FLAGS | STANDARD_ID_MASK
    ptr1: int = 0

    @property
    def can_id(self):
        return int(self.message['id'])

    @property
    def name(self):
        return self.message['Msg_name']

    @property
    def dlc(self):
        return self.message['DLC']

    def vnim_handle(self):
        return 'VNIM_' + self.name.upper() + '_MESSAGE'


@dataclass
class MergedGroup:
    block: MergeBlock
    kind: str
    members: list      # message dicts, lowest ID first; members[0] keeps the rule

    @property
    def base(self):
        return self.block.base & self.block.mask

    @property
    def representative(self):
        return self.members[0]


@dataclass
class RxPlan:
    buffers: list                  # three lists of RxRule (FIFO 0, 1, 2)
    groups: list = field(default_factory=list)
    unreceived_in_blocks: list = field(default_factory=list)   # (block, message) accepted by a merged rule but not received before

    def rules(self):
        return [r for buf in self.buffers for r in buf]

    def fifo_counts(self):
        return tuple(len(buf) for buf in self.buffers)


# ---- configuration ----------------------------------------------------------------------------
def _hex_or_int(value, what, path):
    try:
        return int(value, 16) if isinstance(value, str) else int(value)
    except (TypeError, ValueError):
        raise FifoConfigError("%s: %s must be a number such as 0x3D0, got %r" % (path, what, value))


def load_config(data_dir):
    path = os.path.join(data_dir, CONFIG_FILE)
    if not os.path.exists(path):
        return FifoConfig()
    try:
        with open(path, encoding='utf-8') as fh:
            raw = json.load(fh)
    except ValueError as exc:
        raise FifoConfigError("%s is not valid JSON (%s)" % (path, exc))
    if not isinstance(raw, dict):
        raise FifoConfigError("%s must contain a JSON object" % path)
    unknown = sorted(set(raw) - set(KNOWN_KEYS))
    if unknown:
        raise FifoConfigError("%s: unknown setting(s) %s (known: %s)" % (path, ", ".join(unknown), ", ".join(KNOWN_KEYS)))
    cfg = FifoConfig(source=path)
    for key in ('max_rx_rules', 'max_rules_per_fifo'):
        if key in raw:
            value = raw[key]
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise FifoConfigError("%s: %s must be a positive whole number, got %r" % (path, key, value))
            setattr(cfg, key, value)
    blocks = []
    for entry in raw.get('merge_blocks', []):
        if not isinstance(entry, dict) or 'base' not in entry or 'mask' not in entry:
            raise FifoConfigError("%s: each merge_blocks entry needs \"base\" and \"mask\", got %r" % (path, entry))
        base = _hex_or_int(entry['base'], 'merge block base', path)
        mask = _hex_or_int(entry['mask'], 'merge block mask', path)
        if mask & ~STANDARD_ID_MASK or base & ~STANDARD_ID_MASK:
            raise FifoConfigError("%s: merge block 0x%03X/0x%03X: base and mask must be 11-bit standard CAN IDs" % (path, base, mask))
        if base & ~mask:
            raise FifoConfigError("%s: merge block base 0x%03X is not aligned to mask 0x%03X (bits outside the mask must be 0)" % (path, base, mask))
        block = MergeBlock(base, mask)
        for other in blocks:
            if (block.base & other.mask & block.mask) == (other.base & other.mask & block.mask):
                raise FifoConfigError("%s: merge blocks %s and %s overlap" % (path, other.label(), block.label()))
        blocks.append(block)
    cfg.merge_blocks = blocks
    names = raw.get('additional_rx_messages', [])
    if not isinstance(names, list) or not all(isinstance(n, str) and n for n in names):
        raise FifoConfigError("%s: additional_rx_messages must be a list of message names" % path)
    cfg.additional_rx_messages = list(names)
    return cfg


# ---- planning helpers used by can_rx_filt_gen ----------------------------------------------------
def add_additional_messages(il_mes, received, all_rx, config):
    """Add config.additional_rx_messages (application messages) to il_mes, keeping name order."""
    by_name = {m['Msg_name'].upper(): m for m in all_rx}
    have = {m['Msg_name'].upper() for m in received}
    missing = [n for n in config.additional_rx_messages if n.upper() not in by_name]
    if missing:
        raise FifoPlanError(["additional_rx_messages: %s not found among the received messages of the DBC" % ", ".join(missing)])
    added = [by_name[n.upper()] for n in config.additional_rx_messages if n.upper() not in have]
    seen = set()
    added = [m for m in added if not (m['Msg_name'].upper() in seen or seen.add(m['Msg_name'].upper()))]
    return sorted(il_mes + added, key=lambda x: x['Msg_name'])


def merge_blocks(categories, config, all_rx=()):
    """categories: {'IL': [...], 'TP': [...], 'NM': [...]} message dicts in rule order.
    Returns (categories without the merged-away members, {representative id: rule mask}, groups,
    [(block, message) DBC messages inside a block that were not received before])."""
    problems, groups, masks, removed, unreceived = [], [], {}, set(), []
    for block in config.merge_blocks:
        inside = [(kind, m) for kind, msgs in categories.items() for m in msgs if block.contains(int(m['id']))]
        if not inside:
            problems.append("merge block %s: no enabled received message has an ID in this block" % block.label())
            continue
        kinds = sorted({k for k, _ in inside})
        if len(kinds) > 1:
            problems.append("merge block %s mixes message layers %s (%s): one dispatch entry can serve only one layer"
                            % (block.label(), " and ".join(kinds), ", ".join("%s=%s" % (m['Msg_name'], k) for k, m in inside)))
            continue
        dlcs = sorted({m['DLC'] for _, m in inside})
        if len(dlcs) > 1:
            problems.append("merge block %s: messages have different DLC (%s): the dispatch entry checks one DLC for all of them"
                            % (block.label(), ", ".join("%s=%s" % (m['Msg_name'], m['DLC']) for _, m in inside)))
            continue
        members = sorted((m for _, m in inside), key=lambda m: int(m['id']))
        groups.append(MergedGroup(block, kinds[0], members))
        masks[int(members[0]['id'])] = RULE_MASK_FLAGS | block.mask
        removed.update(int(m['id']) for m in members[1:])
        got = {int(m['id']) for m in members}
        unreceived.extend((block, m) for m in sorted(all_rx, key=lambda m: int(m['id']))
                          if block.contains(int(m['id'])) and int(m['id']) not in got)
    if problems:
        raise FifoPlanError(problems)
    reduced = {k: [m for m in msgs if int(m['id']) not in removed] for k, msgs in categories.items()}
    return reduced, masks, groups, unreceived


# ---- checks and diagnostics ----------------------------------------------------------------------
def check_limits(plan, config):
    """Problems (empty list when the plan fits the controller)."""
    problems = []
    counts = plan.fifo_counts()
    total = sum(counts)
    split = ", ".join("FIFO %d: %d" % (i, c) for i, c in enumerate(counts))
    if total > config.max_rx_rules:
        problems.append("%d receive rules are needed but the controller accepts at most %d (%s)" % (total, config.max_rx_rules, split))
    for i, buf in enumerate(plan.buffers):
        if len(buf) > config.max_rules_per_fifo:
            extra = buf[config.max_rules_per_fifo:]
            problems.append("FIFO %d (PTR1 0x%X) has %d receive rules, limit %d; these do not fit: %s"
                            % (i, FIFO_PTR1[i], len(buf), config.max_rules_per_fifo,
                               ", ".join("%s (0x%03X)" % (r.name, r.can_id) for r in extra)))
    return problems


def suggest_merge_blocks(plan, mask=0x7F0):
    """Candidate ID blocks (never applied automatically): >= 2 single-ID rules of the same layer
    and DLC in one aligned block. Sorted by rules saved, then by base ID."""
    full = RULE_MASK_FLAGS | STANDARD_ID_MASK
    by_block = {}
    for r in plan.rules():
        if r.mask == full:
            by_block.setdefault(r.can_id & mask, []).append(r)
    out = []
    for base, rules in by_block.items():
        if len(rules) < 2 or len({(r.kind, r.dlc) for r in rules}) != 1:
            continue
        out.append(MergedGroup(MergeBlock(base, mask), rules[0].kind, sorted((r.message for r in rules), key=lambda m: int(m['id']))))
    return sorted(out, key=lambda g: (-len(g.members), g.base))


def dispatch_snippet(group):
    """C code for DllDispatchReceivedMessage (nw_can_dll.c) mapping every ID of a merged block."""
    base = group.base
    lines = ["\t\t/* 0x%03X Multiplexed Messages (%s share one receive rule) */" % (base, group.block.label()),
             "\t\telse if (((pRmd->Identifier.I32 & 0x%03Xu) == 0x%03Xu) && " % (group.block.mask, base),
             "\t\t\t\t((pRxDispatch[idIndex].identifier & 0x%03Xu) == 0x%03Xu))" % (group.block.mask, base),
             "\t\t{",
             "\t\t\tmatchFound = TRUE;",
             "",
             "\t\t\tswitch (pRmd->Identifier.I32)",
             "\t\t\t{"]
    for m in group.members:
        lines.append("\t\t\t\tcase 0x%03Xu: canFrameHandle = VNIM_%s_MESSAGE; break;" % (int(m['id']), m['Msg_name'].upper()))
    lines += ["\t\t\t\tdefault:", "\t\t\t\t\tmatchFound = FALSE;", "\t\t\t\t\tidIndex++;", "\t\t\t\t\tbreak;",
              "\t\t\t}", "\t\t}"]
    return "\n".join(lines)


def read_rule_table(text):
    """[(id, mask, ptr1)] of a can_rxrule.cfg text, in rule-table order."""
    values = {}
    for n, kind, v in re.findall(r"#define\s+CAN0_RX_RULE(\d+)_(ID|MASK|PTR1)\s+\(CAN_UINT32\)\s*(0x[0-9a-fA-F]+)", text):
        values.setdefault(int(n), {})[kind] = int(v, 16)
    order = [int(n) for n in re.findall(r"\{\s*CAN0_RX_RULE(\d+)_ID\s*,", text)]
    return [(values[n]['ID'], values[n]['MASK'], values[n]['PTR1']) for n in order]


def read_dispatch_counts(text):
    """Number of entries in dllhscanRxIdsVector0/1/2 of a nw_can_dll.h text."""
    counts = []
    for i in range(3):
        m = re.search(r"dllhscanRxIdsVector%d\[ *\] *=\s*\{(.*?)\n\};" % i, text, re.S)
        counts.append(len(re.findall(r"DLL_RX_\w+_FRAME", m.group(1))) if m else 0)
    return tuple(counts)


def plan_summary(plan, config):
    """Machine-readable plan (CODE_GEN/fifo_plan.json)."""
    return {
        "config_file": config.source,
        "limits": {"max_rx_rules": config.max_rx_rules, "max_rules_per_fifo": config.max_rules_per_fifo},
        "fifo_counts": list(plan.fifo_counts()),
        "total_rules": sum(plan.fifo_counts()),
        "merged_blocks": [{"block": g.block.label(), "base": "0x%03X" % g.base, "mask": "0x%03X" % g.block.mask,
                           "layer": g.kind, "rule_id": "0x%03X" % int(g.representative['id']),
                           "members": [{"id": "0x%03X" % int(m['id']), "name": m['Msg_name'],
                                        "vnim_handle": "VNIM_%s_MESSAGE" % m['Msg_name'].upper(), "dlc": m['DLC']}
                                       for m in g.members]} for g in plan.groups],
        "additional_rx_messages": list(config.additional_rx_messages),
        "rules": [{"rule": i + 1, "id": "0x%03X" % r.can_id, "mask": "0x%08X" % r.mask, "fifo_ptr1": "0x%X" % r.ptr1,
                   "name": r.name, "layer": r.kind} for i, r in enumerate(plan.rules())],
    }


def overflow_hint(plan, config):
    """What the user can do when check_limits() reports problems (text for the error popup)."""
    lines = ["No file was changed. Reduce the receive rules to %d or fewer:" % config.max_rx_rules]
    candidates = suggest_merge_blocks(plan)
    if candidates:
        lines.append("- Receive an aligned ID block through one rule: add it to merge_blocks in data\\%s, e.g. %s. "
                     "Candidates (same layer and DLC): %s. Each merged block needs matching dispatch code in "
                     "nw_can_dll.c; CoGeNT writes it to CODE_GEN\\MANUAL_ACTIONS.md."
                     % (CONFIG_FILE,
                        json.dumps({"merge_blocks": [{"base": "0x%03X" % g.base, "mask": "0x%03X" % g.block.mask}
                                                     for g in candidates[:2]]}),
                        "; ".join("%s: %d messages (%s), saves %d rules" % (
                            g.block.label(), len(g.members), ", ".join(m['Msg_name'] for m in g.members[:4])
                            + (", ..." if len(g.members) > 4 else ""), len(g.members) - 1) for g in candidates[:5])))
    lines.append("- Or untick Rx enable for messages this ECU does not need in '+ TX/RX Message Configurations'.")
    lines.append("- If your controller accepts more rules, set max_rx_rules / max_rules_per_fifo in data\\%s." % CONFIG_FILE)
    return "\n".join(lines)


# ---- Manual Action Required report (CODE_GEN/MANUAL_ACTIONS.md) -----------------------------------
CHECK_COMMAND = (r".venv\Scripts\python.exe tools\compare_reference.py --generated CODE_GEN "
                 r"--reference <your workspace> --plan CODE_GEN\fifo_plan.json")
CARRY_COMMAND = (r".venv\Scripts\python.exe tools\carry_forward.py --base <generated files your edits started from> "
                 r"--edited <your workspace> --new CODE_GEN --out <new folder>")


def _entry(status, title, location, current, change, why, dependencies, steps, verification):
    lines = ["## %s: %s" % (status, title), "",
             "- **File and location:** " + location,
             "- **Current value:** " + current,
             "- **Required change:** " + change[0]]
    lines += change[1:]
    lines += ["- **Why CoGeNT cannot do it:** " + why,
              "- **Dependencies:** " + dependencies,
              "- **Steps:**"]
    lines += ["  %d. %s" % (i + 1, s) for i, s in enumerate(steps)]
    lines += ["- **Verification:** " + verification, ""]
    return lines


def manual_actions(plan, config, dbc_name, node, disabled_additional=()):
    """(Markdown text, number of entries that need the user). No time stamps: the same inputs give
    the same file. disabled_additional: additional_rx_messages whose Rx enable is off on the page."""
    counts = plan.fifo_counts()
    out = ["# Manual actions after code generation", "",
           "DBC: `%s`  " % dbc_name, "Node: `%s`  " % node,
           "FIFO configuration: %s  " % ("`data\\%s`" % CONFIG_FILE if config.source
                                       else "none (platform defaults, no merged ID blocks)"),
           "Receive rules: %d of %d (FIFO 0: %d, FIFO 1: %d, FIFO 2: %d; limit %d per FIFO)"
           % (sum(counts), config.max_rx_rules, counts[0], counts[1], counts[2], config.max_rules_per_fifo), "",
           "Status: **AUTOMATIC** = done by CoGeNT in the generated files; **MANUAL** = you must edit a file "
           "or add code CoGeNT does not generate; **REVIEW** = runtime behaviour you should confirm.", ""]
    auto = []
    for g in plan.groups:
        auto.append("- can_rxrule.cfg: IDs %s are received through one rule (ID 0x%03X, mask 0x%08X) instead of %d rules"
                    % (g.block.label(), int(g.representative['id']), RULE_MASK_FLAGS | g.block.mask, len(g.members)))
        auto.append("- nw_can_dll.h: one dispatch entry for the block (0x%03X %s); entries of %s removed"
                    % (int(g.representative['id']), g.representative['Msg_name'],
                       ", ".join(m['Msg_name'] for m in g.members[1:]) or "no other message"))
    for name in config.additional_rx_messages:
        auto.append("- can_rxrule.cfg / nw_can_dll.h: receive rule and dispatch entry for %s (additional_rx_messages)" % name)
    actions = []
    for g in plan.groups:
        ids = ", ".join("0x%03X %s" % (int(m['id']), m['Msg_name']) for m in g.members)
        actions += _entry(
            "MANUAL", "nw_can_dll.c dispatch for the merged block %s" % g.block.label(),
            "`nw_can_dll.c` (hand-written driver file, not generated), function `DllDispatchReceivedMessage`, "
            "inside the loop over `pRxDispatch[]`, before the generic identifier compare",
            "not visible to CoGeNT (the file is in your workspace); tools\\compare_reference.py checks it",
            ["every received ID of the block must select its own VNIM handle (%s). The dispatch table has only the "
             "entry for 0x%03X, so without this branch all of them would be handled as %s:"
             % (ids, int(g.representative['id']), g.representative['Msg_name']),
             "", "```c", dispatch_snippet(g), "```", ""],
            "nw_can_dll.c is not produced by CoGeNT and also contains code CoGeNT does not know.",
            "receive rule 0x%03X/0x%08X in can_rxrule.cfg and its single dispatch entry in nw_can_dll.h (this "
            "generation); the VNIM_*_MESSAGE handles in nw_il_par.h of this generation; DLC %s of every member"
            % (int(g.representative['id']), RULE_MASK_FLAGS | g.block.mask, g.representative['DLC']),
            ["Open nw_can_dll.c of your workspace and find the branch for 0x%03X (search for `0x%03X`)." % (g.base, g.base),
             "Make it map exactly the IDs listed above (add missing IDs, remove IDs that are no longer received).",
             "Keep the `default:` branch: frames the merged rule accepts but no message uses must not be dispatched.",
             "Build the project."],
            "`%s` reports \"All merged IDs are mapped correctly\"; on the target, send each ID once and check that its "
            "VNIM message (not %s) is updated." % (CHECK_COMMAND, g.representative['Msg_name']))
    for g in plan.groups:
        extra = [m for b, m in plan.unreceived_in_blocks if b == g.block]
        known = {int(m['id']) for m in g.members} | {int(m['id']) for m in extra}
        free = [i for i in range(g.base, g.base + (STANDARD_ID_MASK & ~g.block.mask) + 1) if i not in known]
        if not extra and not free:
            continue
        actions += _entry(
            "REVIEW", "frames the merged rule %s accepts in addition" % g.block.label(),
            "can_rxrule.cfg rule 0x%03X (generated)" % int(g.representative['id']),
            "the rule accepts every ID of %s" % g.block.label(),
            ["confirm that these frames may reach the receive FIFO (the dispatch code above drops them):",
             "  - DBC messages of the block that this ECU does not receive: %s"
             % (", ".join("0x%03X %s" % (int(m['id']), m['Msg_name']) for m in extra) or "none"),
             "  - IDs of the block without a DBC message: %s" % (", ".join("0x%03X" % i for i in free) or "none")],
            "one rule with a mask accepts the whole aligned block; which frames are on the bus is a property of your network.",
            "merge_blocks in data\\%s" % CONFIG_FILE,
            ["Check whether any of these IDs is sent on the bus and at what rate.",
             "If they must not reach the FIFO, remove the block from merge_blocks and free receive rules elsewhere."],
            "the FIFO overrun counters stay at 0 in a full-load bus test.")
    for name in config.additional_rx_messages:
        disabled = name.upper() in {n.upper() for n in disabled_additional}
        actions += _entry(
            "MANUAL", "interaction-layer and VNIM code for %s" % name,
            "nw_il_msg.h (%s_msgType), nw_il_par.h / nw_il_par.c (receive frame table, IL_RX_NUM_*), "
            "nw_vnim_app_signals_par.h / .c (VNIM_%s_MSGID and signal handling), vnim.msg.resource, "
            "vnim.txrx.resource, nw_host_mgr_txrx.resource" % (name, name.upper()),
            ("CoGeNT generated no code for %s because its Rx enable is off on '+ TX/RX Message Configurations'"
             % name) if disabled else ("%s is enabled on the page, so CoGeNT generated its code" % name),
            ["add your hand-written code for %s to the files above (CoGeNT generates only its receive rule and "
             "dispatch entry)." % name],
            "CoGeNT generates multiplexed messages only in the VCU5_500 layout; this message needs a layout "
            "that has not been specified for the generator.",
            "nw_can_dll.h of this generation refers to VNIM_%s_MESSAGE, so the build fails until the handle exists."
            % name.upper(),
            ["Re-apply your previous hand edits with `%s` (it reports what could not be merged)." % CARRY_COMMAND,
             "Review the merged files and copy them into your workspace.",
             "Build the project."],
            "the build succeeds; `%s` shows only the differences you expect." % CHECK_COMMAND)
    entries = sum(1 for line in actions if line.startswith("## "))
    if entries == 0:
        out += ["No manual action is required for the receive rules.", ""]
    out += ["## AUTOMATIC", ""]
    out += auto or ["- Nothing beyond the normal generation (no merged ID blocks, no additional messages)."]
    out += [""] + actions
    out += ["## Other hand edits", "",
            "CoGeNT only knows the edits listed above. To re-apply every other edit you made to earlier generated "
            "files (for example code for messages CoGeNT cannot generate), run:", "", "```", CARRY_COMMAND, "```", "",
            "It merges your edits into the new files, writes the result only to the new folder, and lists every "
            "place it could not merge.", ""]
    return "\n".join(out), entries
