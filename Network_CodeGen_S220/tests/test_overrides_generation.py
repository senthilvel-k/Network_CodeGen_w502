"""40024 fixture generated with the Code overrides of the S2XX workspace (S2XX_OVERRIDES) and without."""
import json
import os
import re
import shutil
import sys

import pytest

from support import CODE_FILES, ROOT, S2XX_OVERRIDES, load_fixture, run_file

sys.path.insert(0, str(ROOT))
FIXTURE = "s2xx_40024_a"
FIFO = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}]}
REM = ["REM_MSG_%d" % i for i in range(16)]


def _generate(home, overrides):
    from cogent_generate import run_code_generation
    fx = load_fixture(FIXTURE)
    shutil.copytree(fx.data_dir, home / "data")
    (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps(FIFO), encoding="utf-8")
    if overrides is not None:
        (home / "data" / "CanOverrideConfiguration.data").write_text(json.dumps(overrides), encoding="utf-8")
    run_code_generation(str(fx.dbc), fx.node, "2000-01-01 00:00")
    return {f: run_file(home, f).read_text(encoding="latin-1") for f in CODE_FILES}


def _in_home(home, func, *args):
    old = os.getcwd()
    os.chdir(home)
    try:
        return func(*args)
    finally:
        os.chdir(old)


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    """'plain': no settings file; 'empty': an empty settings object; 'over': the S2XX overrides."""
    out = {}
    for key, overrides in (("plain", None), ("empty", {}), ("over", S2XX_OVERRIDES)):
        home = tmp_path_factory.mktemp("over_%s" % key)
        out[key] = _in_home(home, _generate, home, overrides)
    return out


def _function(text, head):
    start = text.index(head)
    return text[start:text.index("\n}\n", start)]


def _section(text, start, end):
    begin = text.index(start)
    return text[begin:text.index(end, begin)]


def rx_handles(h):
    return {k: int(v) for k, v in re.findall(r"^#define VNIM_(\w+)_MESSAGE\s+(\d+)\s*$", h, re.M)}


def rx_frame_order(h):
    return re.findall(r"/\* (\w+)Message \*/", _section(h, "#define IL_RX_FRAME_TABLE", "Received Message (Frame) Callback"))


def rx_frame_entry(h, name):
    table = _section(h, "#define IL_RX_FRAME_TABLE", "Received Message (Frame) Callback")
    start = table.index("/* %sMessage */" % name)
    return table[start:table.index("PreCopy", start)]


def test_an_empty_settings_object_changes_nothing(runs):
    for name in CODE_FILES:
        assert runs["empty"][name] == runs["plain"][name], name


# ---------------------------------------------------------------- rx timeout (TC_NSM)

def test_receive_timeout_is_the_cycle_time_of_the_message(runs):
    assert "IL_TIME_IN_TASK_TICS( 0*MSG_TIMEOUT_ERROR_COUNT )" in rx_frame_entry(runs["plain"]["nw_il_par.h"], "TC_NSM")
    assert "IL_TIME_IN_TASK_TICS( 100*MSG_TIMEOUT_ERROR_COUNT )" in rx_frame_entry(runs["over"]["nw_il_par.h"], "TC_NSM")


def test_receive_timeout_adds_the_gain_and_loss_cases(runs):
    for key, present in (("plain", False), ("over", True)):
        v = runs[key]["nw_vnim_app_signals_par.c"]
        gain = _function(v, "static void vnim_message_gain(unsigned8 msg_id)")
        loss = _function(v, "static void vnim_message_loss(unsigned8 msg_id)")
        assert ("case VNIM_TC_NSM_MSGID:" in gain) is present, key
        assert ("case VNIM_TC_NSM_MSGID:" in loss) is present, key
    gain = _function(runs["over"]["nw_vnim_app_signals_par.c"], "static void vnim_message_gain(unsigned8 msg_id)")
    case = gain[gain.index("case VNIM_TC_NSM_MSGID:"):]
    assert "vnim_dtc_unlog(NM_TC_NODE,VNIM_MSG_GAIN,VNIM_TC_NSM_MSGID);" in case[:case.index("break;")]


# ---------------------------------------------------------------- numeric order (REM_MSG_0..15)

