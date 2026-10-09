"""Receive-rule (FIFO) checks in the GUI code generation pipeline (cogent_generate)."""
import json
import shutil
import sys

import pytest

from support import CODE_FILES, ROOT, load_fixture, normalize_date_by

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024_a"        # 40024 _Edited DBC + configuration of the 2026-02-26 12:10 run
TIME = "2000-01-01 00:00"
REFERENCE_CONFIG = {               # what the manual edits of the S2XX workspace correspond to
    "merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
    "additional_rx_messages": ["BMS19_100", "BMS20_100"],
}
REPORTS = ["fifo_plan.json", "MANUAL_ACTIONS.md"]


@pytest.fixture
def home(tmp_path, monkeypatch):
    h = tmp_path / "CoGeNT home with spaces"
    shutil.copytree(load_fixture(FIXTURE).data_dir, h / "data")
    monkeypatch.chdir(h)
    monkeypatch.setenv("LOGNAME", "cogent-test")
    return h


def _fifo_config(home, config):
    (home / "data" / "CanFifoConfiguration.data").write_text(json.dumps(config), encoding="utf-8")


def _generate():
    from cogent_generate import run_code_generation
    return run_code_generation(str(load_fixture(FIXTURE).dbc), "SMART_CORE", TIME)


def _previous_outputs(home):
    (home / "CODE_GEN").mkdir(exist_ok=True)
    for f in CODE_FILES + REPORTS:
        (home / "CODE_GEN" / f).write_text("previous " + f, encoding="utf-8")


def _assert_previous_outputs_untouched(home):
    for f in CODE_FILES + REPORTS:
        assert (home / "CODE_GEN" / f).read_text(encoding="utf-8") == "previous " + f, f
    assert not (home / "CODE_GEN" / ".staging").exists()


def _rules(home):
    from cogent_fifo import read_rule_table
    return read_rule_table((home / "CODE_GEN" / "can_rxrule.cfg").read_text(encoding="latin-1"))


