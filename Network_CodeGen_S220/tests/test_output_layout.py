"""Each code generation goes to its own folder CODE_GEN/<date_time>/: the configuration archive of the run,
the reports and the generated files in the folders of the S2XX repository. Earlier runs stay untouched."""
import json
import shutil
import sys
import zipfile

import pytest

from support import CODE_FILES, ROOT, load_fixture

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024_a"
TIME = "2000-01-01 00:00"
REFERENCE_CONFIG = {"merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
                    "additional_rx_messages": ["BMS19_100", "BMS20_100"]}
EXPECTED_PATHS = {
    "can_rxrule.cfg": "app.nos.arch3/src/can_rxrule.cfg",
    "nw_can_dll.h": "app.nos.arch3/src/nw_can_dll.h",
    "nw_il_msg.h": "app.nos.arch3/src/nw_il_msg.h",
    "nw_il_par.h": "app.nos.arch3/src/nw_il_par.h",
    "nw_il_par.c": "app.nos.arch3/src/nw_il_par.c",
    "nw_nm_par.h": "app.nos.arch3/src/nw_nm_par.h",
    "nw_vnim_app_signals_par.c": "app.vnim.arch3/src/nw_vnim_app_signals_par.c",
    "nw_vnim_app_signals_par.h": "app.vnim.arch3/nw_vnim_app_signals_par.h",
    "vnim.msg.resource": "app.vnim.arch3/vnim.msg.resource",
    "vnim.txrx.resource": "app.vnim.arch3/vnim.txrx.resource",
    "nw_host_mgr_txrx.resource": "app.host.manager/nw_host_mgr_txrx.resource",
}


@pytest.fixture
def home(tmp_path, monkeypatch):
    h = tmp_path / "CoGeNT home"
    shutil.copytree(load_fixture(FIXTURE).data_dir, h / "data")
    (h / "data" / "CanFifoConfiguration.data").write_text(json.dumps(REFERENCE_CONFIG), encoding="utf-8")
    for sub in ("html", "js"):
        (h / sub).mkdir()
        (h / sub / ("page." + sub)).write_text(sub + " page", encoding="utf-8")
    monkeypatch.chdir(h)
    monkeypatch.setenv("LOGNAME", "cogent-test")
    return h


def _generate(monkeypatch=None, stamp=None):
    import cogent_generate
    if stamp:
        monkeypatch.setattr(cogent_generate, "_run_stamp", lambda: stamp)
    return cogent_generate.run_code_generation(str(load_fixture(FIXTURE).dbc), "SMART_CORE", TIME)


def _files(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


def test_layout_covers_every_generated_file():
    import cogent_generate
    assert {f: cogent_generate.output_relpath(f).replace("\\", "/") for f in CODE_FILES} == EXPECTED_PATHS


def test_a_run_writes_its_own_date_time_folder(home, monkeypatch):
    result = _generate(monkeypatch, "11-10-2026_10-15-30")
    run = home / "CODE_GEN" / "11-10-2026_10-15-30"
    assert result.folder == str(run)
    assert sorted(_files(run)) == sorted(list(EXPECTED_PATHS.values()) +
                                         ["11-10-2026_10-15-30.cfg", "MANUAL_ACTIONS.md", "fifo_plan.json"])
    assert sorted(p.replace("\\", "/") for p in result.paths) == sorted(EXPECTED_PATHS.values())
    assert [p.name for p in (home / "CODE_GEN").iterdir()] == ["11-10-2026_10-15-30"]    # nothing else, no staging


def test_the_configuration_archive_of_the_run(home, monkeypatch):
    result = _generate(monkeypatch, "11-10-2026_10-15-30")
    with zipfile.ZipFile(home / "CODE_GEN" / "11-10-2026_10-15-30" / result.config_archive) as z:
        names = set(z.namelist())
        assert {"data/CanDbcMsgConfiguration.data", "data/CanDbcSigConfiguration.data", "data/CanFifoConfiguration.data",
                "data/dbc_details.data", "html/page.html", "js/page.js"} <= names
        assert z.read("data/CanFifoConfiguration.data") == (home / "data" / "CanFifoConfiguration.data").read_bytes()


def test_earlier_runs_and_your_files_stay_untouched(home, monkeypatch):
    code_gen = home / "CODE_GEN"
    (code_gen / "DBC_40024").mkdir(parents=True)
    (code_gen / "DBC_40024" / "can_rxrule.cfg").write_text("kept copy", encoding="utf-8")
    (code_gen / "can_rxrule.cfg").write_text("flat output of an older CoGeNT", encoding="utf-8")
    _generate(monkeypatch, "11-10-2026_10-15-30")
    first = _files(code_gen / "11-10-2026_10-15-30")
    _generate(monkeypatch, "11-10-2026_10-20-00")
    assert _files(code_gen / "11-10-2026_10-15-30") == first
    assert (code_gen / "11-10-2026_10-20-00" / "app.nos.arch3" / "src" / "can_rxrule.cfg").is_file()
    assert (code_gen / "DBC_40024" / "can_rxrule.cfg").read_text(encoding="utf-8") == "kept copy"
    assert (code_gen / "can_rxrule.cfg").read_text(encoding="utf-8") == "flat output of an older CoGeNT"


def test_two_runs_in_the_same_second_get_different_folders(home, monkeypatch):
    first = _generate(monkeypatch, "11-10-2026_10-15-30")
    second = _generate(monkeypatch, "11-10-2026_10-15-30")
    assert first.folder != second.folder and second.folder.endswith("11-10-2026_10-15-30_2")
    assert (home / "CODE_GEN" / "11-10-2026_10-15-30_2" / "11-10-2026_10-15-30_2.cfg").is_file()


def test_a_failed_run_creates_no_folder(home, monkeypatch):
    from cogent_errors import CogentError
    _generate(monkeypatch, "11-10-2026_10-15-30")
    before = _files(home / "CODE_GEN")
    (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps({"max_rx_rules": 100}), encoding="utf-8")
    with pytest.raises(CogentError):
        _generate(monkeypatch, "11-10-2026_10-20-00")
    after = {k: v for k, v in _files(home / "CODE_GEN").items() if k != "errorlog.txt"}
    assert after == before


def test_code_gen_that_is_not_a_folder_is_explained(home):
    from cogent_errors import CogentError
    (home / "CODE_GEN").write_text("a file where the CODE_GEN folder should be", encoding="utf-8")
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "CODE_GEN" in text and "folder" in text and "Traceback" not in text
