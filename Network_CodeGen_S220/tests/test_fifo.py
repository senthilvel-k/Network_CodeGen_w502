"""CAN receive FIFO planning: limits, merged ID blocks ("FIFO multiplexing"), diagnostics."""
import json
import sys

import pytest

from support import ROOT, load_fixture

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024_a"   # 40024 _Edited DBC + configuration of the 2026-02-26 12:10 run
REFERENCE_BLOCKS = [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}]


class FakeDbc:
    """Minimal stand-in for Dbc_Parser.dbc_parser (only what plan_rx_rules uses)."""

    def __init__(self, rx, tx=()):
        self._rx, self._tx = list(rx), list(tx)

    def get_msg_type(self, kind, direction):
        assert kind == "ALL"
        return [dict(m) for m in (self._rx if direction == "rx" else self._tx)]


def msg(can_id, name, dlc="8"):
    return {"id": str(can_id), "Msg_name": name, "DLC": dlc}


def il_cfg(messages, kind="Appl"):
    cfg = {}
    for m in messages:
        cfg[m["Msg_name"].upper() + "_rx_enable"] = "on"
        cfg[m["Msg_name"].upper() + "_msg_type_no_of_events"] = kind
    return cfg


def fifo_cfg(**over):
    from cogent_fifo import FifoConfig, MergeBlock
    blocks = [MergeBlock(int(b["base"], 16), int(b["mask"], 16)) for b in over.pop("merge_blocks", [])]
    return FifoConfig(merge_blocks=blocks, **over)


