"""cogent_overrides: the Code overrides settings (data\\CanOverrideConfiguration.data)."""
import json
import sys

import pytest

from support import ROOT

sys.path.insert(0, str(ROOT))
import cogent_overrides as co  # noqa: E402

FULL = {
    "tx": {"EX_SUMMARY_RESPONSE_0": {"attribute": "Event", "period": 0, "offset": 0},
           "ic10_200": {"confirmation": True},
           "REM_ACK_MSG": {"attribute": "Periodic+Event"}},
    "rx": {"TC_NSM": {"timeout": 100}},
    "nm_tx": [{"message": "MCM_WAKEUP", "label": "MCM_WAKEUP_REASON", "buffer": "Nm_wakeup_buffer"},
              {"message": "IC_ACTIVE", "label": "IC_ACTIVE", "buffer": "Nm_msg_buffer"}],
    "host_forward": {"prefix": "REM_MSG_", "function": "host_update_msg"},
    "numeric_order": ["REM_MSG_"],
}


def write(tmp_path, raw):
    path = tmp_path / co.CONFIG_FILE
    path.write_text(raw if isinstance(raw, str) else json.dumps(raw), encoding="utf-8")
    return str(tmp_path)


@pytest.fixture(autouse=True)
def no_active_overrides():
    co.deactivate()
    yield
    co.deactivate()


def test_missing_file_means_no_override(tmp_path):
    o = co.load(str(tmp_path))
    assert o.empty() and o.tx == {} and o.rx == {} and o.nm_tx == [] and o.numeric_order == []


def test_empty_object_means_no_override(tmp_path):
    assert co.load(write(tmp_path, {})).empty()


def test_full_file(tmp_path):
    o = co.load(write(tmp_path, FULL))
    assert not o.empty()
    assert o.tx["EX_SUMMARY_RESPONSE_0"] == co.TxOverride("Event", 0, 0, False)
    assert o.tx["IC10_200"] == co.TxOverride(None, None, None, True)          # names are upper-cased
    assert o.rx == {"TC_NSM": 100}
    assert o.nm_tx[0] == co.NmTxRow("MCM_WAKEUP", "MCM_WAKEUP_REASON", "Nm_wakeup_buffer")
    assert (o.host_prefix, o.host_function) == ("REM_MSG_", "host_update_msg")
    assert o.numeric_order == ["REM_MSG_"]


def test_round_trip(tmp_path):
    o = co.load(write(tmp_path, FULL))
    assert co.from_dict(co.to_dict(o)) == co.from_dict(co.to_dict(co.from_dict(co.to_dict(o))))
    assert co.to_dict(o)["tx"]["IC10_200"] == {"confirmation": True}
    assert co.to_dict(co.Overrides()) == {}


@pytest.mark.parametrize("raw, words", [
    ("{not json", ["not valid JSON"]),
    ([1], ["JSON object"]),
    ({"colour": 1}, ["unknown setting", "colour"]),
    ({"tx": {"A": {"attribute": "Cyclic"}}}, ["tx", "A", "attribute", "Periodic, Event, Periodic+Event"]),
    ({"tx": {"A": {"period": -5}}}, ["tx", "A", "period", "whole number"]),
    ({"tx": {"A": {"offset": "10ms"}}}, ["tx", "A", "offset", "whole number"]),
    ({"tx": {"A": {"period": True}}}, ["period", "whole number"]),
    ({"tx": {"A": {"confirmation": "yes"}}}, ["confirmation", "true or false"]),
    ({"tx": {"A": {"speed": 1}}}, ["tx", "A", "speed"]),
    ({"tx": {"A B": {"confirmation": True}}}, ["message name", "A B"]),
    ({"rx": {"TC_NSM": {"timeout": 0}}}, ["rx", "TC_NSM", "timeout", "positive"]),
    ({"rx": {"TC_NSM": {}}}, ["rx", "TC_NSM", "timeout"]),
    ({"nm_tx": [{"label": "X", "buffer": "Nm_msg_buffer"}]}, ["nm_tx", "row 1", "message"]),
    ({"nm_tx": [{"message": "IC_ACTIVE", "label": "X", "buffer": "Nm buffer"}]}, ["nm_tx", "row 1", "buffer"]),
    ({"nm_tx": {"message": "IC_ACTIVE"}}, ["nm_tx", "list"]),
    ({"host_forward": {"prefix": "REM_MSG_"}}, ["host_forward", "function"]),
    ({"host_forward": {"prefix": "", "function": "f"}}, ["host_forward", "prefix"]),
    ({"numeric_order": "REM_MSG_"}, ["numeric_order", "list"]),
    ({"numeric_order": ["REM MSG"]}, ["numeric_order", "REM MSG"]),
])
def test_invalid_settings_are_named(tmp_path, raw, words):
    with pytest.raises(co.OverrideConfigError) as err:
        co.load(write(tmp_path, raw))
    text = str(err.value)
    assert co.CONFIG_FILE in text
    for word in words:
        assert word in text, (word, text)


