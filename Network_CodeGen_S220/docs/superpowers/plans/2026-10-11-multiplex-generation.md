# Multiplexed receive messages (BMS19_100 / BMS20_100) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** *Generate code* produces the complete code of enabled multiplexed receive messages that the
legacy generator rejects (BMS19_100, BMS20_100) in the layout and receive logic of the S2XX hand code,
and *Re-apply edits* never adds a second copy of that code.

**Architecture:** A new module `cogent_mux.py` builds a layout model of each *indexed message* and renders
every block of its code. The legacy generators (`msg.py`, `il_par_h_generation.py`,
`il_par_c_generation.py`, `vnim_app_signals_par.py`) get small hooks: they skip indexed messages in their
signal-level loops, print the `cogent_mux` blocks where the hand code has them, and use its signal order in
the per-message VNIM templates. `cogent_carry.py` learns which hand-added messages are now generated.

**Tech Stack:** Python 3.12 (`.venv\Scripts\python.exe`), pytest (markers `gui`, `e2e`), PySide6 GUI,
PyInstaller exe.

**Spec:** `docs/superpowers/specs/2026-10-11-multiplex-generation-design.md`

## Global Constraints

- Output for every message that is not an indexed message stays byte-identical (VCU5_500 included):
  all existing golden/regression tests pass unchanged.
- `D:\networkgen\dc.app.scl.vehiclecomm` is only read; tests that need it read it in place and skip when
  it is absent. No workspace content is committed (the repository is public).
- Never commit the user's runtime changes in `data/`, `html/CAN_DBC*.html`, `html/CanDbc*.html`,
  `js/CanDbc*.js`, nor `CODE_GEN/newww/`.
- Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; push only when asked.
- Generated text style: the generator's spaces (no tabs); comparisons with the hand code ignore all
  white space and blank lines.

## Rulings made while planning

- Data union applies when the byte range first..last touched by multiplexed signals contains no byte of a
  fixed signal (spec: "disjoint" bytes; a fixed signal inside the range would overlap the union).
- Only multiplexer values that have signals get an index struct (C has no empty structs); BMS19/BMS20
  use every value.
- No `VNIM_IS_<signal>_MISSING()` (and no `VNIM_RX_<signal>()`) for signals of indexed messages: the hand
  code has neither; the host receives the whole frame. Added to spec section 5.
- The TX/RX signals page gets "Notification for new rows: [select] Apply" so the 130 new BMS signals can be
  set to `200ms_Delay_g1` (their hand code corresponds to that setting) in one step; its init value
  default becomes upper-case hex (`0x1F4`, as in the hand code).

## Review Focus

1. Multiplexer values with gaps (0, 1, 3): structs only for used values, PreCopy branches only for them.
2. A plain non-multiplexed signal in an indexed message: struct placement, PreCopy compare, flag, macros.
3. A frame-union message whose last index uses fewer bytes than the DLC: struct ends at its last used byte.
4. Enabled indexed message without saved signal settings: the generation error names the missing setting.
5. Re-apply with a hand-added message the new DBC does not have: its hand code is not carried.

---

## File Structure

| File | Responsibility |
|---|---|
| `cogent_mux.py` (new) | classification, layout model, rendering of all indexed-message blocks |
| `msg.py` | `find_unsupported_multiplex` uses `cogent_mux`; types of indexed messages after legacy multiplex types |
| `il_par_h_generation.py` | flag count/offset, macros, prototypes, flag area; skips `VNIM_RX_` for indexed |
| `il_par_c_generation.py` | shadows, put/get functions, PreCopy of indexed messages |
| `vnim_app_signals_par.py` | init list, signal orders in per-message templates, skip `VNIM_IS_..._MISSING` |
| `cogent_generate.py` | error text for out-of-scope multiplexed messages |
| `cogent_fifo.py` | no manual action for an enabled `additional_rx_messages` entry |
| `Can_dbc_gen.py`, `style/cogent_pages.js` | init value default upper-case; "apply to new rows" for notification |
| `cogent_carry.py` | hand-added messages now generated / not in the DBC |
| `tests/test_mux_layout.py` (new) | model unit tests on synthetic messages |
| `tests/test_mux_generation.py` (new) | generation of the 40024 fixture with BMS19/BMS20 enabled |
| `tests/test_mux_reference.py` (new) | comparison with the workspace (skips without it) |
| `tests/test_carry_generated.py` (new) | re-apply rules for generated hand-added messages |
| `tests/support.py` | `enable_indexed(home, names, notify)` helper |
| docs | `USER_GUIDE.md`, `FIFO_MULTIPLEXING.md`, `HANDOFF.md`, spec section 5 note |

---

### Task 1: Layout model (`cogent_mux.py`)

**Files:**
- Create: `cogent_mux.py`
- Test: `tests/test_mux_layout.py`

**Interfaces:**
- Produces:
  - `class OutOfScope(ValueError)` with `.msg_name`, `.multiplexor`, `.problem`
  - `classify(mes) -> str` - `'regular' | 'legacy' | 'indexed'`, raises `OutOfScope`
  - `layout(mes) -> Layout`
  - `layouts(messages, msg_cfg) -> dict[str, Layout]` - enabled indexed receive messages, sorted by name;
    raises `OutOfScope` for an enabled multiplexed message that is neither legacy nor in scope
  - `Layout` fields: `name, kind ('data'|'frame'), dlc, multiplexor: Signal, signals: list[Signal]
    (signal order), structs: dict[int, list[Field]], outer: list[Field|None] (None = union member),
    region: (first, last) | None, group: str | None`; properties `msg_lower`, `mux_lower`,
    `group_lower`, `indexes`
  - `Signal` fields: `name, index (int|None), start, length, parts: list[str], widths: list[int],
    path: str, ctype: str, shadow: str|None`; property `one_field`
  - `Field(name, width)`
  - `flag_area(layouts) -> list[(signal_name, byte, mask)]`

- [ ] **Step 1: Write the failing tests**