def plan_for_fixture(config):
    from Dbc_Parser import dbc_parser
    import can_rx_filt_gen
    fx = load_fixture(FIXTURE)
    data = json.loads((fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    return can_rx_filt_gen.plan_rx_rules(dbc_parser(str(fx.dbc), fx.node), data, config)


# ---- configuration file --------------------------------------------------------------------
def test_missing_configuration_file_gives_platform_defaults(tmp_path):
    from cogent_fifo import load_config
    cfg = load_config(str(tmp_path))
    assert (cfg.max_rx_rules, cfg.max_rules_per_fifo, cfg.merge_blocks, cfg.additional_rx_messages) == (192, 64, [], [])


def test_configuration_file_is_read(tmp_path):
    from cogent_fifo import load_config
    (tmp_path / "CanFifoConfiguration.data").write_text(json.dumps(
        {"max_rx_rules": 190, "max_rules_per_fifo": 63, "merge_blocks": REFERENCE_BLOCKS,
         "additional_rx_messages": ["BMS19_100"]}), encoding="utf-8")
    cfg = load_config(str(tmp_path))
    assert cfg.max_rx_rules == 190 and cfg.max_rules_per_fifo == 63
    assert [(b.base, b.mask) for b in cfg.merge_blocks] == [(0x3D0, 0x7F0), (0x4F0, 0x7F0)]
    assert cfg.additional_rx_messages == ["BMS19_100"]


@pytest.mark.parametrize("content, words", [
    ("{broken", ["not valid JSON"]),
    ('{"merge_blocks": [{"base": "0x3D1", "mask": "0x7F0"}]}', ["0x3D1", "mask"]),
    ('{"max_rx_rules": "many"}', ["max_rx_rules"]),
    ('{"unknown_key": 1}', ["unknown_key"]),
])
def test_invalid_configuration_is_explained(tmp_path, content, words):
    from cogent_fifo import FifoConfigError, load_config
    (tmp_path / "CanFifoConfiguration.data").write_text(content, encoding="utf-8")
    with pytest.raises(FifoConfigError) as exc:
        load_config(str(tmp_path))
    assert "CanFifoConfiguration.data" in str(exc.value)
    assert all(w in str(exc.value) for w in words)


# ---- planning on synthetic inputs (FIFO boundary) ------------------------------------------
def test_exactly_192_rules_fit():
    from cogent_fifo import check_limits
    rx = [msg(0x100 + i, "M%03d" % i) for i in range(192)]
    plan = __import__("can_rx_filt_gen").plan_rx_rules(FakeDbc(rx), il_cfg(rx), fifo_cfg())
    assert plan.fifo_counts() == (64, 64, 64)
    assert check_limits(plan, fifo_cfg()) == []


def test_193_rules_overflow_and_name_the_messages_that_do_not_fit():
    from cogent_fifo import check_limits
    rx = [msg(0x100 + i, "M%03d" % i) for i in range(193)]
    plan = __import__("can_rx_filt_gen").plan_rx_rules(FakeDbc(rx), il_cfg(rx), fifo_cfg())
    problems = check_limits(plan, fifo_cfg())
    text = "\n".join(problems)
    assert plan.fifo_counts() == (64, 64, 65)
    assert "193" in text and "192" in text and "FIFO 2" in text and "M192" in text


def test_per_fifo_limit_is_configurable():
    from cogent_fifo import check_limits
    rx = [msg(0x100 + i, "M%03d" % i) for i in range(150)]
    plan = __import__("can_rx_filt_gen").plan_rx_rules(FakeDbc(rx), il_cfg(rx), fifo_cfg())
    assert check_limits(plan, fifo_cfg(max_rx_rules=192, max_rules_per_fifo=20)) != []
    assert check_limits(plan, fifo_cfg(max_rx_rules=150, max_rules_per_fifo=64)) == []


def test_merge_block_collapses_members_into_the_lowest_id_and_keeps_its_slot():
    rx = [msg(0x3D0, "A_NSM"), msg(0x3D2, "B_100"), msg(0x3DF, "C_100"), msg(0x123, "D_10")]
    plan = __import__("can_rx_filt_gen").plan_rx_rules(
        FakeDbc(rx), il_cfg(rx), fifo_cfg(merge_blocks=[{"base": "0x3D0", "mask": "0x7F0"}]))
    rules = [(r.can_id, r.mask) for r in plan.rules()]
    assert rules == [(0x3D0, 0xC00007F0), (0x123, 0xC00007FF)]   # sorted by name: A_NSM, D_10
    group = plan.groups[0]
    assert [m["Msg_name"] for m in group.members] == ["A_NSM", "B_100", "C_100"]


def test_merge_block_members_must_share_dlc():
    from cogent_fifo import FifoPlanError
    rx = [msg(0x3D0, "A", "8"), msg(0x3D2, "B", "6")]
    with pytest.raises(FifoPlanError) as exc:
        __import__("can_rx_filt_gen").plan_rx_rules(
            FakeDbc(rx), il_cfg(rx), fifo_cfg(merge_blocks=[{"base": "0x3D0", "mask": "0x7F0"}]))
    assert "0x3D0" in str(exc.value) and "DLC" in str(exc.value) and "B" in str(exc.value)


def test_merge_block_members_must_share_the_layer():
    from cogent_fifo import FifoPlanError
    rx = [msg(0x3D0, "A"), msg(0x3D2, "B")]
    cfg = il_cfg(rx[:1])
    cfg.update(il_cfg(rx[1:], kind="NM"))
    with pytest.raises(FifoPlanError) as exc:
        __import__("can_rx_filt_gen").plan_rx_rules(
            FakeDbc(rx), cfg, fifo_cfg(merge_blocks=[{"base": "0x3D0", "mask": "0x7F0"}]))
    assert "IL" in str(exc.value) and "NM" in str(exc.value)


def test_merge_block_without_enabled_messages_is_reported():
    from cogent_fifo import FifoPlanError
    rx = [msg(0x123, "A")]
    with pytest.raises(FifoPlanError) as exc:
        __import__("can_rx_filt_gen").plan_rx_rules(
            FakeDbc(rx), il_cfg(rx), fifo_cfg(merge_blocks=[{"base": "0x3D0", "mask": "0x7F0"}]))
    assert "0x3D0" in str(exc.value) and "no enabled" in str(exc.value)


def test_additional_rx_message_is_added_in_name_order_once():
    rx = [msg(0x100, "A"), msg(0x200, "C"), msg(0x3EB, "B_MUX")]
    cfg = il_cfg(rx[:2])
    cfg.update({"B_MUX_rx_enable": "", "B_MUX_msg_type_no_of_events": "Appl"})   # disabled on the page
    plan = __import__("can_rx_filt_gen").plan_rx_rules(
        FakeDbc(rx), cfg, fifo_cfg(additional_rx_messages=["B_MUX", "A"]))
    assert [r.name for r in plan.rules()] == ["A", "B_MUX", "C"]


def test_unknown_additional_rx_message_is_reported():
    from cogent_fifo import FifoPlanError
    rx = [msg(0x100, "A")]
    with pytest.raises(FifoPlanError) as exc:
        __import__("can_rx_filt_gen").plan_rx_rules(FakeDbc(rx), il_cfg(rx), fifo_cfg(additional_rx_messages=["NOPE"]))
    assert "NOPE" in str(exc.value)


# ---- planning on the real 40024 configuration ----------------------------------------------
def test_40024_without_merging_overflows_with_candidates():
    from cogent_fifo import check_limits, suggest_merge_blocks
    plan = plan_for_fixture(fifo_cfg())
    assert plan.fifo_counts() == (64, 64, 81)
    assert any("209" in p for p in check_limits(plan, fifo_cfg()))
    candidates = suggest_merge_blocks(plan)
    assert (candidates[0].base, len(candidates[0].members)) == (0x4F0, 16)
    assert (candidates[1].base, len(candidates[1].members)) == (0x3D0, 13)


def test_40024_with_reference_configuration_fits_64_64_56():
    from cogent_fifo import check_limits
    cfg = fifo_cfg(merge_blocks=REFERENCE_BLOCKS, additional_rx_messages=["BMS19_100", "BMS20_100"])
    plan = plan_for_fixture(cfg)
    assert plan.fifo_counts() == (64, 64, 56)
    assert check_limits(plan, cfg) == []
    assert sorted(len(g.members) for g in plan.groups) == [13, 16]


def test_planning_is_deterministic():
    cfg = fifo_cfg(merge_blocks=REFERENCE_BLOCKS, additional_rx_messages=["BMS19_100", "BMS20_100"])
    a, b = plan_for_fixture(cfg), plan_for_fixture(cfg)
    assert [(r.can_id, r.mask, r.ptr1) for r in a.rules()] == [(r.can_id, r.mask, r.ptr1) for r in b.rules()]


def test_rule_table_and_dispatch_readers_handle_omitted_vectors():
    from cogent_fifo import read_dispatch_counts, read_rule_table
    cfg = ("#define  CAN0_RX_RULE1_ID  (CAN_UINT32) 0x3d0u\n#define  CAN0_RX_RULE1_MASK  (CAN_UINT32) 0xC00007F0u\n"
           "#define  CAN0_RX_RULE1_PTR1  (CAN_UINT32) 0x100u\n{CAN0_RX_RULE1_ID, CAN0_RX_RULE1_MASK},\n")
    assert read_rule_table(cfg) == [(0x3D0, 0xC00007F0, 0x100)]
    entry = "   {\n       0x3d0,\n       #if (X)\n         8u,\n       #endif\n       VNIM_A_MESSAGE,\n       DLL_RX_IL_FRAME\n   }"
    dll = ("static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector0[ ] =\n{\n" + entry + ",\n" + entry + "\n};\n"
           " /* CAN Hardware Receive Vector1*/\n /* CAN Hardware Receive Vector2*/\n")   # empty vectors are omitted
    assert read_dispatch_counts(dll) == (2, 0, 0)


def test_dispatch_snippet_lists_every_merged_message():
    from cogent_fifo import dispatch_snippet
    cfg = fifo_cfg(merge_blocks=REFERENCE_BLOCKS)
    plan = plan_for_fixture(cfg)
    g = next(g for g in plan.groups if g.base == 0x3D0)
    code = dispatch_snippet(g)
    assert "(pRmd->Identifier.I32 & 0x7F0u) == 0x3D0u" in code
    assert "case 0x3D2u: canFrameHandle = VNIM_BMS11_100_MESSAGE; break;" in code
    assert code.count("case 0x") == 13