def test_check_names_against_the_dbc():
    o = co.from_dict(FULL)
    problems = co.check_names(o, tx={"EX_SUMMARY_RESPONSE_0", "IC10_200", "MCM_WAKEUP", "IC_ACTIVE"},
                              rx={"TC_NSM"})
    assert len(problems) == 1 and "REM_ACK_MSG" in problems[0] and "tx" in problems[0]
    problems = co.check_names(o, tx={"EX_SUMMARY_RESPONSE_0", "IC10_200", "REM_ACK_MSG", "IC_ACTIVE"},
                              rx={"TC_NSM"})
    assert len(problems) == 1 and "MCM_WAKEUP" in problems[0] and "nm_tx" in problems[0]
    assert co.check_names(o, tx={"EX_SUMMARY_RESPONSE_0", "IC10_200", "REM_ACK_MSG", "MCM_WAKEUP",
                                 "IC_ACTIVE"}, rx=set()) == [
        "rx: TC_NSM is not a receive message of the node in the DBC"]


def test_numeric_order_only_within_the_prefix_group():
    names = ["A", "REM_MSG_0", "REM_MSG_1", "REM_MSG_10", "REM_MSG_11", "REM_MSG_2", "REM_MSG_9", "Z"]
    order = co.numeric_positions(names, prefixes=["REM_MSG_"])
    assert [names[i] for i in order] == ["A", "REM_MSG_0", "REM_MSG_1", "REM_MSG_2", "REM_MSG_9",
                                        "REM_MSG_10", "REM_MSG_11", "Z"]
    assert co.numeric_positions(names, prefixes=[]) == list(range(len(names)))


def test_numeric_order_keeps_other_names_in_place():
    names = ["REM_MSG_10", "B", "REM_MSG_2", "BMS19_100", "BMS1_10"]
    assert [names[i] for i in co.numeric_positions(names, prefixes=["REM_MSG_"])] == [
        "REM_MSG_2", "B", "REM_MSG_10", "BMS19_100", "BMS1_10"]


def test_numeric_order_respects_groups():
    names = ["REM_MSG_10", "REM_MSG_2", "REM_MSG_11", "REM_MSG_3"]
    groups = ["FCM", "FCM", "TGU", "TGU"]
    assert [names[i] for i in co.numeric_positions(names, groups, prefixes=["REM_MSG_"])] == [
        "REM_MSG_2", "REM_MSG_10", "REM_MSG_3", "REM_MSG_11"]
    groups = [None, "FCM", "FCM", "FCM"]                     # None: never moved (a key message)
    assert [names[i] for i in co.numeric_positions(names, groups, prefixes=["REM_MSG_"])] == [
        "REM_MSG_10", "REM_MSG_2", "REM_MSG_3", "REM_MSG_11"]


def test_numeric_order_uses_the_active_settings():
    names = ["REM_MSG_10", "REM_MSG_2"]
    assert co.numeric_positions(names) == [0, 1]
    co.activate(co.from_dict({"numeric_order": ["REM_MSG_"]}))
    assert co.numeric_positions(names) == [1, 0]
    co.deactivate()
    assert co.numeric_positions(names) == [0, 1]


def test_receive_timeout_acts_as_the_dbc_cycle_time():
    messages = {"1": {"Msg_name": "TC_NSM", "DIR": "rx", "GenMsgCycleTime": "0"},
                "2": {"Msg_name": "TC_NSM_TX", "DIR": "tx", "GenMsgCycleTime": "0"},
                "3": {"Msg_name": "ESC2_10", "DIR": "rx", "GenMsgCycleTime": "10"}}
    co.apply_messages(messages)
    assert messages["1"]["GenMsgCycleTime"] == "0"                   # nothing active
    co.activate(co.from_dict({"rx": {"tc_nsm": {"timeout": 100}, "TC_NSM_TX": {"timeout": 5}}}))
    co.apply_messages(messages)
    assert [messages[k]["GenMsgCycleTime"] for k in "123"] == ["100", "0", "10"]