```python
"""cogent_mux layout model on synthetic messages in the parser's format (Dbc_Parser)."""
import pytest

from cogent_mux import Field, OutOfScope, classify, flag_area, layout, layouts


def mes(name, signals, dlc=8, direction="rx"):
    """signals: (name, mul, start, length[, order]) with mul 'M', 'm<N>' or None (plain)."""
    sig_list = {}
    for s in signals:
        sname, mul, start, length = s[:4]
        d = {"Len": str(length), "Order": s[4] if len(s) > 4 else "Intel", "Endbit": str(start)}
        if mul == "M":
            d["Mul_order"] = "root"
        elif mul:
            d["Mul_order"] = mul.lstrip("m")
        sig_list[sname] = d
    multiplexed = any(s[1] for s in signals)
    return {"Msg_name": name, "DLC": str(dlc), "Multiplex": "YES" if multiplexed else "NO", "DIR": direction,
            "Sig_List": sig_list, "id": "1000"}


# BMS19-like: 8-bit multiplexor in byte 0, 16-bit temperatures from bit 16, index 2 shorter
TEMPS = mes("BMS19_100", [("BMS_CELLTEMP_INDEX", "M", 0, 8)] +
            [("BMS_CELLTEMP%d" % (3 * i + k + 1), "m%d" % i, 16 + 16 * k, 16) for i in range(2) for k in range(3)] +
            [("BMS_CELLTEMP7", "m2", 16, 16), ("BMS_CELLTEMP8", "m2", 32, 16)])
# BMS20-like: 4-bit multiplexor, 10-bit voltages from bit 4
VOLTS = mes("BMS20_100", [("BMS_CELLVOLTAGE_INDEX", "M", 0, 4)] +
            [("BMS_CELLVOLTAGE%d" % (6 * i + k + 1), "m%d" % i, 4 + 10 * k, 10) for i in range(2) for k in range(6)])
VCU5 = mes("VCU5_500", [("VIN_INDEX", "M", 56, 2), ("VIN_DATA_0", "m0", 0, 56), ("VIN_DATA_1", "m1", 0, 56),
                        ("VIN_DATA_2", "m2", 0, 24)])


def test_classification():
    assert classify(VCU5) == "legacy"
    assert classify(TEMPS) == "indexed" and classify(VOLTS) == "indexed"
    assert classify(mes("PLAIN_10", [("A", None, 0, 8)])) == "regular"


def test_data_union_layout_of_bms19():
    lay = layout(TEMPS)
    assert lay.kind == "data" and lay.region == (2, 7) and lay.group == "BMS_CELLTEMP_DATA"
    assert lay.outer == [Field("BMS_CELLTEMP_INDEX", 8), Field("unused1", 8), None]
    assert lay.structs[0] == [Field("BMS_CELLTEMP1_0", 8), Field("BMS_CELLTEMP1_1", 8), Field("BMS_CELLTEMP2_0", 8),
                              Field("BMS_CELLTEMP2_1", 8), Field("BMS_CELLTEMP3_0", 8), Field("BMS_CELLTEMP3_1", 8)]
    assert lay.structs[2] == [Field("BMS_CELLTEMP7_0", 8), Field("BMS_CELLTEMP7_1", 8), Field("BMS_CELLTEMP8_0", 8),
                              Field("BMS_CELLTEMP8_1", 8)]                       # ends at its last used byte
    t1 = lay.signals[0]
    assert (t1.name, t1.path, t1.ctype, t1.shadow) == \
        ("BMS_CELLTEMP1", "bms19_100.bms_celltemp_data.bms_celltemp_index_0", "CAN_UINT16", "BMS19_100__CELLTEMP1")
    assert [s.name for s in lay.signals][-1] == "BMS_CELLTEMP_INDEX"
    assert lay.multiplexor.path == "bms19_100" and lay.multiplexor.one_field


def test_frame_union_layout_of_bms20():
    lay = layout(VOLTS)
    assert lay.kind == "frame" and lay.region is None
    assert lay.structs[0][:4] == [Field("BMS_CELLVOLTAGE_INDEX", 4), Field("BMS_CELLVOLTAGE1_0", 4),
                                  Field("BMS_CELLVOLTAGE1_1", 6), Field("BMS_CELLVOLTAGE2_0", 2)]
    v1 = lay.signals[0]
    assert (v1.parts, v1.widths, v1.path) == (["BMS_CELLVOLTAGE1_0", "BMS_CELLVOLTAGE1_1"], [4, 6],
                                              "bms20_100.bms_cellvoltage_index_0")
    assert lay.multiplexor.path == "bms20_100.bms_cellvoltage_index_0"


def test_signal_order_gaps_and_plain_signal():
    m = mes("GAP_100", [("SEL", "M", 0, 8), ("B", "m3", 16, 8), ("A", "m0", 24, 8), ("CRC", None, 56, 8)])
    lay = layout(m)
    assert [s.name for s in lay.signals] == ["A", "B", "CRC", "SEL"]          # (index, start), plain, mux
    assert lay.indexes == [0, 3] and sorted(lay.structs) == [0, 3]
    assert lay.kind == "data" and lay.region == (2, 3)
    assert lay.outer == [Field("SEL", 8), Field("unused1", 8), None, Field("unused4", 8), Field("unused5", 8),
                         Field("unused6", 8), Field("CRC", 8)]
    assert lay.structs[3] == [Field("B", 8)] and lay.structs[0] == [Field("unused2", 8), Field("A", 8)]


def test_frame_union_index_ends_at_its_last_byte():
    m = mes("SHORT_100", [("SEL", "M", 0, 4), ("A", "m0", 4, 12), ("B", "m1", 4, 4)], dlc=8)
    lay = layout(m)
    assert lay.kind == "frame"
    assert lay.structs[1] == [Field("SEL", 4), Field("B", 4)]


@pytest.mark.parametrize("bad, problem", [
    (mes("MOTO_100", [("S", "M", 0, 8), ("X", "m0", 23, 16, "Motorola")]), "Motorola"),
    (mes("LONG_100", [("S", "M", 0, 8), ("X", "m0", 8, 40)]), "longer than 32 bits"),
    (mes("NOMUX_100", [("X", "m0", 8, 8), ("Y", "m1", 8, 8)]), "no multiplexor"),
    (mes("TX_100", [("S", "M", 0, 8), ("X", "m0", 8, 16)], direction="tx"), "transmitted"),
    (mes("FD_100", [("S", "M", 0, 8), ("X", "m0", 8, 16)], dlc=64), "DLC"),
    (mes("OVER_100", [("S", "M", 0, 8), ("X", "m0", 4, 8)]), "overlaps"),
])
def test_out_of_scope_messages_are_named(bad, problem):
    with pytest.raises(OutOfScope) as exc:
        classify(bad)
    assert problem in exc.value.problem and exc.value.msg_name == bad["Msg_name"]


def test_extended_multiplexing_is_out_of_scope():
    m = mes("EXT_100", [("S", "M", 0, 8), ("X", "m0", 8, 8)])
    m["Sig_List"]["X"]["Mul_order"] = "1M"
    with pytest.raises(OutOfScope) as exc:
        classify(m)
    assert "extended multiplexing" in exc.value.problem


def test_layouts_only_for_enabled_receive_messages():
    cfg = {"BMS19_100_rx_enable": "on", "BMS19_100_msg_type_no_of_events": "Appl",
           "BMS20_100_rx_enable": "", "BMS20_100_msg_type_no_of_events": "Appl",
           "VCU5_500_rx_enable": "on", "VCU5_500_msg_type_no_of_events": "Appl"}
    assert list(layouts([VOLTS, TEMPS, VCU5], cfg)) == ["BMS19_100"]


def test_flag_area_order_multiplexors_last():
    lays = {"BMS19_100": layout(TEMPS), "BMS20_100": layout(VOLTS)}
    area = flag_area(lays)
    assert area[0] == ("BMS_CELLTEMP1", 0, 0x1) and area[7] == ("BMS_CELLTEMP8", 0, 0x80)
    assert area[8] == ("BMS_CELLVOLTAGE1", 1, 0x1)
    assert area[-2:] == [("BMS_CELLTEMP_INDEX", 2, 0x10), ("BMS_CELLVOLTAGE_INDEX", 2, 0x20)]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_mux_layout.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'cogent_mux'`