def test_receive_handles_in_numeric_order(runs):
    plain, over = rx_handles(runs["plain"]["nw_il_par.h"]), rx_handles(runs["over"]["nw_il_par.h"])
    assert [plain[m] for m in REM] != sorted(plain[m] for m in REM)               # string order before
    assert [over[m] for m in REM] == sorted(plain[m] for m in REM)                # same numbers, numeric order
    assert {k: v for k, v in over.items() if k not in REM} == {k: v for k, v in plain.items() if k not in REM}


def test_receive_frame_table_follows_the_handles(runs):
    h = runs["over"]["nw_il_par.h"]
    order, handles = rx_frame_order(h), rx_handles(h)
    assert [m for m in order if m.startswith("REM_MSG_")] == REM
    assert all(handles[m] == i for i, m in enumerate(order))                      # entry k has handle k


def test_other_lists_keep_the_string_order(runs):
    for name in ("nw_il_msg.h", "nw_il_par.c"):
        text = runs["over"][name]
        assert text.index("REM_MSG_10") < text.index("REM_MSG_2"), name
    v = runs["over"]["nw_vnim_app_signals_par.c"]
    assert v.index("void VnimIlRx_REM_MSG_10_MsgIndication( void )") < v.index("void VnimIlRx_REM_MSG_2_MsgIndication( void )")


def test_vnim_message_ids_in_numeric_order(runs):
    def enum(text):
        return _section(text, "/*VNIM Message ENUM*/", "NUM_VNIM_MESSAGES").splitlines()
    plain, over = enum(runs["plain"]["nw_vnim_app_signals_par.h"]), enum(runs["over"]["nw_vnim_app_signals_par.h"])
    rem = [l for l in over if "VNIM_REM_MSG_" in l]
    assert [re.search(r"VNIM_(REM_MSG_\d+)_MSGID", l).group(1) for l in rem] == REM
    assert "VNIM_REM_MSG_9_MSGID,/*FCM msg stop index*/" in rem[9]                # the line moves with its comment
    assert sorted(over) == sorted(plain)
    assert [l for l in over if "VNIM_REM_MSG_" not in l] == [l for l in plain if "VNIM_REM_MSG_" not in l]


# ---------------------------------------------------------------- errors

@pytest.mark.parametrize("overrides, words", [
    ({"tx": {"NO_SUCH_MSG": {"attribute": "Event"}}}, ["NO_SUCH_MSG", "not a transmit message"]),
    ({"rx": {"IC10_200": {"timeout": 10}}}, ["IC10_200", "not a receive message"]),
    ({"tx": {"IC10_200": {"attribute": "Sometimes"}}}, ["IC10_200", "attribute"]),
])
def test_invalid_overrides_stop_the_generation(tmp_path, overrides, words):
    from cogent_errors import CogentError
    with pytest.raises(CogentError) as err:
        _in_home(tmp_path, _generate, tmp_path, overrides)
    text = str(err.value) + " " + (err.value.hint or "")
    for word in words + ["CanOverrideConfiguration.data", "Code overrides"]:
        assert word in text, (word, text)
    assert not (tmp_path / "CODE_GEN").exists() or not [p for p in (tmp_path / "CODE_GEN").iterdir()
                                                        if p.name[0].isdigit()]


# ---------------------------------------------------------------- tx attribute, period / offset, confirmation

EVENT = "   (IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\"
PERIODIC = "   (IL_TX_ATTR_PERIODIC),         /* Frame Transmission Attributes              */   \\"
PERIODIC_EVENT = "   (IL_TX_ATTR_PERIODIC|IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\"
NOTIFY = "   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\"
NULL_PERIODIC = "   NULL,                                                            /* Pointer to the Periodic Attributes (or NULL) */  \\"
ZERO_PERIOD = "   IL_TIME_IN_TASK_TICS( 0 ),                /* Primary Period in Task Tics  */     \\"
ZERO_OFFSET = "   IL_TIME_IN_TASK_TICS( 0 ),                /* Offset Delay in Task Tics    */    \\"


def tx_frame_entries(h):
    table = _section(h, "#define IL_TX_FRAME_TABLE", "Interaction Layer Periodic Transmit Table")
    return dict(re.findall(r"/\*(\w+) Message \*/\\\n(.*?)\n   }", table, re.S))


def tx_periodic_rows(h):
    table = _section(h, "#define IL_TX_PERIODIC_TABLE", "Transmit Message (Frame) Callback Functions")
    return dict(re.findall(r"/\* (\w+)Message is Periodic \*/.*?\n(.*?)\n   &il_tx_periodic_count", table, re.S))


