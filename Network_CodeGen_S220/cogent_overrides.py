"""Code overrides: settings for the S2XX hand edits that a plain generation does not reproduce
(data\\CanOverrideConfiguration.data, page 'Code overrides').

    {"tx": {"<MSG>": {"attribute": "Periodic" | "Event" | "Periodic+Event", "period": ms, "offset": ms,
                      "confirmation": true}},
     "rx": {"<MSG>": {"timeout": ms}},
     "nm_tx": [{"message": "<Tx MSG>", "label": "<comment>", "buffer": "<C buffer>"}],
     "host_forward": {"prefix": "REM_MSG_", "function": "host_update_msg"},
     "numeric_order": ["REM_MSG_"]}

Every key is optional; a missing or empty file means no override. cogent_generate loads and checks the
settings and activates them for the generators of one run (activate / deactivate); the generators ask
for the active settings through the functions below, so without settings every file is unchanged."""
import json
import os
import re
from dataclasses import dataclass, field

CONFIG_FILE = 'CanOverrideConfiguration.data'
KNOWN_KEYS = ('tx', 'rx', 'nm_tx', 'host_forward', 'numeric_order')
TX_KEYS = ('attribute', 'period', 'offset', 'confirmation')
TX_ATTRIBUTES = ('Periodic', 'Event', 'Periodic+Event')
IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


class OverrideConfigError(ValueError):
    """The settings are invalid; the message names the file and the entry."""


@dataclass
class TxOverride:
    attribute: str = None          # one of TX_ATTRIBUTES, None: from the DBC send type
    period: int = None             # ms, periodic transmit table row
    offset: int = None             # ms
    confirmation: bool = False     # Tx confirmation / precopy callbacks


@dataclass
class NmTxRow:
    message: str
    label: str
    buffer: str


@dataclass
class Overrides:
    tx: dict = field(default_factory=dict)              # upper-case message name -> TxOverride
    rx: dict = field(default_factory=dict)              # upper-case message name -> timeout in ms
    nm_tx: list = field(default_factory=list)           # NmTxRow, in table order
    host_prefix: str = ''
    host_function: str = ''
    numeric_order: list = field(default_factory=list)   # message name prefixes
    source: str = field(default=None, compare=False)

    def empty(self):
        return not (self.tx or self.rx or self.nm_tx or self.host_prefix or self.numeric_order)


def load(data_dir):
    path = os.path.join(data_dir, CONFIG_FILE)
    if not os.path.exists(path):
        return Overrides()
    try:
        with open(path, encoding='utf-8') as fh:
            raw = json.load(fh)
    except ValueError as exc:   # JSONDecodeError and UnicodeDecodeError
        raise OverrideConfigError("%s is not valid JSON (%s)" % (path, exc)) from exc
    return from_dict(raw, path)


def from_dict(raw, path=None):
    """Overrides from the JSON object of the settings file (or from the page); `path` names the source
    in error messages."""
    where = path or CONFIG_FILE

    def fail(text):
        raise OverrideConfigError("%s: %s" % (where, text))

    if not isinstance(raw, dict):
        fail("must contain a JSON object")
    unknown = sorted(set(raw) - set(KNOWN_KEYS))
    if unknown:
        fail("unknown setting(s) %s (known: %s)" % (", ".join(unknown), ", ".join(KNOWN_KEYS)))
    out = Overrides(source=path)
    for name, entry in _table(raw, 'tx', fail).items():
        if not isinstance(entry, dict):
            fail("tx: %s must be an object" % name)
        extra = sorted(set(entry) - set(TX_KEYS))
        if extra:
            fail("tx: %s: unknown setting(s) %s (known: %s)" % (name, ", ".join(extra), ", ".join(TX_KEYS)))
        attribute = entry.get('attribute')
        if attribute is not None and attribute not in TX_ATTRIBUTES:
            fail("tx: %s: attribute must be one of %s, got %r" % (name, ", ".join(TX_ATTRIBUTES), attribute))
        confirmation = entry.get('confirmation', False)
        if not isinstance(confirmation, bool):
            fail("tx: %s: confirmation must be true or false, got %r" % (name, confirmation))
        out.tx[name] = TxOverride(attribute, _ms(entry, 'period', 'tx: %s' % name, fail, 0),
                                  _ms(entry, 'offset', 'tx: %s' % name, fail, 0), confirmation)
    for name, entry in _table(raw, 'rx', fail).items():
        if not isinstance(entry, dict) or 'timeout' not in entry:
            fail("rx: %s needs a timeout in ms" % name)
        out.rx[name] = _ms(entry, 'timeout', 'rx: %s' % name, fail, 1)
    rows = raw.get('nm_tx', [])
    if not isinstance(rows, list):
        fail("nm_tx must be a list of rows")
    for n, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            fail("nm_tx row %d must be an object" % n)
        values = []
        for key in ('message', 'label', 'buffer'):
            value = row.get(key)
            if not isinstance(value, str) or not IDENTIFIER.match(value):
                fail("nm_tx row %d: %s must be a name (letters, digits, _), got %r" % (n, key, value))
            values.append(value)
        out.nm_tx.append(NmTxRow(values[0].upper(), values[1], values[2]))
    host = raw.get('host_forward')
    if host is not None:
        if not isinstance(host, dict):
            fail("host_forward must be an object with prefix and function")
        for key in ('prefix', 'function'):
            value = host.get(key)
            if not isinstance(value, str) or not IDENTIFIER.match(value):
                fail("host_forward: %s must be a name (letters, digits, _), got %r" % (key, value))
        out.host_prefix, out.host_function = host['prefix'].upper(), host['function']
    prefixes = raw.get('numeric_order', [])
    if not isinstance(prefixes, list):
        fail("numeric_order must be a list of message name prefixes")
    for prefix in prefixes:
        if not isinstance(prefix, str) or not IDENTIFIER.match(prefix):
            fail("numeric_order: %r is not a message name prefix (letters, digits, _)" % (prefix,))
        out.numeric_order.append(prefix.upper())
    return out