- [ ] **Step 3: Implement `cogent_mux.py` (model part)**

```python
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
    kind: str
    dlc: int
    multiplexor: Signal
    signals: list
    structs: dict
    outer: list
    region: object = None
    group: object = None

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
    """Byte-aligned bit fields of an Intel signal: names, widths, frame bytes and first bits."""
    bits = range(sig.start, sig.start + sig.length)
    by_byte = {}
    for b in bits:
        by_byte.setdefault(b // 8, []).append(b)
    rows = sorted(by_byte)
    sig.widths = [len(by_byte[r]) for r in rows]
    sig.bytes_ = rows
    sig.parts = [sig.name] if len(rows) == 1 else ['%s_%d' % (sig.name, k) for k in range(len(rows))]
    return [(by_byte[r][0], name, width) for r, name, width in zip(rows, sig.parts, sig.widths)]


def _fields(items, first, last):
    """Bit fields for frame bytes first..last; items: (first bit, name, width) inside those bytes."""
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
        if order == 'root':
            if mux is not None:
                raise OutOfScope(mes['Msg_name'], mux.name, 'it has more than one multiplexor')
            mux = Signal(name, None, int(d['Endbit']), int(d['Len']))
        elif order is not None and not str(order).isdigit():
            raise OutOfScope(mes['Msg_name'], None, 'it uses extended multiplexing (signal %s is multiplexed '
                             'and a multiplexor)' % name)
        else:
            sigs.append(Signal(name, int(order) if order is not None else None, int(d['Endbit']), int(d['Len'])))
        if d['Order'] != 'Intel':
            raise OutOfScope(mes['Msg_name'], None, 'signal %s is Motorola (big-endian); only Intel multiplexed '
                             'messages are supported' % name)
    return mux, sigs


def classify(mes):
    """'regular' (not multiplexed), 'legacy' (VCU5_500 layout) or 'indexed'; OutOfScope otherwise."""
    if mes.get('Multiplex') != 'YES':
        return 'regular'
    import msg
    if all('Mul_order' in d for d in mes['Sig_List'].values()):
        try:
            if msg.multiplex_layout_problem(mes, msg_multiplex(mes)) is None:
                return 'legacy'
        except (KeyError, ValueError):
            pass
    _check(mes)
    return 'indexed'


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
    prefix = os.path.commonprefix([name, ''])
    for s in multiplexed:
        common = os.path.commonprefix([name, s.name])
        s.shadow = '%s_%s' % (name, s.name[len(common):])
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
```

(Remove the unused `prefix = ...` line while implementing; `msg._enable_key` already exists in `msg.py`.)

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_mux_layout.py -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add cogent_mux.py tests/test_mux_layout.py
git commit -m "Layout model for multiplexed receive messages the legacy generator rejects"
```

---

### Task 2: Generation fixture helper, types in nw_il_msg.h and the scope check

**Files:**
- Modify: `msg.py` (`message_structure_generation`, `find_unsupported_multiplex`)
- Modify: `cogent_generate.py:180-197` (`multiplex_error` text)
- Modify: `tests/support.py` (helper)
- Create: `tests/test_mux_generation.py`
- Add to `cogent_mux.py`: `types(lay) -> str`

**Interfaces:**
- Consumes: Task 1 (`layout`, `layouts`, `OutOfScope`)
- Produces: `support.enable_indexed(home, names=("BMS19_100", "BMS20_100"), notify="200ms_Delay_g1")`;
  `tests/test_mux_generation.py::generated(tmp_path)` fixture returning `{file name: text}` of a 40024
  generation with BMS19/BMS20 enabled (module-scoped, generated once)

- [ ] **Step 1: Failing tests**

`tests/support.py` addition:

```python
def enable_indexed(home, names=("BMS19_100", "BMS20_100"), notify="200ms_Delay_g1"):
    """Enable receive messages and give their signals the settings the TX/RX signals page saves for new
    signals (init value = DBC start value), with the notification group of the S2XX BMS signals."""
    import json
    import sys
    sys.path.insert(0, str(ROOT))
    from Dbc_Parser import dbc_parser
    data = Path(home) / "data"
    msg_cfg = json.loads((data / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    sig_cfg = json.loads((data / "CanDbcSigConfiguration.data").read_text(encoding="utf-8"))
    details = json.loads((data / "dbc_details.data").read_text(encoding="utf-8"))
    dbc = dbc_parser(details["file_path"], details["ch0_node_name"])
    for mes in dbc.get_msg_type("ALL", "rx"):
        if mes["Msg_name"] in names:
            msg_cfg[mes["Msg_name"] + "_rx_enable"] = "on"
            for sig, d in mes["Sig_List"].items():
                start = d.get("GenSigStartValue", "0")
                sig_cfg.update({sig + "_green_drive": "", sig + "_os_notify_no_of_events": notify,
                                sig + "_rx_init_value": "0x%X" % int(float(start or 0)),
                                sig + "_signal_content": "", sig + "_signal_fault_id": ""})
    (data / "CanDbcMsgConfiguration.data").write_text(json.dumps(msg_cfg), encoding="utf-8")
    (data / "CanDbcSigConfiguration.data").write_text(json.dumps(sig_cfg), encoding="utf-8")
```

(While implementing, read `dbc_details.data` of the fixture to confirm the key names `file_path` /
`ch0_node_name`; the fixture's `dbc` path is `load_fixture(...).dbc` - use that instead if the details file
holds an absolute path of another machine.)

`tests/test_mux_generation.py`:

```python
"""40024 fixture generated with BMS19_100 / BMS20_100 enabled (indexed multiplexed messages)."""
import json
import re
import shutil
import sys

import pytest

from support import CODE_FILES, ROOT, enable_indexed, load_fixture, run_file

sys.path.insert(0, str(ROOT))
FIXTURE = "s2xx_40024_a"
FIFO = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}]}


def _generate(home, enable):
    from cogent_generate import run_code_generation
    shutil.copytree(load_fixture(FIXTURE).data_dir, home / "data")
    (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps(FIFO), encoding="utf-8")
    if enable:
        enable_indexed(home)
    run_code_generation(str(load_fixture(FIXTURE).dbc), "SMART_CORE", "2000-01-01 00:00")
    return {f: run_file(home, f).read_text(encoding="latin-1") for f in CODE_FILES}


@pytest.fixture(scope="module")
def both(tmp_path_factory):
    import os
    out = {}
    for enable in (False, True):
        home = tmp_path_factory.mktemp("bms_%s" % enable)
        old = os.getcwd()
        os.chdir(home)
        try:
            out[enable] = _generate(home, enable)
        finally:
            os.chdir(old)
    return out


def lines(text):
    return [re.sub(r"\s+", "", l) for l in text.replace("\r", "").split("\n") if l.strip()]


