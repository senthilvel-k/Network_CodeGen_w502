"""GUI-facing project logic: receive-rule view for the FIFO card/page and new messages/signals."""
import json
import sys

import pytest

from support import ROOT, load_fixture

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024_a"
REFERENCE = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
             "additional_rx_messages": ["BMS19_100", "BMS20_100"]}


@pytest.fixture(scope="module")
def project():
    from cogent_project import cached_dbc
    fx = load_fixture(FIXTURE)
    msg = json.loads((fx.data_dir / "CanDbcMsgConfiguration.data").read_text(encoding="utf-8"))
    sig = json.loads((fx.data_dir / "CanDbcSigConfiguration.data").read_text(encoding="utf-8"))
    return cached_dbc(str(fx.dbc), fx.node), msg, sig


def view(project, raw=None, msg=None):
    from cogent_fifo import config_from_dict
    from cogent_project import fifo_view
    dbc, msg_cfg, _ = project
    return fifo_view(dbc, msg if msg is not None else msg_cfg, config_from_dict(raw or {}))


def test_view_with_the_reference_configuration_fits(project):
    v = view(project, REFERENCE)
    assert (v["total"], v["fits"], v["fifo_counts"], v["max_rx_rules"]) == (184, True, [64, 64, 56], 192)
    assert [(m["label"], m["applied"], len(m["members"])) for m in v["merged"]] == \
        [("0x3D0-0x3DF", True, 13), ("0x4F0-0x4FF", True, 16)]
    assert [r["name"] for r in v["receive_only"]] == ["BMS19_100", "BMS20_100"]
    assert all(r["problem"] == "" for r in v["receive_only"])


def test_view_without_configuration_preselects_the_blocks_needed(project):
    v = view(project, {"additional_rx_messages": ["BMS19_100", "BMS20_100"]})
    assert (v["total"], v["fits"]) == (211, False)
    assert [c["label"] for c in v["candidates"] if c["preselected"]] == ["0x4F0-0x4FF", "0x3D0-0x3DF"]
    assert v["preselect_fits"] is True and v["preselect_total"] == 184
    first = v["candidates"][0]
    assert (first["saves"], first["layer"], first["dlc"]) == (15, "IL", "8")
    assert first["members"][0] == {"id": "0x4F0", "name": "REM_MSG_0"}
    assert any("211 receive rules are needed" in p for p in v["problems"])


def test_view_flags_invalid_kept_block(project):
    v = view(project, {"merge_blocks": [{"base": "0x000", "mask": "0x7F0"}] + REFERENCE["merge_blocks"]})
    bad = v["merged"][0]
    assert (bad["label"], bad["applied"]) == ("0x000-0x00F", False)
    assert "no enabled received message" in bad["problems"][0]
    assert v["total"] == view(project, {"merge_blocks": REFERENCE["merge_blocks"]})["total"]


def test_view_flags_unknown_receive_only_message(project):
    v = view(project, {"additional_rx_messages": ["NOPE_100"]})
    assert v["receive_only"] == [{"name": "NOPE_100", "id": "", "problem": "not a received message of this DBC"}]


def test_receive_only_choices_are_disabled_received_messages(project):
    names = [c["name"] for c in view(project)["receive_only_choices"]]
    assert "BMS19_100" in names and "BMS20_100" in names and "REM_MSG_0" not in names


def test_tolerant_planning_reports_unconfigured(project):
    _, msg_cfg, _ = project
    trimmed = {k: v for k, v in msg_cfg.items() if not k.startswith("VCU5_500_")}
    full, v = view(project), view(project, msg=trimmed)
    assert v["unconfigured"] == ["VCU5_500"]
    assert v["total"] == full["total"] - 1          # counted as disabled until the page is saved


def test_view_is_json_serializable(project):
    json.dumps(view(project, REFERENCE))


def test_new_items_lists_messages_and_signals_without_saved_settings(project):
    from cogent_project import new_items
    dbc, msg_cfg, sig_cfg = project
    base = new_items(dbc, msg_cfg, sig_cfg)
    msg2 = {k: v for k, v in msg_cfg.items() if k != "BMS4_100_rx_enable"}
    sig2 = {k: v for k, v in sig_cfg.items() if k != "BMS_BATTERYPACKSOH_rx_init_value"}
    new = new_items(dbc, msg2, sig2)
    added_msgs = [m for m in new["messages"] if m not in base["messages"]]
    added_sigs = [s for s in new["signals"] if s not in base["signals"]]
    assert added_msgs == [{"name": "BMS4_100", "direction": "rx"}]
    assert added_sigs == [{"name": "BMS_BATTERYPACKSOH", "message": "BMS4_100", "direction": "rx"}]


def test_cached_dbc_returns_independent_copies(project):
    dbc = project[0]
    first = dbc.get_msg_type("ALL", "rx")
    first[0]["Msg_name"] = "CHANGED"
    assert dbc.get_msg_type("ALL", "rx")[0]["Msg_name"] != "CHANGED"