def test_tx_attribute_event_without_periodic_row(runs):
    over = tx_frame_entries(runs["over"]["nw_il_par.h"])
    rows, plain_rows = tx_periodic_rows(runs["over"]["nw_il_par.h"]), tx_periodic_rows(runs["plain"]["nw_il_par.h"])
    for name in ["EX_SUMMARY_RESPONSE_%d" % i for i in range(4)] + ["MCM_SP", "MCM_WAKEUP"]:
        lines = over[name].splitlines()
        assert EVENT in lines and NULL_PERIODIC in lines and PERIODIC not in lines, name
    for name in ["EX_SUMMARY_RESPONSE_%d" % i for i in range(4)] + ["MCM_SP"]:
        assert rows[name].splitlines()[1:] == [ZERO_PERIOD, ZERO_OFFSET], name
    assert "IL_TIME_IN_TASK_TICS( 150)" in plain_rows["EX_SUMMARY_RESPONSE_0"]
    assert rows["MCM_WAKEUP"] == plain_rows["MCM_WAKEUP"] and "IL_TIME_IN_TASK_TICS( 20 )" in rows["MCM_WAKEUP"]


def test_tx_attribute_periodic_and_event(runs):
    over, plain = tx_frame_entries(runs["over"]["nw_il_par.h"]), tx_frame_entries(runs["plain"]["nw_il_par.h"])
    assert PERIODIC_EVENT in over["REM_ACK_MSG"].splitlines()
    assert over["REM_ACK_MSG"].replace(PERIODIC_EVENT, PERIODIC) == plain["REM_ACK_MSG"]


def test_tx_confirmation_callbacks(runs):
    h = runs["over"]["nw_il_par.h"]
    over, plain = tx_frame_entries(h), tx_frame_entries(runs["plain"]["nw_il_par.h"])
    for name in ("IC10_200", "IC11_500", "MCM4_1000"):
        lines = over[name].splitlines()
        assert NOTIFY in lines, name
        assert "   &Vnim_%s_Conf,                        \t\t\t                                   " \
               "/* Pointer to Tx confirmation function               */\t\\" % name in lines
        assert "   &Vnim_%s_PreCopy                        \t\t\t                                   " \
               "/* Pointer to Tx Precopy function               */\t\\" % name in lines
        assert "NULL,                        \t\t\t" in plain[name]
        assert "extern void Vnim_%s_PreCopy(void);\nextern void Vnim_%s_Conf(void);" % (name, name) in h
    assert "Vnim_IC10_200_Conf" not in runs["plain"]["nw_il_par.h"]


def test_other_tx_messages_unchanged(runs):
    changed = {"EX_SUMMARY_RESPONSE_%d" % i for i in range(4)} | {"MCM_SP", "MCM_WAKEUP", "REM_ACK_MSG",
                                                                   "IC10_200", "IC11_500", "MCM4_1000"}
    for table in (tx_frame_entries, tx_periodic_rows):
        over, plain = table(runs["over"]["nw_il_par.h"]), table(runs["plain"]["nw_il_par.h"])
        assert set(over) == set(plain) and len(plain) == 48                   # enabled Tx messages
        assert {k: v for k, v in over.items() if k not in changed} == {k: v for k, v in plain.items() if k not in changed}


def test_tx_override_of_a_disabled_message_is_ignored(tmp_path, runs):
    """TGU1_100 is a transmit message of the DBC whose Tx is not enabled in the fixture."""
    out = _in_home(tmp_path, _generate, tmp_path, {"tx": {"TGU1_100": {"attribute": "Event", "confirmation": True}}})
    assert out["nw_il_par.h"] == runs["plain"]["nw_il_par.h"]


# ---------------------------------------------------------------- NM transmit table (nw_nm_par.h)