def test_types_follow_the_legacy_multiplex_type(both):
    h = both[True]["nw_il_msg.h"]
    assert h.index("}VCU5_500_msgType;") < h.index("}BMS_CELLTEMP_INDEX_0_sigType;") \
        < h.index("}BMS19_100_msgType;") < h.index("}BMS_CELLVOLTAGE_INDEX_0_sigType;") \
        < h.index("}BMS20_100_msgType;") < h.index("/* ACC1_500 */")
    assert "BMS_CELLTEMP_DATA_Sigbuf  bms_celltemp_data;" in h
    assert lines("typedef union {\n  CAN_UINT8 msgBuffer[8];\n  BMS_CELLVOLTAGE_INDEX_0_sigType  "
                 "bms_cellvoltage_index_0;")[0] in lines(h)


def test_disabled_messages_change_nothing(both):
    assert "BMS19_100" not in both[False]["nw_il_msg.h"]
```

Add to `tests/test_mux_layout.py`:

```python
def test_types_text_of_bms19():
    from cogent_mux import types
    text = types(layout(TEMPS))
    assert "typedef struct {\n  CAN_UINT8 BMS_CELLTEMP1_0:8;" in text
    assert "}BMS_CELLTEMP_INDEX_0_sigType;" in text
    assert "typedef union \n{\n   CAN_UINT8          sig_buffer[6];\n   BMS_CELLTEMP_INDEX_0_sigType  " \
           "bms_celltemp_index_0;" in text
    assert "/* BMS19_100 */\ntypedef struct {\n  CAN_UINT8 BMS_CELLTEMP_INDEX:8;\n  CAN_UINT8 unused1:8;\n" \
           "  BMS_CELLTEMP_DATA_Sigbuf  bms_celltemp_data;\n}BMS19_100_msgType;" in text
```

Add to `tests/test_generation_errors.py` (style of the existing multiplex test there):

```python
def test_out_of_scope_multiplexed_message_is_named(tmp_path, monkeypatch):
    import cogent_mux
    import msg
    monkeypatch.setattr(msg, "find_unsupported_multiplex",
                        lambda dbc, cfg: ("BMS20_100", "BMS_CELLVOLTAGE_INDEX", "signal X is Motorola"))
    # generate with the s2xx fixture as the other tests of this file do, then:
    # assert "BMS20_100" in text and "Motorola" in text and "VCU5_500" not in text
```

(Write it with the file's existing `home`/generation helpers; the assertion is that the popup names the
message and the reason and no longer claims only the VCU5_500 layout exists.)

- [ ] **Step 2: Run** `.venv\Scripts\python.exe -m pytest tests/test_mux_layout.py tests/test_mux_generation.py -q`
Expected: FAIL (`types` missing; generation raises the multiplex error for BMS19_100)

- [ ] **Step 3: Implement**

`cogent_mux.types`:

```python
def _struct(fields, type_name):
    return ['typedef struct {'] + ['  CAN_UINT8 %s:%d;' % (f.name, f.width) for f in fields] + \
        ['}%s;' % type_name, '']


def types(lay):
    out = []
    for i in lay.indexes:
        out += _struct(lay.structs[i], '%s_%d_sigType' % (lay.multiplexor.name, i))
    if lay.kind == 'data':
        out += ['typedef union ', '{', '   CAN_UINT8          sig_buffer[%d];' % (lay.region[1] - lay.region[0] + 1)]
        out += ['   %s_%d_sigType  %s_%d;' % (lay.multiplexor.name, i, lay.mux_lower, i) for i in lay.indexes]
        out += ['}%s_Sigbuf;' % lay.group, '', '/* %s */' % lay.name, 'typedef struct {']
        out += ['  %s_Sigbuf  %s;' % (lay.group, lay.group_lower) if f is None else
                '  CAN_UINT8 %s:%d;' % (f.name, f.width) for f in lay.outer]
        out += ['}%s_msgType;' % lay.name, '']
    else:
        out += ['/* %s */' % lay.name, 'typedef union {', '  CAN_UINT8 msgBuffer[%d];' % lay.dlc]
        out += ['  %s_%d_sigType  %s_%d;' % (lay.multiplexor.name, i, lay.mux_lower, i) for i in lay.indexes]
        out += ['}%s_msgType;' % lay.name, '']
    return '\n'.join(out) + '\n'
```

`msg.py` - `message_structure_generation`: before the loop add
`indexed = cogent_mux.layouts([m for m in Dbc_Msg if m.get('DIR') == 'rx'], vnim_msg_cfg_data)`; in the
`else:` branch (multiplexed) replace `msg_struct_gen_multiplex(mes)` by

```python
        elif mes['Msg_name'].upper() in indexed:
          pass                                   # printed after the legacy multiplexed types
        else:
          msg_struct_gen_multiplex(mes)
```

(adapt the `if/else` so `mes["Multiplex"] == "NO"` keeps its branch), and right after the loop, before
`cl=0`, add `for lay in indexed.values(): print(cogent_mux.types(lay))`.

`msg.find_unsupported_multiplex`: for each enabled multiplexed message call `cogent_mux.classify(mes)`;
return `(mes['Msg_name'], exc.multiplexor, exc.problem)` on `OutOfScope`, else `None` (legacy and indexed
are generated).

`cogent_generate.multiplex_error`: text "message %s is multiplexed (multiplexor %s) and %s. CoGeNT
generates multiplexed receive messages with Intel signals of up to 32 bits, one multiplexor and a DLC of
at most 8, and the VCU5_500 layout." keep the hint.

- [ ] **Step 4: Run** the same tests → pass; plus `tests/test_generation_errors.py` → pass.

- [ ] **Step 5: Commit** `git commit -m "Indexed multiplexed messages: types in nw_il_msg.h, scope check"`

---

### Task 3: nw_il_par.h (flags, counts, macros, prototypes)

**Files:**
- Modify: `il_par_h_generation.py` (`message_structure_generation_tx_rx` count block ~line 454,
  `signal_get_Put` loops at ~749, 801, 852, 891, 930, 944)
- Add to `cogent_mux.py`: `flag_lines(lays)`, `count_lines(regular_signals, lays)`, `put_macros(lays)`,
  `get_macros(lays)`, `put_prototypes(lays)`, `get_prototypes(lays)`
- Test: `tests/test_mux_generation.py`

**Interfaces:** Consumes Task 1-2. Produces the six renderers (each returns a list of lines).

- [ ] **Step 1: Failing tests** (append to `tests/test_mux_generation.py`)

```python
FLAG = re.compile(r"#define (ILSet_\w+)_DataChanged\(\) +(\(il_Rx_DataChanged_Flag\[[^\]]+\].*)")


def flags(text):
    return dict(FLAG.findall(text))


