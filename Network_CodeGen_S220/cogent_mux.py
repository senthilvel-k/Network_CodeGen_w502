"""Multiplexed receive messages the legacy generator cannot lay out ("indexed messages").

Spec: docs/superpowers/specs/2026-10-11-multiplex-generation-design.md. VCU5_500-style messages (accepted
by msg.multiplex_layout_problem) keep the legacy code. Every other enabled multiplexed receive message in
scope is laid out here; the legacy generators print the blocks rendered here where the S2XX hand code
has them."""
import os
from dataclasses import dataclass, field

ON = ('on', 'On', 'ON', 1, '1')


class OutOfScope(ValueError):
    """An enabled multiplexed message that neither the legacy generator nor this module can generate."""
    def __init__(self, msg_name, multiplexor, problem):
        ValueError.__init__(self, '%s: %s' % (msg_name, problem))
        self.msg_name, self.multiplexor, self.problem = msg_name, multiplexor, problem


@dataclass
class Field:
    name: str
    width: int


@dataclass
class Signal:
    name: str
    index: object            # multiplexer value; None for the multiplexor and plain signals
    start: int
    length: int
    parts: list = field(default_factory=list)
    widths: list = field(default_factory=list)
    bytes_: list = field(default_factory=list)
    path: str = ''
    ctype: str = ''
    shadow: object = None

    @property
    def one_field(self):
        return len(self.parts) == 1


@dataclass
class Layout:
    name: str
    kind: str                # 'data': union of the multiplexed bytes; 'frame': union of whole frames
    dlc: int
    multiplexor: Signal
    signals: list            # signal order: multiplexed (index, start), plain (start), multiplexor
    structs: dict            # multiplexer value -> [Field]
    outer: list              # data union: fields of <MSG>_msgType, None = the union member
    region: object = None    # data union: (first byte, last byte) of the multiplexed signals
    group: object = None     # data union: <GROUP> of <GROUP>_Sigbuf

    @property
    def msg_lower(self):
        return self.name.lower()

    @property
    def mux_lower(self):
        return self.multiplexor.name.lower()

    @property
    def group_lower(self):
        return self.group.lower() if self.group else None

    @property
    def indexes(self):
        return sorted(self.structs)


def _ctype(length):
    return 'CAN_UINT8' if length <= 8 else 'CAN_UINT16' if length <= 16 else 'CAN_UINT32'


