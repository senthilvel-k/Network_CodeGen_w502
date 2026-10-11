"""Re-apply edits page: folders, run, results and Manual Action Required list, safety, keep a copy of
CODE_GEN. Synthetic generated files; tests share one app and run in file order."""
import json

import pytest

from gui_support import js, navigate, settle, start_app_copy, wait_alert

pytestmark = pytest.mark.gui
FIXTURE = "s237_36144_2"
GEN = ["/* header */", "Date                : 2026-01-01 10:00", "int a = 1;", "int b = 2;", "int c = 3;",
       "int d = 4;", "int e = 5;", "int f = 6;", "int g = 7;", "int h = 8;", "/* end */"]
RUN = "document.getElementById('reapply-run').click()"


def write(folder, name, lines):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes("\r\n".join(lines).encode("latin-1") + b"\r\n")


def replaced(lines, index, value):
    out = list(lines)
    out[index] = value
    return out


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    back_end, home, fx, dbc, restore = start_app_copy(tmp_path_factory, FIXTURE)
    root = tmp_path_factory.mktemp("reapply folders")
    write(root / "previous gen", "nw_il_par.c", GEN)
    write(root / "my workspace" / "src", "nw_il_par.c", replaced(GEN, 3, "int b = 20;   /* mine */"))
    write(root / "new gen", "nw_il_par.c", replaced(GEN, 8, "int g = 70;"))
    yield back_end, home, root
    restore()


def fill(qtbot, gui, base, edited, new, out):
    js(qtbot, gui, "document.getElementById('reapply-base').value=%s; document.getElementById('reapply-edited').value=%s;"
                   "document.getElementById('reapply-new').value=%s; document.getElementById('reapply-out').value=%s; 1"
       % tuple(json.dumps(str(p)) for p in (base, edited, new, out)))


def test_page_opens_from_the_sidebar_with_defaults(qtbot, app):
    back_end, home, root = app
    gui = back_end.app
    navigate(qtbot, gui, "BackEnd.default_page()")
    navigate(qtbot, gui, "document.querySelector('a[href=\"BackEnd.reapply_page\"]').click()")
    assert gui.template[0] == "Reapply.html"
    assert js(qtbot, gui, "document.getElementById('reapply-new').value").endswith("CODE_GEN")
    assert "MERGED" in js(qtbot, gui, "document.getElementById('reapply-out').value")


def test_run_shows_results_and_writes_the_report(qtbot, app):
    back_end, home, root = app
    gui = back_end.app
    fill(qtbot, gui, root / "previous gen", root / "my workspace", root / "new gen", root / "result 1")
    navigate(qtbot, gui, RUN)
    rows = js(qtbot, gui, "document.getElementById('reapply-results').innerText")
    assert "nw_il_par.c" in rows and "merged" in rows
    merged = (root / "result 1" / "nw_il_par.c").read_text(encoding="latin-1")
    assert "int b = 20;   /* mine */" in merged and "int g = 70;" in merged
    assert (root / "result 1" / "CARRY_FORWARD.md").exists()
    saved = json.loads((home / "data" / "ReapplyEdits.data").read_text(encoding="utf-8"))
    assert saved["base"] == str(root / "previous gen")


def test_conflicts_are_listed_with_file_and_line(qtbot, app):
    back_end, home, root = app
    gui = back_end.app
    write(root / "new gen 2", "nw_il_par.c", replaced(GEN, 3, "int b = 200;"))
    fill(qtbot, gui, root / "previous gen", root / "my workspace", root / "new gen 2", root / "result 2")
    navigate(qtbot, gui, RUN)
    attention = js(qtbot, gui, "document.getElementById('reapply-attention').innerText")
    assert "nw_il_par.c line 4" in attention and "changed lines you edited" in attention


def test_output_inside_the_workspace_is_refused(qtbot, app):
    back_end, home, root = app
    gui = back_end.app
    before = (root / "my workspace" / "src" / "nw_il_par.c").read_bytes()
    fill(qtbot, gui, root / "previous gen", root / "my workspace", root / "new gen", root / "my workspace" / "out")
    navigate(qtbot, gui, RUN)
    error = js(qtbot, gui, "document.getElementById('reapply-error').innerText")
    assert "inside the workspace folder" in error
    assert not (root / "my workspace" / "out").exists()
    assert (root / "my workspace" / "src" / "nw_il_par.c").read_bytes() == before


def test_open_result_folder(qtbot, app, monkeypatch):
    back_end, home, root = app
    gui = back_end.app
    opened = []
    monkeypatch.setattr(back_end.os, "startfile", opened.append, raising=False)
    fill(qtbot, gui, root / "previous gen", root / "my workspace", root / "new gen", root / "result 3")
    navigate(qtbot, gui, RUN)
    js(qtbot, gui, "document.getElementById('reapply-open').click(); 1")
    qtbot.waitUntil(lambda: opened == [str(root / "result 3")], timeout=10000)


def test_keep_a_copy_of_code_gen(qtbot, app):
    back_end, home, root = app
    gui = back_end.app
    (home / "CODE_GEN").mkdir(exist_ok=True)
    for name in back_end.cogent_generate.GENERATED_FILES:
        (home / "CODE_GEN" / name).write_text("generated " + name, encoding="utf-8")
    gui.alerts.clear()
    js(qtbot, gui, "document.getElementById('keep-copy').click(); 1")
    text = wait_alert(qtbot, gui, "Copy of CODE_GEN saved")
    copies = [p for p in (home / "CODE_GEN").iterdir() if p.is_dir()]
    assert len(copies) == 1 and copies[0].name in text
    assert sorted(p.name for p in copies[0].iterdir()) == sorted(back_end.cogent_generate.GENERATED_FILES)
    settle(qtbot, gui)