def test_flag_area_and_counts(both):
    h, plain = both[True]["nw_il_par.h"], both[False]["nw_il_par.h"]
    assert "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (162 + 17) " in h
    assert "#define IL_MUX_MSG_OFFSET_ID   162 " in h and "IL_MUX_MSG_OFFSET_ID" not in plain
    f, p = flags(h), flags(plain)
    assert {k: v for k, v in f.items() if k in p} == p                 # every regular flag unchanged
    assert f["ILSet_BMS_CELLTEMP1"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 0] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLVOLTAGE1"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 4] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLTEMP_INDEX"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 16] |= (CAN_UINT8) (0x1))")
    assert f["ILSet_BMS_CELLVOLTAGE_INDEX"].startswith("(il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + 16] |= (CAN_UINT8) (0x2))")


def test_macros_and_prototypes_after_the_regular_ones(both):
    h = both[True]["nw_il_par.h"]
    assert "#define ILRxPut_BMS_CELLTEMP_INDEX(data)    BMS19_100.bms19_100.BMS_CELLTEMP_INDEX= data" in h
    assert "#define ILRxPut_BMS_CELLVOLTAGE_INDEX(data)    " \
           "BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX= data" in h
    put = h.index("#define ILRxPut_BMS_CELLTEMP_INDEX(data)")
    assert h.index("#define ILRxPut_TIME_TO_CHARGE(data)") < put < h.index("Receive Signal Rx Get Macros")
    assert "void ILRxPut_BMS_CELLVOLTAGE1(CAN_UINT16 data);" in h and "CAN_UINT16 IlRxGetBMS_CELLTEMP1(void);" in h
    assert "VNIM_RX_BMS_CELLTEMP1" not in h and "VNIM_RX_BMS_CELLTEMP_INDEX" not in h
```

- [ ] **Step 2: Run** → FAIL

- [ ] **Step 3: Implement**

```python
def count_lines(regular_signals, lays):
    g = (regular_signals + 7) // 8
    m = (len(flag_area(lays)) + 7) // 8
    return ['#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (%d + %d) ' % (g, m), '#define IL_MUX_MSG_OFFSET_ID   %d ' % g]


def flag_lines(lays):
    out = []
    for name, k, mask in flag_area(lays):
        at = 'il_Rx_DataChanged_Flag[IL_MUX_MSG_OFFSET_ID + %d]' % k
        out += ['#define ILSet_%s_DataChanged()        (%s |= (CAN_UINT8) (%s))' % (name, at, hex(mask)),
                '#define ILGet_%s_DataChanged()        (%s & (CAN_UINT8) (%s))' % (name, at, hex(mask)),
                '#define ILClr_%s_DataChanged()        (%s &= (((CAN_UINT8) (0xff)) & ((CAN_UINT8)~%su)))'
                % (name, at, hex(mask)), '']
    return out


def _macro_signals(lay):
    return [s for s in lay.signals if s.one_field and s is not lay.multiplexor] + [lay.multiplexor]


def put_macros(lays):
    return ['#define ILRxPut_%s(data)    %s.%s.%s= data' % (s.name, lay.name, s.path, s.parts[0])
            for lay in lays.values() for s in _macro_signals(lay)]


def get_macros(lays):
    return ['#define IlRxGet%s() \t\t%s.%s.%s' % (s.name, lay.name, s.path, s.parts[0])
            for lay in lays.values() for s in _macro_signals(lay)]


def _function_signals(lay):
    return [s for s in lay.signals if not s.one_field]


def put_prototypes(lays):
    return ['void ILRxPut_%s(%s data);' % (s.name, s.ctype) for lay in lays.values() for s in _function_signals(lay)]


def get_prototypes(lays):
    return ['%s IlRxGet%s(void);' % (s.ctype, s.name) for lay in lays.values() for s in _function_signals(lay)]
```

Hooks in `il_par_h_generation.py` (each function already has `vnim_msg_cfg_data` and `dbc`): add
`indexed = cogent_mux.layouts(dbc.get_msg_type(full_msg, 'rx'), vnim_msg_cfg_data)` once per function;
in each Rx signal loop listed above add `if mes['Msg_name'].upper() in indexed: continue` right after the
`rx_enable` check (put/get macros, prototypes, VNIM_RX, flags); after the put-macro loop
`print('\n'.join(cogent_mux.put_macros(indexed)))` when `indexed`; the same for get macros, put/get
prototypes and `flag_lines` (after the last regular flag macro). In the count block skip indexed messages'
signals in `temp_sig_count` and print `count_lines(temp_sig_count, indexed)` instead of the single
`IL_NUM_OF_RX_DATA_CHANGED_FLAG` line when `indexed` is not empty. Use the module's existing name for the
`'ALL'` constant (`full_msg`).

- [ ] **Step 4: Run** `tests/test_mux_generation.py` and `tests/test_generation_golden.py tests/test_fifo_pipeline.py`
→ pass (golden skip as before).

- [ ] **Step 5: Commit** `git commit -m "Indexed multiplexed messages in nw_il_par.h"`

---

### Task 4: nw_il_par.c (shadows, put/get functions, PreCopy)

**Files:**
- Modify: `il_par_c_generation.py` (`buffer_obj`, `message_Put_rx`, `message_Get_rx`, `message_precopy`)
- Add to `cogent_mux.py`: `shadows(lays)`, `put_functions(lays)`, `get_functions(lays)`, `precopy(lay)`
- Test: `tests/test_mux_layout.py`, `tests/test_mux_generation.py`

- [ ] **Step 1: Failing tests**

`tests/test_mux_layout.py`:

```python
def norm(text):
    import re
    return [re.sub(r"\s+", "", l) for l in text.split("\n") if l.strip()]


def test_put_get_functions_of_a_split_signal():
    from cogent_mux import get_functions, put_functions
    lays = {"BMS20_100": layout(VOLTS)}
    put = norm("\n".join(put_functions(lays)))
    assert put[:5] == norm("void ILRxPut_BMS_CELLVOLTAGE1(CAN_UINT16 data)\n{\n    CAN_ENTER_CRITICAL_SECTION(0);\n"
                           "   BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_0 = (CAN_UINT8) ((data) & 0x0f);\n"
                           "   BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_1 = (CAN_UINT8) (((data) >>4) & 0x3f);")
    get = norm("\n".join(get_functions(lays)))
    assert get[:6] == norm("CAN_UINT16 IlRxGetBMS_CELLVOLTAGE1(void)\n{\n   CAN_UINT16  rValue;\n"
                           "    CAN_ENTER_CRITICAL_SECTION(0);\n"
                           "   rValue = (CAN_UINT16)((CAN_UINT16)BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_0);\n"
                           "   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE1_1) << 4);")


def test_precopy_checks_only_the_received_index():
    from cogent_mux import precopy
    text = norm(precopy(layout(VOLTS)))
    assert text[:4] == norm("void BMS20_100_PreCopy (void)\n{\n   CAN_UINT16 rValue;\n"
                            "   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))")
    assert norm("if((BMS20_100.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX != "
                "Rx_buffer.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX))\n{\n"
                "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();") == text[5:8]
    assert norm("if(Rx_buffer.bms20_100.bms_cellvoltage_index_0.BMS_CELLVOLTAGE_INDEX == 1)")[0] in text
    i = text.index(norm("if(rValue != BMS20_100__CELLVOLTAGE1)")[0])
    assert text[i:i + 5] == norm("if(rValue != BMS20_100__CELLVOLTAGE1)\n{\nBMS20_100__CELLVOLTAGE1 = rValue;\n"
                                 "ILSet_BMS_CELLVOLTAGE1_DataChanged();\n}")