def _split(sig):
    """Byte-aligned bit fields of an Intel signal: (first bit, field name, width) per frame byte."""
    by_byte = {}
    for b in range(sig.start, sig.start + sig.length):
        by_byte.setdefault(b // 8, []).append(b)
    rows = sorted(by_byte)
    sig.widths = [len(by_byte[r]) for r in rows]
    sig.bytes_ = rows
    sig.parts = [sig.name] if len(rows) == 1 else ['%s_%d' % (sig.name, k) for k in range(len(rows))]
    return [(by_byte[r][0], name, width) for r, name, width in zip(rows, sig.parts, sig.widths)]


def _fields(items, first, last):
    """Bit fields of frame bytes first..last; items: (first bit, name, width) inside those bytes.
    Gaps are unused<byte> (unused<byte>_<k> for a second gap in the same byte)."""
    out, used = [], set()

    def gap(byte, width):
        name, k = 'unused%d' % byte, 1
        while name in used:
            name, k = 'unused%d_%d' % (byte, k), k + 1
        used.add(name)
        out.append(Field(name, width))

    items = sorted(items)
    for byte in range(first, last + 1):
        bit = 8 * byte
        for start, name, width in [i for i in items if i[0] // 8 == byte]:
            if start > bit:
                gap(byte, start - bit)
            out.append(Field(name, width))
            bit = start + width
        if bit < 8 * byte + 8:
            gap(byte, 8 * byte + 8 - bit)
    return out


def _signals(mes):
    mux, sigs = None, []
    for name, d in mes['Sig_List'].items():
        order = d.get('Mul_order')
        if d['Order'] != 'Intel':
            raise OutOfScope(mes['Msg_name'], None, 'signal %s is Motorola (big-endian); only Intel multiplexed '
                             'messages are supported' % name)
        if order == 'root':
            if mux is not None:
                raise OutOfScope(mes['Msg_name'], mux.name, 'it has more than one multiplexor')
            mux = Signal(name, None, int(d['Endbit']), int(d['Len']))
        elif order is not None and not str(order).isdigit():
            raise OutOfScope(mes['Msg_name'], None, 'it uses extended multiplexing (signal %s is multiplexed '
                             'and a multiplexor)' % name)
        else:
            sigs.append(Signal(name, int(order) if order is not None else None, int(d['Endbit']), int(d['Len'])))
    return mux, sigs


def msg_multiplex(mes):
    """The dict Dbc_Parser.get_multiplex returns, built from the message itself."""
    root = next((n for n, d in mes['Sig_List'].items() if d.get('Mul_order') == 'root'), None)
    values = [int(d['Mul_order']) for d in mes['Sig_List'].values() if d.get('Mul_order') not in (None, 'root')]
    maxval = max(values) if values else 0
    groups = [[] for _ in range(maxval + 1)] if maxval else []
    for n, d in mes['Sig_List'].items():
        if d.get('Mul_order') not in (None, 'root') and groups:
            groups[int(d['Mul_order'])].append(n)
    return {'Multiplexor': root, 'Multiplex_group': groups or None, 'Multiplex_maxval': maxval,
            'Multiplex_group_Name': (root + '_DATA') if root else None}


def _check(mes):
    name = mes['Msg_name']
    if mes.get('DIR') == 'tx':
        raise OutOfScope(name, None, 'it is transmitted; only received multiplexed messages are supported')
    if int(mes['DLC']) > 8:
        raise OutOfScope(name, None, 'its DLC is %s (above 8, CAN FD)' % mes['DLC'])
    mux, sigs = _signals(mes)
    if mux is None:
        raise OutOfScope(name, None, 'it has multiplexed signals but no multiplexor signal (M)')
    for s in sigs:
        if s.index is not None and s.length > 32:
            raise OutOfScope(name, mux.name, 'signal %s is longer than 32 bits' % s.name)
    occupied = {}
    for s in [mux] + sigs:
        if s.start + s.length > 8 * int(mes['DLC']):
            raise OutOfScope(name, mux.name, 'signal %s does not fit in the DLC' % s.name)
        for b in range(s.start, s.start + s.length):
            for other, idx in occupied.get(b, []):
                if idx is None or s.index is None or idx == s.index:
                    raise OutOfScope(name, mux.name, 'signal %s overlaps signal %s' % (s.name, other))
            occupied.setdefault(b, []).append((s.name, s.index))


def classify(mes):
    """'regular' (not multiplexed), 'legacy' (VCU5_500 layout) or 'indexed'; OutOfScope otherwise."""
    if mes.get('Multiplex') != 'YES':
        return 'regular'
    import msg
    if all('Mul_order' in d for d in mes['Sig_List'].values()):
        try:
            if msg.multiplex_layout_problem(mes, msg_multiplex(mes)) is None:
                return 'legacy'
        except (KeyError, ValueError, TypeError):
            pass
    _check(mes)
    return 'indexed'


def layout(mes):
    _check(mes)
    name = mes['Msg_name'].upper()
    mux, sigs = _signals(mes)
    fixed = [s for s in sigs if s.index is None] + [mux]
    multiplexed = [s for s in sigs if s.index is not None]
    items = {id(s): _split(s) for s in fixed + multiplexed}
    fixed_bytes = {b for s in fixed for b in s.bytes_}
    mux_bytes = sorted({b for s in multiplexed for b in s.bytes_})
    region = (mux_bytes[0], mux_bytes[-1])
    by_index = {}
    for s in multiplexed:
        by_index.setdefault(s.index, []).append(s)
    lay = Layout(name, 'data', int(mes['DLC']), mux, [], {}, [])
    if not fixed_bytes & set(range(region[0], region[1] + 1)):
        lay.region = region
        lay.group = (mux.name[:-len('_INDEX')] if mux.name.endswith('_INDEX') else mux.name) + '_DATA'
        for i, members in by_index.items():
            last = max(b for s in members for b in s.bytes_)
            lay.structs[i] = _fields([it for s in members for it in items[id(s)]], region[0], last)
            for s in members:
                s.path = '%s.%s.%s_%d' % (lay.msg_lower, lay.group_lower, lay.mux_lower, i)
        last = max(max(fixed_bytes), region[1])
        outer_items = [it for s in fixed for it in items[id(s)]]
        lay.outer = (_fields(outer_items, 0, region[0] - 1) if region[0] > 0 else []) + [None] + \
            (_fields(outer_items, region[1] + 1, last) if last > region[1] else [])
        for s in fixed:
            s.path = lay.msg_lower
    else:
        lay.kind = 'frame'
        fixed_items = [it for s in fixed for it in items[id(s)]]
        for i, members in by_index.items():
            last = max(b for s in members + fixed for b in s.bytes_)
            lay.structs[i] = _fields(fixed_items + [it for s in members for it in items[id(s)]], 0, last)
            for s in members:
                s.path = '%s.%s_%d' % (lay.msg_lower, lay.mux_lower, i)
        for s in fixed:
            s.path = '%s.%s_%d' % (lay.msg_lower, lay.mux_lower, min(by_index))
    for s in fixed + multiplexed:
        s.ctype = _ctype(s.length)
    for s in multiplexed:
        s.shadow = '%s_%s' % (name, s.name[len(os.path.commonprefix([name, s.name])):])
    lay.signals = sorted(multiplexed, key=lambda s: (s.index, s.start)) + \
        sorted([s for s in fixed if s is not mux], key=lambda s: s.start) + [mux]
    return lay


def enabled(mes, msg_cfg):
    import msg
    key = msg._enable_key(mes, msg_cfg)
    return key is not None and msg_cfg.get(key) in ON


def layouts(messages, msg_cfg):
    """{name: Layout} of the enabled indexed receive messages, sorted by name."""
    out = {}
    for mes in sorted(messages, key=lambda m: m['Msg_name']):
        if mes.get('Multiplex') == 'YES' and enabled(mes, msg_cfg) and classify(mes) == 'indexed':
            out[mes['Msg_name'].upper()] = layout(mes)
    return out


def flag_area(lays):
    """(signal, byte offset, mask) of the multiplex flag area: per message its signals without the
    multiplexor, then all multiplexors."""
    names = [s.name for lay in lays.values() for s in lay.signals if s is not lay.multiplexor] + \
        [lay.multiplexor.name for lay in lays.values()]
    return [(n, k // 8, 1 << (k % 8)) for k, n in enumerate(names)]
