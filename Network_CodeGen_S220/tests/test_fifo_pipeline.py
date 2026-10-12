"""Receive-rule (FIFO) checks in the GUI code generation pipeline (cogent_generate)."""
import json
import shutil
import sys

import pytest

from support import CODE_FILES, ROOT, latest_run, load_fixture, normalize_date_by, run_file, run_folder_count

sys.path.insert(0, str(ROOT))

FIXTURE = "s2xx_40024_a"        # 40024 _Edited DBC + configuration of the 2026-02-26 12:10 run
TIME = "2000-01-01 00:00"
REFERENCE_CONFIG = {               # what the manual edits of the S2XX workspace correspond to
    "merge_blocks": [{"base": "0x3D0", "mask": "0x7F0"}, {"base": "0x4F0", "mask": "0x7F0"}],
    "additional_rx_messages": ["BMS19_100", "BMS20_100"],
}
REPORTS = ["fifo_plan.json", "MANUAL_ACTIONS.md"]


def sorted_runs(home):
    import cogent_generate
    from pathlib import Path
    return [Path(p) for p in cogent_generate.run_folders(str(home / "CODE_GEN"))]


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
    assert run_folder_count(home) == 0                            # a failed run creates no run folder


def _rules(home):
    from cogent_fifo import read_rule_table
    return read_rule_table(run_file(home, "can_rxrule.cfg").read_text(encoding="latin-1"))


