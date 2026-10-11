"""Configuration archives (.cfg): they hold the configuration, never the pages of the app itself."""
import sys
import zipfile

from support import ROOT

sys.path.insert(0, str(ROOT))
import cogent_generate  # noqa: E402


def _folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for folder in ("html", "data", "js"):
        (tmp_path / folder).mkdir()
    for name in ("CAN_DBC_msg.html", "_sidebar.html", "Tool_Index_Page.html", "Overrides.html", "Fifo.html"):
        (tmp_path / "html" / name).write_text("current " + name, encoding="utf-8")
    (tmp_path / "data" / "dbc_details.data").write_text("{}", encoding="utf-8")
    (tmp_path / "js" / "CanDbcMsgConfiguration.js").write_text("js", encoding="utf-8")


def test_archive_holds_the_configuration_not_the_app_pages(tmp_path, monkeypatch):
    _folder(tmp_path, monkeypatch)
    cogent_generate.write_config_archive("a.cfg")
    names = set(zipfile.ZipFile("a.cfg").namelist())
    assert {"html/CAN_DBC_msg.html", "data/dbc_details.data", "js/CanDbcMsgConfiguration.js"} <= names
    assert not names & {"html/" + n for n in cogent_generate.APP_PAGES}


def test_loading_an_archive_keeps_the_app_pages(tmp_path, monkeypatch):
    """Archives of earlier versions contain the app pages of that version (e.g. the legacy home page)."""
    _folder(tmp_path, monkeypatch)
    with zipfile.ZipFile("old.cfg", "w") as z:
        for name in ("html/_sidebar.html", "html/Tool_Index_Page.html", "html/CAN_DBC_msg.html", "data/dbc_details.data"):
            z.writestr(name, "archived " + name)
    extracted = cogent_generate.extract_config_archive("old.cfg")
    assert sorted(extracted) == ["data/dbc_details.data", "html/CAN_DBC_msg.html"]
    assert (tmp_path / "html" / "_sidebar.html").read_text(encoding="utf-8") == "current _sidebar.html"
    assert (tmp_path / "html" / "Tool_Index_Page.html").read_text(encoding="utf-8") == "current Tool_Index_Page.html"
    assert (tmp_path / "html" / "CAN_DBC_msg.html").read_text(encoding="utf-8") == "archived html/CAN_DBC_msg.html"