def test_shadows():
    from cogent_mux import shadows
    assert shadows({"BMS19_100": layout(TEMPS)})[0] == "CAN_UINT16 BMS19_100__CELLTEMP1;"
```

`tests/test_mux_generation.py`:

```python
def test_receive_code_after_the_regular_code(both):
    c = both[True]["nw_il_par.c"]
    assert c.index("WLC_NSM_buf WLC_NSM;") < c.index("CAN_UINT16 BMS19_100__CELLTEMP1;")
    assert c.index("void ILRxPut_RESERVED_WLC(") < c.index("void ILRxPut_BMS_CELLTEMP1(CAN_UINT16 data)")
    assert c.index("void IlRxGetRESERVED_WLC(") < c.index("CAN_UINT16 IlRxGetBMS_CELLTEMP1(void)")
    assert c.index("void WLC_NSM_PreCopy (void)") < c.index("void BMS19_100_PreCopy (void)") \
        < c.index("void BMS20_100_PreCopy (void)")
    assert c.count("void BMS19_100_PreCopy") == 1
```

- [ ] **Step 2: Run** → FAIL

- [ ] **Step 3: Implement**

```python
def _mask(width):
    return '0x%02x' % ((1 << width) - 1)


def shadows(lays):
    return ['%s %s;' % (s.ctype, s.shadow) for lay in lays.values() for s in lay.signals if s.shadow]


def _assemble(target, root, s):
    t = s.ctype
    lines, shift = [], 0
    for k, (part, width) in enumerate(zip(s.parts, s.widths)):
        src = '%s.%s.%s' % (root, s.path, part)
        lines.append('%s = (%s)((%s)%s);' % (target, t, t, src) if k == 0 else
                     '%s |= (%s)(((%s)%s) << %d);' % (target, t, t, src, shift))
        shift += width
    return lines


def put_functions(lays):
    out = []
    for lay in lays.values():
        for s in _function_signals(lay):
            out += ['void ILRxPut_%s(%s data)' % (s.name, s.ctype), '{', '    CAN_ENTER_CRITICAL_SECTION(0);']
            shift = 0
            for k, (part, width) in enumerate(zip(s.parts, s.widths)):
                value = '((data) & %s)' % _mask(width) if k == 0 else '(((data) >>%d) & %s)' % (shift, _mask(width))
                out.append('   %s.%s.%s = (CAN_UINT8) %s;' % (lay.name, s.path, part, value))
                shift += width
            out += ['   CAN_EXIT_CRITICAL_SECTION(0);', '}', '']
    return out


def get_functions(lays):
    out = []
    for lay in lays.values():
        for s in _function_signals(lay):
            out += ['%s IlRxGet%s(void)' % (s.ctype, s.name), '{', '   %s  rValue;' % s.ctype,
                    '    CAN_ENTER_CRITICAL_SECTION(0);']
            out += ['   ' + l for l in _assemble('rValue', lay.name, s)]
            out += ['   CAN_EXIT_CRITICAL_SECTION(0);', '   return rValue;', '}', '']
    return out


def precopy(lay):
    widest = max((s.ctype for s in lay.signals if s.shadow), key=lambda t: int(t[8:]))
    mux = lay.multiplexor
    sel = 'Rx_buffer.%s.%s' % (mux.path, mux.parts[0])
    out = ['void %s_PreCopy (void)' % lay.name, '{', '   %s rValue;' % widest, '',
           '   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))', '   {',
           '     if((%s.%s.%s != %s))' % (lay.name, mux.path, mux.parts[0], sel), '     {',
           '         ILSet_%s_DataChanged();' % mux.name, '     }', '']
    for i in lay.indexes:
        out += ['     if(%s == %d)' % (sel, i), '     {']
        for s in [s for s in lay.signals if s.index == i]:
            out += ['         ' + l for l in _assemble('rValue', 'Rx_buffer', s)]
            out += ['         if(rValue != %s)' % s.shadow, '         {', '             %s = rValue;' % s.shadow,
                    '             ILSet_%s_DataChanged();' % s.name, '         }', '']
        out += ['     }', '']
    for s in [s for s in lay.signals if s.index is None and s is not mux]:
        cond = ' || '.join('(%s.%s.%s != Rx_buffer.%s.%s)' % (lay.name, s.path, p, s.path, p) for p in s.parts)
        out += ['     if(%s)' % cond, '     {', '         ILSet_%s_DataChanged();' % s.name, '     }', '']
    out += ['   }', '}', '']
    return '\n'.join(out)
```

Hooks in `il_par_c_generation.py`: compute `indexed` as in Task 3 at the start of each of the four
functions; `buffer_obj`: after the Rx buffer loop `if indexed: print('\n' + '\n'.join(shadows(indexed)))`;
`message_Put_rx` / `message_Get_rx` / `message_precopy`: `continue` for indexed messages inside the
message loop and, after the loop, print `put_functions`, `get_functions`, and `precopy(lay)` for each
layout in name order.

- [ ] **Step 4: Run** `tests/test_mux_layout.py tests/test_mux_generation.py tests/test_fifo_pipeline.py` → pass

- [ ] **Step 5: Commit** `git commit -m "Indexed multiplexed messages in nw_il_par.c"`

---

### Task 5: VNIM (nw_vnim_app_signals_par.c / .h)

**Files:**
- Modify: `vnim_app_signals_par.py` (`vnim_set_init_signals` Rx loop ~436; MsgIndication loops ~659-800;
  Timeout ~854; on-fail case ~1205-1230; IPCL ~1274; `VNIM_IS_..._MISSING` ~1967)
- Add to `cogent_mux.py`: `vnim_order(mes, lays, mux_first=False) -> list[str]`, `init_lines(lays, sig_cfg)`
- Test: `tests/test_mux_generation.py`

- [ ] **Step 1: Failing tests**

```python
def _function(text, head):
    start = text.index(head)
    return text[start:text.index("\n}\n", start)]


def test_vnim_lists_follow_the_hand_code_order(both):
    v = both[True]["nw_vnim_app_signals_par.c"]
    ind = _function(v, "void VnimIlRx_BMS19_100_MsgIndication( void )")
    sets = re.findall(r"ILSet_(\w+)_DataChanged", ind)
    assert sets[0] == "BMS_CELLTEMP1" and sets[-1] == "BMS_CELLTEMP_INDEX"
    gets = re.findall(r"if\(ILGet_(\w+)_DataChanged", ind)
    assert gets[0] == "BMS_CELLTEMP_INDEX" and gets[1] == "BMS_CELLTEMP1"
    assert "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();" in _function(v, "void VnimIlRx_BMS20_100_Timeout( void )")
    case = v[v.index("       case VNIM_BMS20_100_MSGID:\n         ILRxPut_BMS_CELLVOLTAGE1"):]
    case = case[:case.index("break;")]
    assert "NM_MSG_MISSING(VNIM_BMS20_100_MSGID);" in case and "ILSet_BMS_CELLVOLTAGE_INDEX_DataChanged();" in case


