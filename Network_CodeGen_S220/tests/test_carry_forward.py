"""tools/carry_forward.py: re-applying hand edits of generated files to a new generation."""
import hashlib
import sys

import pytest

from support import ROOT

sys.path.insert(0, str(ROOT / "tools"))

GEN = ["/* header */", "Date                : 2026-01-01 10:00", "By                  : someone",
       "Traceability        : OLD.dbc", "int a = 1;", "int b = 2;", "int c = 3;", "int d = 4;", "int e = 5;",
       "int f = 6;", "int g = 7;", "int h = 8;", "/* end */"]


def write(folder, name, lines, eol="\r\n"):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(eol.join(lines).encode("latin-1") + eol.encode())


def lines_of(path):
    return path.read_bytes().decode("latin-1").replace("\r\n", "\n").rstrip("\n").split("\n")


def run(tmp_path, base, edited, new, name="nw_il_par.c", out="out"):
    import carry_forward
    write(tmp_path / "base", name, base)
    write(tmp_path / "ws" / "app" / "src", name, edited)
    write(tmp_path / "new", name, new)
    results = carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", tmp_path / out)
    return next(r for r in results if r["file"] == name), tmp_path / out / name


def replaced(lines, index, value):
    out = list(lines)
    out[index] = value
    return out


def test_edit_and_generator_change_in_different_places_are_both_kept(tmp_path):
    edited = replaced(GEN, 5, "int b = 20;   /* hand edit */")
    new = replaced(GEN, 10, "int g = 70;")
    res, out = run(tmp_path, GEN, edited, new)
    assert res["status"] == "merged" and res["conflicts"] == [] and res["edits"] == 1
    assert lines_of(out) == replaced(edited, 10, "int g = 70;")


def test_same_lines_changed_by_both_is_a_conflict_with_location_and_all_versions(tmp_path):
    import carry_forward
    res, out = run(tmp_path, GEN, replaced(GEN, 6, "int c = 30;"), replaced(GEN, 6, "int c = 300;"))
    assert res["status"] == "CONFLICTS"
    (line, new, base, edited), = res["conflicts"]
    assert (new, base, edited) == (["int c = 300;"], ["int c = 3;"], ["int c = 30;"])
    text = lines_of(out)
    assert text[line - 1].startswith("<<<<<<< new generation") and ">>>>>>> your edit" in text
    report = carry_forward.report([res], "base", "ws", "new", "out")
    for heading in ("File and location", "Current value (new generation)", "Your edit", "Required change",
                    "Why not automatic", "Dependencies", "Steps", "Verification"):
        assert "**%s" % heading in report
    assert "line %d" % line in report


def test_white_space_only_conflict_keeps_your_formatting(tmp_path):
    res, out = run(tmp_path, GEN, replaced(GEN, 6, "int   c   = 30;"), replaced(GEN, 6, "int c = 30;"))
    assert res["conflicts"] == [] and res["auto"] == {"white space": 1}
    assert lines_of(out)[6] == "int   c   = 30;"


def test_header_stamp_conflict_keeps_the_new_stamp_and_flags_other_generation(tmp_path):
    edited = replaced(replaced(GEN, 1, "Date                : 2024-10-17 17:05"), 3, "Traceability        : OLDER.dbc")
    new = replaced(replaced(GEN, 1, "Date                : 2026-10-09 09:00"), 3, "Traceability        : NEW.dbc")
    res, out = run(tmp_path, GEN, edited, new)
    assert res["conflicts"] == [] and res["auto"] == {"header stamp": 2}   # Date and Traceability (By unchanged)
    assert lines_of(out)[1:4] == new[1:4]
    assert res["origin"] == ("OLDER.dbc", "OLD.dbc")


def test_file_missing_in_workspace_takes_the_new_file_and_is_reported(tmp_path):
    import carry_forward
    write(tmp_path / "base", "nw_il_msg.h", GEN)
    write(tmp_path / "new", "nw_il_msg.h", GEN)
    (tmp_path / "ws").mkdir()
    results = carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", tmp_path / "out")
    res = next(r for r in results if r["file"] == "nw_il_msg.h")
    assert res["status"] == "new file taken" and "not found" in res["detail"]
    assert "Manual Action Required" in carry_forward.report(results, "b", "w", "n", "o")


def test_new_line_style_of_the_new_file_is_kept(tmp_path):
    import carry_forward
    write(tmp_path / "base", "nw_il_par.h", GEN, eol="\n")
    write(tmp_path / "ws", "nw_il_par.h", replaced(GEN, 5, "int b = 20;"), eol="\n")
    write(tmp_path / "new", "nw_il_par.h", GEN, eol="\r\n")
    carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", tmp_path / "out")
    data = (tmp_path / "out" / "nw_il_par.h").read_bytes()
    assert b"int b = 20;\r\n" in data and b"\n" not in data.replace(b"\r\n", b"")


def test_inputs_are_never_written_and_unsafe_outputs_are_refused(tmp_path):
    import carry_forward
    res, _ = run(tmp_path, GEN, replaced(GEN, 5, "int b = 20;"), replaced(GEN, 9, "int f = 60;"))
    digest = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob("*") if p.is_file()
              and "out" not in p.parts}
    for out in (tmp_path / "ws" / "merged", tmp_path / "new", tmp_path / "out"):   # inside input / an input / not empty
        with pytest.raises(carry_forward.UsageError):
            carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", out)
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in digest} == digest
    assert not (tmp_path / "ws" / "merged").exists()


def test_carrying_forward_is_repeatable_and_idempotent(tmp_path):
    import carry_forward
    res, first = run(tmp_path, GEN, replaced(GEN, 5, "int b = 20;"), replaced(GEN, 9, "int f = 60;"))
    carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "new", tmp_path / "out2")
    assert (tmp_path / "out2" / "nw_il_par.c").read_bytes() == first.read_bytes()
    # merging again onto a result that already contains the edits changes nothing
    carry_forward.carry_forward(tmp_path / "base", tmp_path / "ws", tmp_path / "out", tmp_path / "out3")
    assert (tmp_path / "out3" / "nw_il_par.c").read_bytes() == first.read_bytes()


def test_command_line_exit_codes_and_report(tmp_path):
    import carry_forward
    write(tmp_path / "base", "nw_il_par.c", GEN)
    write(tmp_path / "ws", "nw_il_par.c", replaced(GEN, 5, "int b = 20;"))
    write(tmp_path / "new", "nw_il_par.c", replaced(GEN, 9, "int f = 60;"))
    args = ["--base", str(tmp_path / "base"), "--edited", str(tmp_path / "ws"), "--new", str(tmp_path / "new")]
    # the other generated files are missing from --new: reported as skipped, so the exit code asks for attention
    assert carry_forward.main(args + ["--out", str(tmp_path / "o1")]) == 1
    assert "| nw_il_par.c | merged | 1 | 0 |" in (tmp_path / "o1" / "CARRY_FORWARD.md").read_text(encoding="utf-8")
    assert carry_forward.main(args + ["--out", str(tmp_path / "ws" / "x")]) == 2
