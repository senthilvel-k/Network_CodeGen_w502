import io
import sys

from support import ROOT

sys.path.insert(0, str(ROOT))

from py2compat import Py2Dict, py2_hash, py2_print  # noqa: E402


def test_py2_hash_matches_cpython27_with_32bit_long():
    # Python 2.7 on Windows (LLP64: C long is 32 bit): hash('a') == -468864544
    assert py2_hash("a") == -468864544
    assert py2_hash("") == 0
    assert py2_hash(5) == 5
    assert py2_hash(-1) == -2


def test_py2dict_is_a_dict_with_normal_mapping_behaviour():
    d = Py2Dict([("b", 1), ("a", 2)])
    d["c"] = 3
    d["a"] = 20
    assert isinstance(d, dict)
    assert d["a"] == 20 and len(d) == 3 and "c" in d
    del d["b"]
    assert sorted(d) == ["a", "c"]
    assert d.pop("c") == 3 and list(d) == ["a"]
    assert d.setdefault("z", 9) == 9 and d["z"] == 9
    assert sorted(d.keys()) == ["a", "z"] and sorted(d.values()) == [9, 20]


def test_py2dict_iteration_reproduces_legacy_signal_order():
    """vnim.txrx.resource from the legacy (Python 2.7) run lists each Tx message's
    signals in CPython 2.7 dict order; inserting them in DBC order must reproduce it."""
    import re
    dbc = ROOT / "DBC" / "S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc"
    legacy = [l.split("VNT_")[1].split("_MSGID")[0]
              for l in open(ROOT / "CODE_GEN" / "DBC_S237_36144_2" / "vnim.txrx.resource", encoding="latin-1")
              if "notify_rcv( VNT_" in l]
    # Signals in DBC file order for message IS6_500 (24 signals).
    text = dbc.read_text(encoding="latin-1")
    block = text.split("BO_ ")
    is6 = next(b for b in block if b.split(" ")[1] == "IS6_500:")
    sigs = [m.upper() for m in re.findall(r"^\s*SG_ (\S+)", is6, re.M)]
    assert len(sigs) == 24
    d = Py2Dict()
    for s in sigs:
        d[s] = {}
    assert list(d) == [s for s in legacy if s in d]


def test_py2dict_uses_32bit_python27_probe_sequence():
    """The latest legacy runs (2024-06 .. 2026-02) were made with 32-bit Python 2.7:
    for message OBC_STS_500 the colliding signals only come out in the legacy order
    when size_t is 32 bit (64-bit Python 2.7 gives a different order)."""
    import re
    dbc = ROOT / "DBC" / "S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc"
    legacy_h = (ROOT / "CODE_GEN" / "DBC_S237_36144_2" / "nw_vnim_app_signals_par.h").read_text(encoding="latin-1")
    legacy = re.findall(r"#define VNIM_IS_(\w+)_MISSING\(\)\s+vnim_is_message_missing\(VNIM_OBC_STS_500_MSGID\)", legacy_h)
    block = next(b for b in dbc.read_text(encoding="latin-1").split("\nBO_ ") if b.split(" ")[1] == "OBC_STS_500:")
    d = Py2Dict()
    for s in re.findall(r"^\s*SG_ (\S+)", block, re.M):
        d[s.upper()] = 1
    assert len(legacy) == 12
    assert list(d) == legacy


def test_py2dict_delete_then_insert_reuses_dummy_slot():
    d = Py2Dict()
    for k in ["k%d" % i for i in range(5)]:
        d[k] = 1
    order_before = list(d)
    del d[order_before[0]]
    d[order_before[0]] = 1          # same key, same hash -> same (dummy) slot again
    assert list(d) == order_before


def test_py2_print_omits_separator_after_item_ending_in_newline():
    out = io.StringIO()
    py2_print("header\n", "\n", file=out)
    assert out.getvalue() == "header\n\n\n"


def test_py2_print_softspace_rules():
    out = io.StringIO()
    py2_print("a", "b", file=out)            # print 'a', 'b'
    py2_print("x", end=" ", file=out)        # print 'x',
    py2_print("y", file=out)                 # print 'y'      -> "x y"
    py2_print("p\n", end=" ", file=out)      # print 'p\n',
    py2_print("q", file=out)                 # print 'q'      -> no space after newline
    py2_print("", "b", 1, file=out)          # print '', 'b', 1
    py2_print(file=out)                      # print
    assert out.getvalue() == "a b\nx y\np\nq\n b 1\n\n"