def test_init_list_appended_multiplexor_first(both):
    v = both[True]["nw_vnim_app_signals_par.c"]
    i = v.index("   ILRxPut_BMS_CELLTEMP_INDEX(0x0u);")
    assert v.index("ILRxPut_RESERVED_WLC(&Onfail_value_zero[0]);") < i < v.index("   ILRxPut_BMS_CELLTEMP1(0x1F4u);") \
        < v.index("   ILRxPut_BMS_CELLVOLTAGE_INDEX(0x0u);") < v.index("   ILRxPut_BMS_CELLVOLTAGE1(0x0u);")


def test_no_per_signal_application_macros(both):
    assert "VNIM_IS_BMS_CELLTEMP1_MISSING" not in both[True]["nw_vnim_app_signals_par.h"]
```

- [ ] **Step 2: Run** → FAIL

- [ ] **Step 3: Implement**

```python
def vnim_order(mes, lays, mux_first=False):
    lay = lays.get(mes['Msg_name'].upper())
    if lay is None:
        return list(mes['Sig_List'])
    names = [s.name for s in lay.signals]
    return names[-1:] + names[:-1] if mux_first else names


def init_lines(lays, sig_cfg):
    return ['   ILRxPut_%s(%su);' % (name, sig_cfg[name + '_rx_init_value'])
            for lay in lays.values() for name in vnim_order({'Msg_name': lay.name}, lays, mux_first=True)]