def _table(raw, key, fail):
    table = raw.get(key, {})
    if not isinstance(table, dict):
        fail("%s must be an object of message names" % key)
    out = {}
    for name, entry in table.items():
        if not IDENTIFIER.match(name):
            fail("%s: %r is not a message name" % (key, name))
        out[name.upper()] = entry
    return out


def _ms(entry, key, where, fail, minimum):
    value = entry.get(key)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        fail("%s: %s must be a %s whole number of ms, got %r"
             % (where, key, "positive" if minimum else "non-negative", value))
    return value


def to_dict(overrides):
    """The settings file object of `overrides` (only the keys that are set)."""
    out = {}
    if overrides.tx:
        out['tx'] = {name: {k: v for k, v in (('attribute', o.attribute), ('period', o.period),
                                              ('offset', o.offset), ('confirmation', o.confirmation or None))
                            if v is not None}
                     for name, o in overrides.tx.items()}
    if overrides.rx:
        out['rx'] = {name: {'timeout': t} for name, t in overrides.rx.items()}
    if overrides.nm_tx:
        out['nm_tx'] = [{'message': r.message, 'label': r.label, 'buffer': r.buffer} for r in overrides.nm_tx]
    if overrides.host_prefix:
        out['host_forward'] = {'prefix': overrides.host_prefix, 'function': overrides.host_function}
    if overrides.numeric_order:
        out['numeric_order'] = list(overrides.numeric_order)
    return out


def check_names(overrides, tx, rx):
    """Problems of settings that name messages the node does not send (tx, nm_tx) or receive (rx);
    `tx` / `rx` are the upper-case message names of the node in the DBC."""
    problems = ["tx: %s is not a transmit message of the node in the DBC" % n for n in overrides.tx if n not in tx]
    problems += ["rx: %s is not a receive message of the node in the DBC" % n for n in overrides.rx if n not in rx]
    problems += ["nm_tx row %d: %s is not a transmit message of the node in the DBC" % (i, r.message)
                 for i, r in enumerate(overrides.nm_tx, 1) if r.message not in tx]
    return problems


# --------------------------------------------------------------------------- active settings of a run

_active = Overrides()


def activate(overrides):
    global _active
    _active = overrides


def deactivate():
    activate(Overrides())


def active():
    return _active


def apply_messages(messages):
    """Dbc_Parser hook: a receive timeout acts as the DBC cycle time (GenMsgCycleTime) of the message."""
    if not _active.rx:
        return
    for message in messages.values():
        timeout = _active.rx.get(str(message.get('Msg_name', '')).upper())
        if timeout is not None and message.get('DIR') == 'rx':
            message['GenMsgCycleTime'] = str(timeout)


def _number(name, prefix):
    rest = name.upper()[len(prefix):] if name.upper().startswith(prefix) else ''
    return int(rest) if rest.isdigit() else None


def numeric_positions(names, groups=None, prefixes=None):
    """Index order of `names` with numeric_order applied: names made of a prefix and a number are put in
    the order of their numbers (REM_MSG_2 before REM_MSG_10) in the positions they hold, separately per
    group (`groups[i]`, e.g. the node; None: never moved); every other name keeps its position."""
    prefixes = _active.numeric_order if prefixes is None else prefixes
    groups = groups if groups is not None else [''] * len(names)
    members = {}
    for i, name in enumerate(names):
        prefix = next((p for p in prefixes if _number(name, p) is not None), None)
        if prefix is not None and groups[i] is not None:
            members.setdefault((groups[i], prefix), []).append(i)
    order = list(range(len(names)))
    for (_, prefix), slots in members.items():
        for slot, i in zip(slots, sorted(slots, key=lambda i: (_number(names[i], prefix), names[i]))):
            order[slot] = i
    return order
