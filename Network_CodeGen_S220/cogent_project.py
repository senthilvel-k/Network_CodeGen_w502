"""Project state shown in the GUI (no Qt): receive-rule usage and merge suggestions for the FIFO card and
the Receive FIFO page, and messages/signals of the DBC that have no saved settings yet ("new")."""

import os

import can_rx_filt_gen
import cogent_fifo

ENABLED = ('on', 'ON', 'On', 1, '1')


class CachedDbc:
    """Message lists of one DBC/node, parsed once (Dbc_Parser is slow). Callers get their own message
    dicts (plain dicts: planning only reads id, name, DLC and the signal list, which is shared)."""

    def __init__(self, dbc, node):
        from Dbc_Parser import dbc_parser
        parser = dbc_parser(dbc, node)
        self.dbc, self.node = dbc, node
        self._lists = {(kind, direction): [dict(m) for m in parser.get_msg_type(kind, direction)]
                       for kind, direction in (('ALL', 'rx'), ('ALL', 'tx'))}

    def get_msg_type(self, kind, direction):
        return [dict(m) for m in self._lists[(kind, direction)]]


_CACHE = {}


def cached_dbc(dbc, node):
    key = (os.path.abspath(dbc), os.path.getmtime(dbc), node)
    if key not in _CACHE:
        _CACHE.clear()
        _CACHE[key] = CachedDbc(dbc, node)
    return _CACHE[key]


class TolerantConfig(dict):
    """Saved message settings where a message without settings counts as disabled (it is listed in
    .missing so the GUI can say that the page has to be saved)."""

    def __init__(self, data):
        dict.__init__(self, data)
        self.missing = set()

    def __missing__(self, key):
        for field, default in (('_rx_enable', ''), ('_tx_enable', ''), ('_msg_type_no_of_events', 'Appl')):
            if key.endswith(field):
                self.missing.add(key[:-len(field)])
                return default
        raise KeyError(key)


def _hex(i):
    return "0x%03X" % int(i)


def _members(messages):
    return [{"id": _hex(m['id']), "name": m['Msg_name']} for m in sorted(messages, key=lambda m: int(m['id']))]


def _with(config, merge_blocks, additional):
    return cogent_fifo.FifoConfig(config.max_rx_rules, config.max_rules_per_fifo, list(merge_blocks),
                                  list(additional), config.source)


def fifo_view(dbc, msg_cfg, config):
    """Everything the FIFO card and the Receive FIFO page show (JSON-serializable)."""
    tolerant = TolerantConfig(msg_cfg)
    rx = dbc.get_msg_type('ALL', 'rx')
    rx_by_name = {m['Msg_name'].upper(): m for m in rx}

    receive_only, additional = [], []
    for name in config.additional_rx_messages:
        m = rx_by_name.get(name.upper())
        if m is None:
            receive_only.append({"name": name, "id": "", "problem": "not a received message of this DBC"})
            continue
        additional.append(name)
        enabled = tolerant[name.upper() + '_rx_enable'] in ENABLED
        receive_only.append({"name": name, "id": _hex(m['id']),
                             "problem": "already enabled on the message page" if enabled else ""})

    def plan_fn(cfg):
        return can_rx_filt_gen.plan_rx_rules(dbc, tolerant, cfg)

    base_plan = plan_fn(_with(config, [], additional))
    categories = {'IL': [], 'TP': [], 'NM': []}
    for r in base_plan.rules():
        categories[r.kind].append(r.message)
    merged, valid = [], []
    for block in config.merge_blocks:
        problems = cogent_fifo.block_problems(categories, block)
        inside = [m for msgs in categories.values() for m in msgs if block.contains(int(m['id']))]
        merged.append({"base": _hex(block.base), "mask": _hex(block.mask), "label": block.label(),
                       "members": _members(inside), "problems": problems, "applied": not problems})
        if not problems:
            valid.append(block)

    effective = _with(config, valid, additional)
    plan = plan_fn(effective)
    problems = cogent_fifo.check_limits(plan, effective)
    candidates = cogent_fifo.suggest_merge_blocks(plan)
    chosen, chosen_fit, chosen_total = [], True, sum(plan.fifo_counts())
    if problems:
        chosen, chosen_fit = cogent_fifo.preselect(plan_fn, effective, candidates)
        chosen_total = sum(plan_fn(_with(effective, valid + chosen, additional)).fifo_counts())
    chosen_keys = {(b.base, b.mask) for b in chosen}
    disabled = [m for m in rx if tolerant[m['Msg_name'].upper() + '_rx_enable'] not in ENABLED
                and m['Msg_name'].upper() not in {n.upper() for n in additional}]
    return {
        "total": sum(plan.fifo_counts()),
        "fifo_counts": list(plan.fifo_counts()),
        "max_rx_rules": config.max_rx_rules,
        "max_rules_per_fifo": config.max_rules_per_fifo,
        "fits": not problems,
        "problems": problems,
        "merged": merged,
        "candidates": [{"base": _hex(g.base), "mask": _hex(g.block.mask), "label": g.block.label(),
                        "members": _members(g.members), "layer": g.kind, "dlc": g.representative['DLC'],
                        "saves": len(g.members) - 1, "preselected": (g.block.base, g.block.mask) in chosen_keys}
                       for g in sorted(candidates, key=lambda g: (-len(g.members), g.base))],
        "preselect_fits": chosen_fit,
        "preselect_total": chosen_total,
        "receive_only": receive_only,
        "receive_only_choices": [{"name": m['Msg_name'], "id": _hex(m['id'])}
                                 for m in sorted(disabled, key=lambda m: m['Msg_name'])],
        "unconfigured": sorted(tolerant.missing),
    }


def new_items(dbc, msg_cfg, sig_cfg):
    """Messages and signals of the DBC without saved settings: the rows the pages highlight green.
    The signal page lists the signals of enabled application (Appl) messages only (Can_dbc_gen.html_sig)."""
    messages, signals = [], []
    for direction in ('tx', 'rx'):
        for m in sorted(dbc.get_msg_type('ALL', direction), key=lambda m: m['Msg_name']):
            name = m['Msg_name'].upper()
            if name + '_%s_enable' % direction not in msg_cfg:
                messages.append({"name": m['Msg_name'], "direction": direction})
            if (msg_cfg.get(name + '_%s_enable' % direction) not in ENABLED
                    or msg_cfg.get(name + '_msg_type_no_of_events') != 'Appl'):
                continue
            for s in m['Sig_List']:
                if s.upper() + '_%s_init_value' % direction not in sig_cfg:
                    signals.append({"name": s, "message": m['Msg_name'], "direction": direction})
    return {"messages": messages, "signals": signals}