NM_HEAD = [
    '#define NM_TX_MSG_DATA_STRUCT                            \t\t\t\t\t\t\t\t\\',
    '{                                                                                  \t\t\\',
    '\t/* MCM_WAKEUP_REASON */\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t{\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t   CAN_GPNUM_8,                                 /* CAN message data length  */     \t\\',
    '\t   0x9A,                                       \t/* CAN message identifier   */     \t\\',
    '\t   &Nm_wakeup_buffer[0],                        /* Pointer to Data          */      \\',
    '\t   CANB_TX_STD_DATA,                            /* CAN message options      */      \\',
    '\t   (DLL_NUM_IL_TX_FRAMES+1)                     /* Transmit Message Handle  */      \\',
    '\t},\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t/* IC_ACTIVE */\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t{\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t   CAN_GPNUM_8,                                 /* CAN message data length  */     \t\\',
    '\t   0x234,                                       /* CAN message identifier   */     \t\\',
    '\t   &Nm_msg_buffer[0],                           /* Pointer to Data          */      \\',
    '\t   CANB_TX_STD_DATA,                            /* CAN message options      */      \\',
    '\t   (DLL_NUM_IL_TX_FRAMES+2)                     /* Transmit Message Handle  */      \\',
    '\t},\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
    '\t/* MCM_ACTIVE */\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\',
]


def nm_table(text):
    lines = text.replace("\r", "").split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("#define NM_TX_MSG_DATA_STRUCT"))
    end = lines.index("}", start)
    return lines[start:end + 1]


def test_nm_transmit_table(runs):
    table = nm_table(runs["over"]["nw_nm_par.h"])
    assert table[:len(NM_HEAD)] == NM_HEAD                                  # the S2XX layout, tabs included
    assert table[-2:] == ['\t}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\\', '}']
    assert re.findall(r"/\* (\w+) \*/\t", "\n".join(table)) == [
        "MCM_WAKEUP_REASON", "IC_ACTIVE", "MCM_ACTIVE", "IS_ACTIVE", "MCM_SLEEP"]
    assert re.findall(r"\t   (0x[0-9A-F]+),", "\n".join(table)) == ["0x9A", "0x234", "0x3BD", "0x3C5", "0x3BB"]
    assert re.findall(r"\(DLL_NUM_IL_TX_FRAMES\+(\d)\)", "\n".join(table)) == ["1", "2", "3", "4", "5"]
    assert len(table) == 2 + 5 * 8 + 1


def test_nm_transmit_table_without_override(runs):
    table = nm_table(runs["plain"]["nw_nm_par.h"])
    assert len(table) == 8 and "0x234," in table[3]
    rest = lambda t: t[t.index("typedef enum"):]                            # noqa: E731
    assert rest(runs["over"]["nw_nm_par.h"]) == rest(runs["plain"]["nw_nm_par.h"])


# ---------------------------------------------------------------- host forwarding (REM)

REM_HEAD = ["", "/* ===========================================================================",
            "          R E M    M A C R O S",
            "  =========================================================================*/", ""]


def test_rem_macros_after_the_dlc_fault_defines(runs):
    v = runs["over"]["nw_vnim_app_signals_par.c"]
    lines = v.replace("\r", "").split("\n")
    i = lines.index("          R E M    M A C R O S") - 2
    assert lines[i - 1].startswith("#define IS_WLC_DLC_FAULT(msg_id)")
    assert lines[i:i + 5] == REM_HEAD
    assert lines[i + 5:i + 21] == ["#define VNIM_REM_MSG_%-2d %d" % (n, n) for n in range(16)]
    assert lines[i + 21] == "" and lines[i + 22].startswith("/* ====") and "M E M O R Y" in lines[i + 23]
    assert "R E M    M A C R O S" not in runs["plain"]["nw_vnim_app_signals_par.c"]


def test_forwarded_indications_call_the_host_function(runs):
    over, plain = runs["over"]["nw_vnim_app_signals_par.c"], runs["plain"]["nw_vnim_app_signals_par.c"]
    for name in REM:
        ind = _function(over, "void VnimIlRx_%s_MsgIndication( void )" % name)
        assert "              host_update_msg(VNIM_%s);\n" % name in ind
        assert "VNRCL_%s_MSGID" % name not in ind
        before = _function(plain, "void VnimIlRx_%s_MsgIndication( void )" % name)
        assert ind == before.replace("              #if (vnim_notify_used(VNRCL_%s_MSGID) == YES)\n"
                                     "                os_notify(VNRCL_%s_MSGID,0, NULL );\n"
                                     "              #endif" % (name, name),
                                     "              host_update_msg(VNIM_%s);" % name)
    assert "host_update_msg" not in _function(over, "void VnimIlRx_REM_MSG_0_Timeout( void )")
