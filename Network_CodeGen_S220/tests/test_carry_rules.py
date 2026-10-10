"""cogent_carry: receive-rule files from the new generation, derived values resolved from the merged
message list, and checks of the merged result (synthetic files shaped like the generated ones)."""
import sys

import pytest

from support import ROOT

sys.path.insert(0, str(ROOT))


def write(folder, name, text, eol="\r\n"):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(text.replace("\n", eol).encode("latin-1"))


def read(path):
    return path.read_bytes().decode("latin-1").replace("\r\n", "\n")


def enum(names):
    return "typedef enum\n{\n" + "".join("   VNIM_%s_MSGID,\n" % n for n in names) + "   NUM_VNIM_MESSAGES\n} VNIM_MSG_ID;\n"


def handles(names, width=None):
    """Handle defines; with width the name column is padded to width (at least one space)."""
    def column(n):
        name = "VNIM_%s_MESSAGE" % n
        return name.ljust(max(width, len(name) + 1)) if width else name + "     "
    return "".join("#define " + column(n) + str(i) + "\n" for i, n in enumerate(names))


def arrays(n, style_tail=""):
    pos = ",".join(str(i // 8) for i in range(n))
    mask = ",".join("0x%X" % (1 << (i % 8)) for i in range(n))
    return ("static unsigned8 vnim_msg_byte_position[NUM_VNIM_MESSAGES] = \n{\n    " + pos + style_tail + "\n};\n\n"
            "static unsigned8 vnim_msg_bit_mask[NUM_VNIM_MESSAGES] = \n{\n    " + mask + style_tail + "\n};\n")


def il_par(rx, flags, names, extra="", width=None, tail=""):
    return ("/* head */\n#define IL_RX_NUM_PERIODIC   %d\n#define IL_RX_NUM_MESSAGES   %d%s\n#define IL_RX_NUM_FRAMES     %d%s\n"
            "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   %s%s\n%s\n/* handles */\n%s/* end */\n"
            % (rx, rx, tail, rx, tail, flags, tail, extra, handles(names, width)))


@pytest.fixture
def scenario(tmp_path):
    """Previous generation A,B,D; your edit adds C (hand-written message) and a multiplex flag offset;
    the new generation adds AA (new DBC message)."""
    base, mine, new = tmp_path / "base", tmp_path / "ws" / "src", tmp_path / "new"
    write(base, "nw_vnim_app_signals_par.h", enum(["A", "B", "D"]))
    write(mine, "nw_vnim_app_signals_par.h", enum(["A", "B", "C", "D"]))
    write(new, "nw_vnim_app_signals_par.h", enum(["A", "AA", "B", "D"]))
    # handles: application messages in enum order, then Diag/NM handles (IS_DIAG_REQ, NM1) numbered after them
    write(base, "nw_il_par.h", il_par(3, "10", ["A", "B", "D", "IS_DIAG_REQ", "NM1"]))
    write(mine, "nw_il_par.h", il_par(4, "(9 + 3)", ["A", "B", "C", "D", "IS_DIAG_REQ", "NM1"],
                                      extra="#define IL_MUX_MSG_OFFSET_ID   9 ", width=24, tail=" "))
    write(new, "nw_il_par.h", il_par(4, "11", ["A", "AA", "B", "D", "IS_DIAG_REQ", "NM1"]))
    write(base, "nw_vnim_app_signals_par.c", "/* c */\n" + arrays(3))
    write(mine, "nw_vnim_app_signals_par.c", "/* c */\n" + arrays(4, "  "))
    write(new, "nw_vnim_app_signals_par.c", "/* c */\n" + arrays(4))
    return tmp_path


def run(scenario):
    import cogent_carry
    results = cogent_carry.carry_forward(scenario / "base", scenario / "ws", scenario / "new", scenario / "out")
    return {r["file"]: r for r in results}, scenario / "out"


def test_receive_counts_get_your_delta_and_the_safe_multiplex_offset(scenario):
    results, out = run(scenario)
    text = read(out / "nw_il_par.h")
    assert "#define IL_RX_NUM_PERIODIC   5\n" in text and "#define IL_RX_NUM_MESSAGES   5 \n" in text
    assert "#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   (11 + 3) \n" in text
    assert "#define IL_MUX_MSG_OFFSET_ID   11 \n" in text                   # first flag byte after the generated ones
    assert results["nw_il_par.h"]["conflicts"] == []


def test_handle_numbers_follow_the_merged_message_order(scenario):
    results, out = run(scenario)
    assert handles(["A", "AA", "B", "C", "D", "IS_DIAG_REQ", "NM1"], width=24) in read(out / "nw_il_par.h")
    assert any("handle" in r for r in results["nw_il_par.h"]["rules_applied"])


def test_per_message_arrays_have_one_entry_per_message(scenario):
    results, out = run(scenario)
    text = read(out / "nw_vnim_app_signals_par.c")
    assert "{\n    0,0,0,0,0\n};" in text and "{\n    0x1,0x2,0x4,0x8,0x10\n};" in text
    assert any("array" in r for r in results["nw_vnim_app_signals_par.c"]["rules_applied"])


def test_checks_pass_on_the_resolved_result(scenario):
    results, _ = run(scenario)
    assert all(r["checks"] == [] for r in results.values()), {f: r["checks"] for f, r in results.items()}


def test_receive_rule_files_come_from_the_new_generation(tmp_path):
    import cogent_carry
    write(tmp_path / "base", "nw_can_dll.h", "a\nb\nc\n")
    write(tmp_path / "ws", "nw_can_dll.h", "a\nB-mine\nc\n")
    write(tmp_path / "new", "nw_can_dll.h", "a\nb-new\nc\nd\n")
    res = {r["file"]: r for r in cogent_carry.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", tmp_path / "out")}
    assert read(tmp_path / "out" / "nw_can_dll.h") == "a\nb-new\nc\nd\n"
    assert res["nw_can_dll.h"]["status"] == "new generation taken" and "Receive FIFO" in res["nw_can_dll.h"]["detail"]


def test_duplicate_check_reports_definitions_the_merge_doubled():
    import cogent_carry
    merged = "#define X 1\nstatic int t[ ] =\n{ 1 };\nstatic int t[ ] =\n{ 1 };\n"
    once = "#define X 1\nstatic int t[ ] =\n{ 1 };\n"
    assert cogent_carry.duplicate_definitions(merged, once, once) == ["t defined 2 times (1 in the new generation, 1 in your file)"]
    assert cogent_carry.duplicate_definitions(once, once, once) == []


def test_table_check_reports_wrong_entry_counts():
    import cogent_carry
    header = enum(["A", "B"]) + "#define VNIM_NODE_LIST \\\n   NODE_A, \\\n   NODE_B, \\\n   NODE_C\n"
    assert cogent_carry.table_problems(header, "nw_vnim_app_signals_par.h", ["A", "B"]) == \
        ["VNIM_NODE_LIST has 3 entries for 2 messages"]


def test_missing_definition_check_reports_what_the_merge_dropped():
    import cogent_carry
    new = "#define A 1\n#define B 2\n#define C 3\n"
    base = "#define A 1\n#define B 2\n#define X 9\n"
    edited = "#define A 1\n#define B 2\n"                         # you removed X on purpose
    assert cogent_carry.missing_definitions("#define A 1\n", new, base, edited) == ["B", "C"]
    assert cogent_carry.missing_definitions(new, new, base, edited) == []


def test_check_reports_a_multiplex_flag_offset_that_overlaps_generated_flags():
    import cogent_carry
    text = ("#define IL_MUX_MSG_OFFSET_ID   161 \n"
            "#define ILSet_A_DataChanged() (il_Rx_DataChanged_Flag[160] |= 1)\n"
            "#define ILSet_B_DataChanged() (il_Rx_DataChanged_Flag[161] |= 2)\n")
    assert cogent_carry.table_problems(text, "nw_il_par.h", []) == [
        "IL_MUX_MSG_OFFSET_ID is 161, but the generated data-changed flags use bytes 0..161: the multiplexed "
        "signal flags share byte 161 with them (the first free byte is 162)"]
    assert cogent_carry.table_problems(text.replace("161 \n", "162 \n", 1), "nw_il_par.h", []) == []
