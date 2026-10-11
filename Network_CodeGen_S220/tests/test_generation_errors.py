"""Code generation pipeline used by the GUI: staging, error explanations, logging."""
import json
import shutil
import sys

import pytest

from support import (CODE_FILES, LEGACY_REFS, ROOT, load_fixture, normalize_date_by, normalize_header,
                     run_file, run_folder_count)

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024"          # real _Edited DBC + config from CODE_GEN/DBC_40024_2
TIME = "2000-01-01 00:00"
# The legacy runs of this fixture use 209 receive rules (81 in FIFO 2). With limits that allow this the
# output must stay identical to the legacy tool; the 192-rule platform limit is tested in test_fifo_pipeline.
LEGACY_LIMITS = {"max_rx_rules": 256, "max_rules_per_fifo": 128}


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A working folder like the app folder (generators use ./data and ./CODE_GEN)."""
    h = tmp_path / "CoGeNT home with spaces"
    shutil.copytree(load_fixture(FIXTURE).data_dir, h / "data")
    (h / "data" / "CanFifoConfiguration.data").write_text(json.dumps(LEGACY_LIMITS), encoding="utf-8")
    monkeypatch.chdir(h)
    monkeypatch.setenv("LOGNAME", "cogent-test")
    return h


def _generate(dbc=None):
    from cogent_generate import run_code_generation
    return run_code_generation(str(dbc or load_fixture(FIXTURE).dbc), "SMART_CORE", TIME)


def _edit(home, name, change):
    p = home / "data" / name
    data = json.loads(p.read_text(encoding="utf-8"))
    change(data)
    p.write_text(json.dumps(data), encoding="utf-8")


def _previous_outputs(home):
    (home / "CODE_GEN").mkdir(exist_ok=True)
    for f in CODE_FILES:
        (home / "CODE_GEN" / f).write_text("previous " + f, encoding="utf-8")


def _assert_previous_outputs_untouched(home):
    for f in CODE_FILES:
        assert (home / "CODE_GEN" / f).read_text(encoding="utf-8") == "previous " + f, f
    assert not (home / "CODE_GEN" / ".staging").exists()
    assert run_folder_count(home) == 0                            # a failed run creates no run folder


def _assert_user_friendly(text):
    assert "Traceback" not in text and 'File "' not in text
    assert "Reason:" in text


def test_generation_writes_all_files_identical_to_legacy_run(home):
    (home / "CODE_GEN").mkdir()
    (home / "CODE_GEN" / "errorlog.txt").write_text("old failure", encoding="utf-8")
    written = _generate()
    assert sorted(written.files) == sorted(CODE_FILES)
    assert written.fifo_counts == (64, 64, 81) and written.manual_actions == 0
    legacy = LEGACY_REFS[FIXTURE][0]
    for f in CODE_FILES:
        assert normalize_header(run_file(home, f).read_bytes()) == normalize_header((legacy / f).read_bytes()), f
    assert not (home / "CODE_GEN" / "errorlog.txt").exists()      # stale log removed after success
    assert not (home / "CODE_GEN" / ".staging").exists()


def test_repeat_generation_gives_identical_files(home):
    _generate()
    first = {f: run_file(home, f).read_bytes() for f in CODE_FILES}
    _generate()
    assert run_folder_count(home) == 2                            # the second run gets its own folder
    for f in CODE_FILES:
        assert normalize_date_by(run_file(home, f).read_bytes()) == normalize_date_by(first[f]), f


def test_unsupported_multiplex_layout_is_explained_before_any_file_is_written(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    _edit(home, "CanDbcMsgConfiguration.data", lambda d: d.__setitem__("BMS19_100_rx_enable", "on"))
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    _assert_user_friendly(text)
    assert "BMS19_100" in text and "multiplex" in text.lower()
    assert "BMS_CELLTEMP" in text and "bit 16" in text
    assert "TX/RX messages" in text
    _assert_previous_outputs_untouched(home)


def test_missing_signal_setting_names_signal_field_file_and_page(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    _edit(home, "CanDbcSigConfiguration.data",
          lambda d: [d.pop(k) for k in [k for k in d if k.endswith("_os_notify_no_of_events")]])
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    _assert_user_friendly(text)
    assert "nw_vnim_app_signals_par.c" in text
    assert "os_notify_no_of_events" in text and "signal" in text
    assert "CanDbcSigConfiguration.data" in text and "TX/RX signals" in text
    _assert_previous_outputs_untouched(home)
    log = (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")
    assert "Traceback" in log and "KeyError" in log and "SMART_CORE" in log
    assert (home / "logs" / "cogent.log").read_text(encoding="utf-8").count("Traceback") >= 1


def test_missing_message_setting_names_message_and_page(home):
    from cogent_errors import CogentError
    _edit(home, "CanDbcMsgConfiguration.data", lambda d: d.pop("VCU5_500_rx_enable"))
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    _assert_user_friendly(text)
    assert "VCU5_500" in text and "rx_enable" in text
    assert "CanDbcMsgConfiguration.data" in text and "TX/RX messages" in text


def test_damaged_configuration_file_is_named(home):
    from cogent_errors import CogentError
    (home / "data" / "CanDbcMsgConfiguration.data").write_text("{broken", encoding="utf-8")
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    _assert_user_friendly(text)
    assert "CanDbcMsgConfiguration.data" in text and "damaged" in text


def test_unsaved_signal_configuration_is_named(home):
    from cogent_errors import CogentError
    (home / "data" / "CanDbcSigConfiguration.data").unlink()
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "CanDbcSigConfiguration.data" in text and "TX/RX signals" in text


def test_missing_dbc_file_is_named(home):
    from cogent_errors import CogentError
    missing = home / "no such folder" / "missing.dbc"
    with pytest.raises(CogentError) as exc:
        _generate(missing)
    text = exc.value.user_message()
    assert "DBC file not found" in text and str(missing) in text


def test_run_folder_that_cannot_be_created_is_explained(home, monkeypatch):
    from cogent_errors import CogentError
    import cogent_generate

    def denied(target):
        raise PermissionError(13, "Access is denied", target)
    monkeypatch.setattr(cogent_generate, "write_config_archive", denied)
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "could not be created" in text and "CODE_GEN" in text and "writable" in text
    assert run_folder_count(home) == 0


def test_unexpected_error_is_reported_without_traceback_and_logged(home, monkeypatch):
    from cogent_errors import CogentError
    import msg

    def boom():
        raise RuntimeError("boom")
    monkeypatch.setattr(msg, "msg_struct_generation", boom)
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    _assert_user_friendly(text)
    assert "nw_il_msg.h" in text and "RuntimeError: boom" in text and "errorlog.txt" in text
    assert "RuntimeError: boom" in (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")