# ---- overflow is detected before any file is written ------------------------------------------------
def test_overflow_with_platform_defaults_names_counts_messages_and_candidates(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "Traceback" not in text
    assert "209 receive rules are needed but the controller accepts at most 192" in text
    assert "FIFO 2 (PTR1 0x400) has 81 receive rules, limit 64" in text
    assert "these do not fit: CCM_ACTIVE (0x3AC)" in text and "VCU_WAKEUP (0x09F)" in text   # NM rules at the end of FIFO 2
    assert "0x4F0-0x4FF: 16 messages" in text and "0x3D0-0x3DF: 13 messages" in text
    assert "merge_blocks" in text and "CanFifoConfiguration.data" in text and "No file was changed" in text
    _assert_previous_outputs_untouched(home)
    assert "209 receive rules" in (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")


@pytest.mark.parametrize("limit, fits", [(184, True), (183, False)])
def test_total_limit_boundary_on_real_configuration(home, limit, fits):
    from cogent_errors import CogentError
    _fifo_config(home, dict(REFERENCE_CONFIG, max_rx_rules=limit))
    if fits:
        assert sum(_generate().fifo_counts) == 184
    else:
        with pytest.raises(CogentError) as exc:
            _generate()
        assert "184 receive rules are needed but the controller accepts at most 183" in str(exc.value)


def test_invalid_fifo_configuration_is_named_and_nothing_is_written(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    _fifo_config(home, {"merge_blocks": [{"base": "0x3D1", "mask": "0x7F0"}]})
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "CanFifoConfiguration.data" in text and "0x3D1" in text and "not aligned" in text
    _assert_previous_outputs_untouched(home)


def test_unknown_additional_message_is_named_and_nothing_is_written(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    _fifo_config(home, dict(REFERENCE_CONFIG, additional_rx_messages=["BMS99_100"]))
    with pytest.raises(CogentError) as exc:
        _generate()
    assert "BMS99_100" in str(exc.value) and "additional_rx_messages" in str(exc.value)
    _assert_previous_outputs_untouched(home)


def test_generated_rules_are_checked_against_the_plan_before_publishing(home, monkeypatch):
    from cogent_errors import CogentError
    import cogent_fifo
    _previous_outputs(home)
    _fifo_config(home, REFERENCE_CONFIG)
    real = cogent_fifo.read_rule_table
    monkeypatch.setattr(cogent_fifo, "read_rule_table", lambda text: real(text)[1:])   # a generator that drops a rule
    with pytest.raises(CogentError) as exc:
        _generate()
    assert "do not match the receive-rule plan" in str(exc.value) and "183 rules, planned 184" in str(exc.value)
    _assert_previous_outputs_untouched(home)


# ---- generation with the merged ID blocks -----------------------------------------------------------
def test_reference_configuration_generates_184_rules_and_reports(home):
    _fifo_config(home, REFERENCE_CONFIG)
    result = _generate()
    assert result.fifo_counts == (64, 64, 56) and result.max_rx_rules == 192
    assert sorted(result.files) == sorted(CODE_FILES) and result.reports == REPORTS
    rules = _rules(home)
    assert len(rules) == 184
    assert (0x3D0, 0xC00007F0, 0x200) in rules and (0x4F0, 0xC00007F0, 0x200) in rules
    assert not [r for r in rules if 0x3D1 <= r[0] <= 0x3DF or 0x4F1 <= r[0] <= 0x4FF]
    assert (0x3EB, 0xC00007FF, 0x100) in rules and (0x3EC, 0xC00007FF, 0x100) in rules   # BMS19_100, BMS20_100
    plan = json.loads((home / "CODE_GEN" / "fifo_plan.json").read_text(encoding="utf-8"))
    assert plan["total_rules"] == 184 and plan["fifo_counts"] == [64, 64, 56]
    assert [b["block"] for b in plan["merged_blocks"]] == ["0x3D0-0x3DF", "0x4F0-0x4FF"]
    assert [len(b["members"]) for b in plan["merged_blocks"]] == [13, 16]
    report = (home / "CODE_GEN" / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "## MANUAL: nw_can_dll.c dispatch for the merged block 0x3D0-0x3DF" in report
    assert "case 0x3D2u: canFrameHandle = VNIM_BMS11_100_MESSAGE; break;" in report
    assert "case 0x4FFu: canFrameHandle = VNIM_REM_MSG_15_MESSAGE; break;" in report
    assert "## MANUAL: interaction-layer and VNIM code for BMS19_100" in report
    assert "Rx enable is off" in report
    for heading in ("File and location", "Current value", "Required change", "Why CoGeNT cannot do it",
                    "Dependencies", "Steps", "Verification"):
        assert report.count("**%s:**" % heading) == result.manual_actions
    assert result.manual_actions == report.count("\n## MANUAL: ") + report.count("\n## REVIEW: ")


def test_repeated_generation_is_identical_including_reports(home):
    _fifo_config(home, REFERENCE_CONFIG)
    _generate()
    first = {f: (home / "CODE_GEN" / f).read_bytes() for f in CODE_FILES + REPORTS}
    _generate()
    for f in CODE_FILES:
        assert normalize_date_by((home / "CODE_GEN" / f).read_bytes()) == normalize_date_by(first[f]), f
    for f in REPORTS:
        assert (home / "CODE_GEN" / f).read_bytes() == first[f], f


def test_without_merging_or_overflow_the_report_says_no_action(home):
    _fifo_config(home, {"max_rx_rules": 256, "max_rules_per_fifo": 128})
    result = _generate()
    assert result.manual_actions == 0
    report = (home / "CODE_GEN" / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "No manual action is required for the receive rules." in report
    assert "tools\\carry_forward.py" in report


# ---- configuration archives ------------------------------------------------------------------------
def test_loading_an_archive_without_fifo_configuration_sets_the_current_one_aside(home):
    import back_end
    _fifo_config(home, REFERENCE_CONFIG)
    note = back_end._set_aside_fifo_config(["data/dbc_details.data", "data/CanDbcMsgConfiguration.data"])
    assert "renamed" in note
    assert not (home / "data" / "CanFifoConfiguration.data").exists()
    assert json.loads((home / "data" / "CanFifoConfiguration.data.previous").read_text(encoding="utf-8")) == REFERENCE_CONFIG


def test_loading_an_archive_with_fifo_configuration_keeps_the_file_for_extraction(home):
    import back_end
    _fifo_config(home, REFERENCE_CONFIG)
    assert back_end._set_aside_fifo_config(["data/dbc_details.data", "data/CanFifoConfiguration.data"]) == ""
    assert (home / "data" / "CanFifoConfiguration.data").exists()