# ---- overflow is detected before any file is written ------------------------------------------------
def test_overflow_popup_is_short_and_the_log_names_messages_and_candidates(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "Traceback" not in text and len(text) < 500
    assert "209 CAN receive rules are needed, but the controller accepts 192 (FIFO 0/1/2: 64/64/81)" in text
    assert "Receive FIFO" in text and "Apply" in text and "Nothing was changed" in text
    _assert_previous_outputs_untouched(home)
    log = (home / "CODE_GEN" / "errorlog.txt").read_text(encoding="utf-8")
    assert "FIFO 2 (PTR1 0x400) has 81 receive rules, limit 64" in log
    assert "these do not fit: CCM_ACTIVE (0x3AC)" in log and "VCU_WAKEUP (0x09F)" in log   # NM rules at the end of FIFO 2
    assert "0x4F0-0x4FF: 16 messages" in log and "0x3D0-0x3DF: 13 messages" in log


@pytest.mark.parametrize("limit, fits", [(184, True), (183, False)])
def test_total_limit_boundary_on_real_configuration(home, limit, fits):
    from cogent_errors import CogentError
    _fifo_config(home, dict(REFERENCE_CONFIG, max_rx_rules=limit))
    if fits:
        assert sum(_generate().fifo_counts) == 184
    else:
        with pytest.raises(CogentError) as exc:
            _generate()
        assert "184 CAN receive rules are needed, but the controller accepts 183" in str(exc.value)


def test_invalid_fifo_configuration_is_named_and_nothing_is_written(home):
    from cogent_errors import CogentError
    _previous_outputs(home)
    _fifo_config(home, {"merge_blocks": [{"base": "0x3D1", "mask": "0x7F0"}]})
    with pytest.raises(CogentError) as exc:
        _generate()
    text = exc.value.user_message()
    assert "CanFifoConfiguration.data" in text and "0x3D1" in text and "not aligned" in text
    assert "Receive FIFO" in text
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
    plan = json.loads((latest_run(home) / "fifo_plan.json").read_text(encoding="utf-8"))
    assert plan["total_rules"] == 184 and plan["fifo_counts"] == [64, 64, 56]
    assert [b["block"] for b in plan["merged_blocks"]] == ["0x3D0-0x3DF", "0x4F0-0x4FF"]
    assert [len(b["members"]) for b in plan["merged_blocks"]] == [13, 16]
    report = (latest_run(home) / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
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
    first = {f: run_file(home, f).read_bytes() for f in CODE_FILES}
    first.update({f: (latest_run(home) / f).read_bytes() for f in REPORTS})
    _generate()
    for f in CODE_FILES:
        assert normalize_date_by(run_file(home, f).read_bytes()) == normalize_date_by(first[f]), f
    for f in REPORTS:                                             # the reports name the run folder: compare without it
        assert (latest_run(home) / f).read_bytes().decode("utf-8").replace(latest_run(home).name, "RUN") == \
            first[f].decode("utf-8").replace(sorted_runs(home)[0].name, "RUN"), f


def test_without_merging_or_overflow_the_report_says_no_action(home):
    _fifo_config(home, {"max_rx_rules": 256, "max_rules_per_fifo": 128})
    result = _generate()
    assert result.manual_actions == 0
    report = (latest_run(home) / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "No manual action is required for the receive rules." in report
    assert "tools\\carry_forward.py" in report


# ---- configuration archives ------------------------------------------------------------------------
def test_loading_an_archive_without_fifo_settings_keeps_the_current_ones(home):
    import back_end
    _fifo_config(home, REFERENCE_CONFIG)
    note = back_end._fifo_note(["data/dbc_details.data", "data/CanDbcMsgConfiguration.data"])
    assert "were kept" in note
    assert json.loads((home / "data" / "CanFifoConfiguration.data").read_text(encoding="utf-8")) == REFERENCE_CONFIG
    assert not (home / "data" / "CanFifoConfiguration.data.previous").exists()


def test_loading_an_archive_without_code_overrides_keeps_the_current_ones(home):
    import back_end
    assert back_end._overrides_note(["data/dbc_details.data"]) == ""          # none saved: nothing to say
    (home / "data" / "CanOverrideConfiguration.data").write_text('{"numeric_order": ["REM_MSG_"]}', encoding="utf-8")
    assert "Code overrides were kept" in back_end._overrides_note(["data/dbc_details.data"])
    assert back_end._overrides_note(["data/dbc_details.data", "data/CanOverrideConfiguration.data"]) == ""


def test_loading_an_archive_with_fifo_settings_needs_no_note(home):
    import back_end
    _fifo_config(home, REFERENCE_CONFIG)
    assert back_end._fifo_note(["data/dbc_details.data", "data/CanFifoConfiguration.data"]) == ""


def test_enabled_additional_message_needs_no_manual_action(home):
    from support import enable_indexed
    fx = load_fixture(FIXTURE)
    _fifo_config(home, REFERENCE_CONFIG)
    enable_indexed(home, fx.dbc, fx.node)
    result = _generate()
    report = (latest_run(home) / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")
    assert "interaction-layer and VNIM code for BMS19_100" not in report
    assert "## REVIEW: additional_rx_messages lists BMS19_100" in report
    assert result.fifo_counts == (64, 64, 56)        # the same rules as through additional_rx_messages


def _report(home):
    return (latest_run(home) / "MANUAL_ACTIONS.md").read_text(encoding="utf-8")


def _entry_of(report, heading):
    start = report.index(heading)
    return report[start:report.index("\n## ", start + 4)]


def test_disabled_additional_message_says_how_to_generate_it(home):
    _fifo_config(home, REFERENCE_CONFIG)
    _generate()
    entry = _entry_of(_report(home), "## MANUAL: interaction-layer and VNIM code for BMS19_100")
    assert "VCU5_500" not in entry
    assert "tick the Rx enable box of BMS19_100" in entry and "generates its code" in entry


def _workspace_dll(home, text):
    """A workspace folder with nw_can_dll.c, chosen as 'Your workspace' on the Re-apply edits page."""
    ws = home.parent / "workspace"
    (ws / "src").mkdir(parents=True, exist_ok=True)
    (ws / "src" / "nw_can_dll.c").write_text(text, encoding="latin-1")
    (home / "data" / "ReapplyEdits.data").write_text(json.dumps({"base": "", "edited": str(ws)}), encoding="utf-8")
    return ws / "src" / "nw_can_dll.c"


@pytest.mark.parametrize("edited", [5, "unreadable"])
def test_a_workspace_that_cannot_be_searched_does_not_stop_the_generation(home, monkeypatch, edited):
    import cogent_carry
    _fifo_config(home, REFERENCE_CONFIG)
    if edited == "unreadable":
        (home.parent / "ws").mkdir()
        edited = str(home.parent / "ws")

        def unreadable(root, name):
            raise PermissionError(13, "Access is denied", root)
        monkeypatch.setattr(cogent_carry, "find_file", unreadable)
    (home / "data" / "ReapplyEdits.data").write_text(json.dumps({"base": "", "edited": edited}), encoding="utf-8")
    result = _generate()
    assert result.manual_actions > 0
    assert "## MANUAL: nw_can_dll.c dispatch for the merged block 0x3D0-0x3DF" in _report(home)


def test_dispatch_of_the_workspace_is_checked(home):
    import re
    _fifo_config(home, REFERENCE_CONFIG)
    first = _generate()
    snippets = re.findall(r"```c\n(.*?)\n```", _report(home), re.S)
    assert len(snippets) == 2
    dll = _workspace_dll(home, "void DllDispatchReceivedMessage(void)\n{\n" + "\n".join(snippets) + "\n}\n")
    second = _generate()
    report = _report(home)
    assert second.manual_actions == first.manual_actions - 2
    assert "## MANUAL: nw_can_dll.c dispatch" not in report
    assert report.count("already maps every ID of the block") == 2 and str(dll) in report
    dll.write_text(dll.read_text(encoding="latin-1").replace(
        "case 0x3D2u: canFrameHandle = VNIM_BMS11_100_MESSAGE; break;", ""), encoding="latin-1")
    third = _generate()
    report = _report(home)
    assert third.manual_actions == first.manual_actions - 1
    entry = _entry_of(report, "## MANUAL: nw_can_dll.c dispatch for the merged block 0x3D0-0x3DF")
    assert "ID 0x3D2 (VNIM_BMS11_100_MESSAGE) is not mapped" in entry and str(dll) in entry
    assert report.count("already maps every ID of the block") == 1
