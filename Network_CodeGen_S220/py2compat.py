"""Python 2.7 behaviour that the generated C files depend on.

The legacy tool ran on CPython 2.7 for Windows. Two of its behaviours are visible in
the generated files and are reproduced here so that the Python 3 port writes
byte-identical output:

* Py2Dict  - dict whose iteration order is CPython 2.7's hash-table order
             (Objects/dictobject.c of 2.7.18). Python 3 dicts iterate in insertion order.
             The order also depends on the interpreter's word size: every known-good
             output from 2024-06 onward (CODE_GEN/DBC_S237_36144_1, _36144_2, DBC_40024,
             DBC_40024_2) matches **32-bit** Python 2.7 (32-bit C long hash, 32-bit size_t
             probing); older 2023/early-2024 runs were made with 64-bit Python 2.7.
* py2_print - the `print` statement's "softspace" rule (no separator space after an
             item that ends in a newline/tab, trailing-comma prints).
"""
import sys

SIZE_T_BITS = 32  # 32-bit Python 2.7 (see module docstring); 64 reproduces 64-bit runs
_M64 = (1 << SIZE_T_BITS) - 1  # size_t mask used for slot index / perturb arithmetic
_PERTURB_SHIFT = 5
_MINSIZE = 8
_DUMMY = object()
_PY2_WHITESPACE = " \t\n\r\x0b\x0c"


def py2_hash(key):
    """hash(key) as computed by CPython 2.7 where C long is 32 bit (Windows)."""
    if isinstance(key, bool):
        key = int(key)
    if isinstance(key, int):
        if not -(1 << 31) <= key < (1 << 31):
            raise TypeError("only 32-bit int keys are emulated")
        return -2 if key == -1 else key
    if not isinstance(key, str):
        raise TypeError("Py2Dict supports str and int keys, got %r" % type(key))
    if not key:
        return 0
    units = [ord(c) for c in key]
    x = (units[0] << 7) & 0xFFFFFFFF
    for c in units:
        x = ((1000003 * x) ^ c) & 0xFFFFFFFF
    x ^= len(units)
    if x & 0x80000000:
        x -= 1 << 32
    return -2 if x == -1 else x


class Py2Dict(dict):
    """dict that iterates (and returns keys()/values()/items()) in CPython 2.7 order.

    Only insertion, replacement, deletion, copy and update are emulated; that is all
    the generators use. popitem() is refused rather than silently diverging."""

    def __init__(self, items=()):
        super().__init__()
        self._table = [None] * _MINSIZE
        self._fill = 0
        for k, v in items:
            self[k] = v

    # -- CPython 2.7 table mechanics -------------------------------------------------
    def _lookup(self, key, h):
        """Slot of `key`, else the slot insertdict() would use (first dummy or empty)."""
        table = self._table
        mask = len(table) - 1
        i = (h & _M64) & mask
        entry = table[i]
        if entry is None:
            return i
        freeslot = None
        if entry is _DUMMY:
            freeslot = i
        elif entry[1] == h and entry[0] == key:
            return i
        perturb = h & _M64
        while True:
            i = ((i << 2) + i + perturb + 1) & _M64
            j = i & mask
            entry = table[j]
            if entry is None:
                return j if freeslot is None else freeslot
            if entry is not _DUMMY and entry[1] == h and entry[0] == key:
                return j
            if entry is _DUMMY and freeslot is None:
                freeslot = j
            perturb >>= _PERTURB_SHIFT

    def _clean_slot(self, h):
        table = self._table
        mask = len(table) - 1
        i = (h & _M64) & mask
        perturb = h & _M64
        while table[i & mask] is not None:
            i = ((i << 2) + i + perturb + 1) & _M64
            perturb >>= _PERTURB_SHIFT
        return i & mask

    def _resize(self, minused):
        newsize = _MINSIZE
        while newsize <= minused:
            newsize <<= 1
        old = self._table
        self._table = [None] * newsize
        self._fill = 0
        for entry in old:
            if entry is not None and entry is not _DUMMY:
                self._table[self._clean_slot(entry[1])] = entry
                self._fill += 1

    def _insert(self, key, value):
        h = py2_hash(key)
        j = self._lookup(key, h)
        if self._table[j] is None:
            self._fill += 1
        self._table[j] = (key, h)
        dict.__setitem__(self, key, value)

    def _merge(self, other):
        """dict_merge() for a mapping argument (used by copy() and update())."""
        if not other:
            return
        if (self._fill + len(other)) * 3 >= len(self._table) * 2:
            self._resize((len(self) + len(other)) * 2)
        for key in other:
            if dict.__contains__(self, key):
                dict.__setitem__(self, key, other[key])
            else:
                self._insert(key, other[key])

    # -- dict API ------------------------------------------------------------------
    def __setitem__(self, key, value):
        if dict.__contains__(self, key):
            dict.__setitem__(self, key, value)
            return
        self._insert(key, value)
        used = len(self)
        if self._fill * 3 >= len(self._table) * 2:
            self._resize((2 if used > 50000 else 4) * used)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._table[self._lookup(key, py2_hash(key))] = _DUMMY

    def __iter__(self):
        return iter([entry[0] for entry in self._table if entry is not None and entry is not _DUMMY])

    def keys(self):
        return list(self)

    def values(self):
        return [dict.__getitem__(self, k) for k in self]

    def items(self):
        return [(k, dict.__getitem__(self, k)) for k in self]

    def pop(self, key, *default):
        if dict.__contains__(self, key):
            value = dict.__getitem__(self, key)
            del self[key]
            return value
        if default:
            return default[0]
        raise KeyError(key)

    def popitem(self):
        raise NotImplementedError("Py2Dict.popitem is not emulated")

    def setdefault(self, key, default=None):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        self[key] = default
        return default

    def clear(self):
        dict.clear(self)
        self._table = [None] * _MINSIZE
        self._fill = 0

    def update(self, other=(), **kwargs):
        if hasattr(other, "keys"):
            self._merge(other)
        else:
            for k, v in other:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def copy(self):
        new = Py2Dict()
        new._merge(self)
        return new

    def __repr__(self):
        return "{" + ", ".join("%r: %r" % (k, v) for k, v in self.items()) + "}"


_softspace_fallback = {}


def _get_softspace(stream):
    try:
        return stream._py2_softspace
    except AttributeError:
        return _softspace_fallback.get(id(stream), 0)


def _set_softspace(stream, value):
    try:
        stream._py2_softspace = value
    except AttributeError:
        _softspace_fallback[id(stream)] = value


def py2_print(*items, end="\n", file=None, sep=None):
    """Python 2 `print` statement semantics for the call forms 2to3 produces:
    print(a, b) == `print a, b`;  print(a, end=' ') == `print a,`;  print() == `print`."""
    if sep is not None or end not in ("\n", " "):
        raise ValueError("only 2to3-generated print forms are supported")
    out = sys.stdout if file is None else file
    if out is None:  # pythonw without a console
        return
    softspace = _get_softspace(out)
    for item in items:
        if softspace:
            out.write(" ")
        text = item if isinstance(item, str) else str(item)
        out.write(text)
        softspace = not (text and text[-1] in _PY2_WHITESPACE and text[-1] != " ")
    if end == "\n":
        out.write("\n")
        softspace = False
    _set_softspace(out, 1 if softspace else 0)