```

Hooks: compute `indexed` per function; init list: `continue` for indexed in the Rx loop, then
`print('\n'.join(cogent_mux.init_lines(indexed, vnim_sig_cfg_data)))`; replace
`for signal in mes['Sig_List']:` by `for signal in cogent_mux.vnim_order(mes, indexed):` in the
MsgIndication error-healing `ILSet` loop, Timeout, on-fail case (puts and representative), IPCL case, and
by `vnim_order(mes, indexed, mux_first=True)` in the indication's `ILGet`/`ILClr` loop; in the
`VNIM_IS_..._MISSING` loop skip indexed messages. Signal names in `vnim_order` are already upper case, as
in `Sig_List`.

- [ ] **Step 4: Run** the tests → pass

- [ ] **Step 5: Commit** `git commit -m "Indexed multiplexed messages in the VNIM files"`

---

### Task 6: Signals page defaults, FIFO report

**Files:**
- Modify: `Can_dbc_gen.py:555-558` (`hex(...)` -> `'0x%X' % ...`)
- Modify: `style/cogent_pages.js` (`cogentMarkNew`: notification select + Apply for new rows)
- Modify: `cogent_fifo.py:461-481` (`manual_actions`)
- Test: `tests/gui/test_gui_pages.py` (or the GUI test file that covers the signal page banner),
  `tests/test_fifo_pipeline.py`

- [ ] **Step 1: Failing tests**

```python
# tests/test_fifo_pipeline.py
def test_enabled_additional_message_needs_no_manual_action(home):
    from support import enable_indexed
    _fifo_config(home, REFERENCE_CONFIG)
    enable_indexed(home)
    result = _generate()
    report = (latest_run(home) / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "interaction-layer and VNIM code for BMS19_100" not in report
    assert "## REVIEW: additional_rx_messages lists BMS19_100" in report
```

GUI test (in the file that already tests "Next new" / "Only new"):

```python
def test_apply_notification_to_new_rows(sig_page):            # use that file's fixture opening CAN_DBC_sig
    run(sig_page, "document.getElementById('cogent-new-notify').value = '200ms_Delay_g1';"
                  "document.getElementById('cogent-apply-notify').click();")
    values = run(sig_page, "Array.prototype.map.call(document.querySelectorAll('tr.cogent-new "
                           "select[id$=\"_os_notify_no_of_events\"]'), function (s) { return s.value; }).join()")
    assert set(values.split(",")) == {"200ms_Delay_g1"}
```

- [ ] **Step 2: Run** → FAIL

- [ ] **Step 3: Implement**
  - `Can_dbc_gen.py`: `temp_html_css_content += '0x%X' % int(index['GenSigStartValue'])` inside the `try`.
  - `cogent_pages.js` in `cogentMarkNew`, when there are new rows and the page has notification selects:
    add `<select id="cogent-new-notify">` with the options `No_Delay`, `200ms_Delay_g1`, `200ms_Delay_g2`
    and `<button type="button" id="cogent-apply-notify" class="cg-btn cg-btn-small">Apply to new rows</button>`;
    the button sets `value` of every `tr.cogent-new select[id$="_os_notify_no_of_events"]`.
  - `cogent_fifo.manual_actions`: for an `additional_rx_messages` name that is enabled (not in
    `disabled_additional`), emit a `REVIEW` entry "additional_rx_messages lists X although X is enabled on
    'TX/RX messages'" (its code and receive rule are generated; the entry can be removed) instead of the
    MANUAL entry.

- [ ] **Step 4: Run** the tests → pass

- [ ] **Step 5: Commit** `git commit -m "Signals page: new-row notification in one step; FIFO report for generated messages"`

---

### Task 7: Reference comparison with the workspace

**Files:**
- Create: `tests/test_mux_reference.py`
- Modify: whatever generator detail the comparison shows (in `cogent_mux.py` / hooks), or spec section 9

- [ ] **Step 1: Write the test**

```python
"""Generated BMS19_100 / BMS20_100 code against the S2XX workspace (read in place; skipped without it)."""
import os
import re
from collections import Counter
from pathlib import Path

import pytest

from test_mux_generation import both  # noqa: F401  (module fixture: 40024 with/without BMS)

WS = Path(os.environ.get("COGENT_REFERENCE_WS", r"D:\networkgen\dc.app.scl.vehiclecomm"))
pytestmark = pytest.mark.skipif(not WS.is_dir(), reason="INCOMPLETE: reference workspace not available")
NAMES = re.compile(r"BMS19_100|BMS20_100|BMS_CELLTEMP|BMS_CELLVOLTAGE|IL_MUX_MSG_OFFSET_ID")
# spec section 9: (file, line without white space, 'extra' = only generated | 'missing' = only workspace)
INTENDED = {
    ("nw_il_par.h", "#defineIL_MUX_MSG_OFFSET_ID162", "extra"),
    ("nw_il_par.h", "#defineIL_MUX_MSG_OFFSET_ID161", "missing"),
}


def ws_file(name):
    hits = [p for p in WS.rglob(name) if p.is_file()]
    assert len(hits) == 1, hits
    return hits[0].read_text(encoding="latin-1")


def bms_lines(text):
    out = Counter()
    for line in text.replace("\r", "").split("\n"):
        if NAMES.search(line):
            out[re.sub(r"\s+", "", line)] += 1
    return out


@pytest.mark.parametrize("name", ["nw_il_msg.h", "nw_il_par.h", "nw_il_par.c", "nw_vnim_app_signals_par.c",
                                  "nw_vnim_app_signals_par.h", "vnim.msg.resource", "vnim.txrx.resource",
                                  "nw_host_mgr_txrx.resource"])
def test_bms_lines_match_the_workspace(both, name):
    gen, ws = bms_lines(both[True][name]), bms_lines(ws_file(name))
    extra = {(name, l, "extra") for l in (gen - ws)}
    missing = {(name, l, "missing") for l in (ws - gen)}
    assert extra | missing <= INTENDED | {x for x in extra | missing if "IL_NUM_OF_RX_DATA_CHANGED_FLAG" in x[1]}, \
        "\n".join(sorted("%s %s: %s" % (k, f, l) for f, l, k in (extra | missing) - INTENDED))
```

- [ ] **Step 2: Run** `.venv\Scripts\python.exe -m pytest tests/test_mux_reference.py -q` and read every
listed line. For each: if the generator is wrong, fix it (red-green in the owning task's tests); if the
hand code is wrong (spec section 9) or a hand formatting difference, add it to `INTENDED` with the spec
item; anything not covered by section 9 is added to the spec with its reason.

- [ ] **Step 3: Run** until it passes; also compare whole blocks: the PreCopy functions, indications,
timeouts and on-fail cases of BMS19_100/BMS20_100 (white space removed) between generated and workspace;
differences must be exactly spec section 9 items 2-4.

- [ ] **Step 4: Commit** `git commit -m "Reference comparison of the generated BMS code with the workspace"`

---

### Task 8: Re-apply edits with generated hand-added messages (spec section 14)

**Files:**
- Modify: `cogent_carry.py` (`carry_forward`, `resolve_counts`, report)
- Create: `tests/test_carry_generated.py`

**Interfaces:**
- Produces: `cogent_carry.hand_added(base_h, edited_h) -> list[str]` (message names with a
  `VNIM_<X>_MESSAGE` handle in edited but not in base); `cogent_carry.owned_hunks(...)`; report section
  "Hand-added messages" listing each name with `now generated` / `not in the DBC` / `re-applied`.

- [ ] **Step 1: Failing tests**

```python
"""Re-apply edits when a hand-added message is generated by the new generation (spec section 14)."""
from cogent_carry import hand_added, merge_without


BASE = "#define VNIM_A_MESSAGE 0\n#define VNIM_C_MESSAGE 1\n#define IL_RX_NUM_MESSAGES   2\n"
EDIT = "#define VNIM_A_MESSAGE 0\n#define VNIM_B_MESSAGE 1\n#define VNIM_C_MESSAGE 2\n#define IL_RX_NUM_MESSAGES   3\n" \
       "/* hand */\n"


def test_hand_added_messages_are_found():
    assert hand_added(BASE, EDIT) == ["B"]


def test_regions_of_a_generated_message_are_left_out():
    base = ["x = A_SIG;", "end"]
    edited = ["x = A_SIG;", "y = B_SIG1;", "z = B_SIG2;", "end", "keep = 1;"]
    out = merge_without(base, edited, owned=lambda lines: all("B_" in l for l in lines))
    assert out == ["x = A_SIG;", "end", "keep = 1;"]
```

Plus the real end-to-end test (skips without the workspace): base `CODE_GEN/DBC_40024` (skip if absent),
edited = workspace, new = 41490 generated with BMS19/BMS20 enabled (DBC
`D:\networkgen\DBC\DBC_V41490\..._Edited.dbc`, skip if absent, with the 41490 data of
`local_reports/DBC_41490` or the fixture data plus `enable_indexed`) → `carry_forward(...)`; assert every
check passes, `void BMS19_100_PreCopy` occurs once in the result's `nw_il_par.c`, `IL_RX_NUM_MESSAGES` is
195, `IL_MUX_MSG_OFFSET_ID` is 163, the NM transmit table has 5 entries, and
`NM_MSG_MISSING(VNIM_BMS19_100_MSGID)` occurs once (only in the BMS19 case). And with a DBC copy without
BMS19_100/BMS20_100 (tmp file, `BO_ 1003`/`BO_ 1004` blocks removed): no `BMS19_100` in any result file.

- [ ] **Step 2: Run** → FAIL

- [ ] **Step 3: Implement** in `cogent_carry.py`:
  - `hand_added(base_text, edited_text)`: handles `#define VNIM_(\w+)_MESSAGE` in edited minus base.
  - `merge_without(base_lines, edited_lines, owned)`: edited lines with the base->edited regions
    (difflib opcodes) for which `owned(changed lines)` is true replaced by their base lines.
  - In `carry_forward`: names = `hand_added(...)`; generated = names with a handle in the new `nw_il_par.h`;
    for `generated` and for names absent from the new DBC (the new run's `.cfg` -> `dbc_details.data` ->
    DBC parsed with `Dbc_Parser`; if not readable, treat as present) build the owned predicate: a region is
    owned when its changed lines mention one of those names, a signal of them (`ILSet_<S>_DataChanged`
    defined in edited and not in base, or signals of the message in the new DBC), or
    `IL_MUX_MSG_OFFSET_ID`, and no handle/signal name of a base message; merge with `edited` replaced by
    `merge_without(base, edited, owned)` for every file.
  - `resolve_counts`: subtract `len(generated)` from the user's `IL_RX_NUM_*` delta; take
    `IL_NUM_OF_RX_DATA_CHANGED_FLAG` / `IL_MUX_MSG_OFFSET_ID` from the new generation when it defines
    `IL_MUX_MSG_OFFSET_ID`.
  - Report: one line per hand-added message.

- [ ] **Step 4: Run** `tests/test_carry_generated.py tests/test_carry_forward.py tests/test_carry_rules.py` → pass

- [ ] **Step 5: Commit** `git commit -m "Re-apply edits keeps generated multiplexed messages and drops removed ones"`

---

### Task 9: Documentation, full verification, delivery

**Files:** `USER_GUIDE.md` (and the Help page that renders it), `FIFO_MULTIPLEXING.md`, `HANDOFF.md`,
spec section 5 (VNIM_IS note).

- [ ] **Step 1:** USER_GUIDE: section "Multiplexed messages" (what is generated, how to enable BMS19_100 /
  BMS20_100, the notification Apply, the error table row), Re-apply section (hand-added messages).
- [ ] **Step 2:** Full suites: non-GUI, `-m gui`, rebuild exe, `-m e2e`; all green (record counts).
- [ ] **Step 3:** Generate 41490 with BMS19/BMS20 enabled from the user's 41490 settings (copy of
  `local_reports/DBC_41490` configuration), re-apply the workspace edits, run the analysis scripts against
  the workspace; write `local_reports/DBC_41490/with_generated_bms/` + README (local only).
- [ ] **Step 4:** Commit docs; final whole-branch review (fresh reviewer); fix pass; report to the user.
