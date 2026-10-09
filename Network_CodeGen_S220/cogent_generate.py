"""Code generation for the GUI's 'code gen' button.

Runs the generators in the legacy order into CODE_GEN/.staging and replaces the files in
CODE_GEN only when every generator succeeded, so a failed run never leaves a mix of new and
old files. Failures are raised as CogentError with a user-facing explanation; the traceback
goes to CODE_GEN/errorlog.txt and logs/cogent.log.

The CAN receive rules are planned and checked against the controller limits (cogent_fifo,
data/CanFifoConfiguration.data) before any generator runs, and the generated can_rxrule.cfg and
nw_can_dll.h are checked against that plan before they are published. Every run also writes
CODE_GEN/fifo_plan.json and CODE_GEN/MANUAL_ACTIONS.md."""
import importlib
import json
import os
import shutil
import sys
from dataclasses import dataclass

import cogent_fifo
import cogent_io
from cogent_errors import (MSG_DATA_FILE, MSG_PAGE, SIG_DATA_FILE, SIG_PAGE, CogentError, log_failure,
                           missing_config_entry)

DATA_DIR = './data'
OUTPUT_DIR = './CODE_GEN'
STAGING_DIR = os.path.join(OUTPUT_DIR, '.staging')
ERROR_LOG = os.path.join(OUTPUT_DIR, 'errorlog.txt')

# (module, [(function, files it writes)]) in the order of the legacy BackEnd.code_gen
PLAN = [
    ("can_rx_filt_gen", [("filter_gen", ["can_rxrule.cfg", "nw_can_dll.h"])]),
    ("msg", [("msg_struct_generation", ["nw_il_msg.h"])]),
    ("il_par_h_generation", [("il_par_h_gen_function", ["nw_il_par.h"])]),
    ("il_par_c_generation", [("il_par_c_gen_function", ["nw_il_par.c"])]),
    ("vnim_app_signals_par", [("vnim_app_c_gen", ["nw_vnim_app_signals_par.c"]),
                              ("vnim_app_h_gen", ["nw_vnim_app_signals_par.h"]),
                              ("vnim_resource_gen", ["vnim.msg.resource", "vnim.txrx.resource",
                                                     "nw_host_mgr_txrx.resource"]),
                              ("nm_par_gen", ["nw_nm_par.h"])]),
]
GENERATED_FILES = [f for _, funcs in PLAN for _, files in funcs for f in files]
FIFO_PLAN = "fifo_plan.json"
MANUAL_ACTIONS = "MANUAL_ACTIONS.md"
REPORT_FILES = [FIFO_PLAN, MANUAL_ACTIONS]


@dataclass
class GenerationResult:
    files: list            # generated source files now in CODE_GEN
    reports: list          # REPORT_FILES
    manual_actions: int    # entries of MANUAL_ACTIONS.md that need the user
    fifo_counts: tuple     # receive rules per FIFO
    max_rx_rules: int


def run_code_generation(dbc, node, time_str):
    """Generate all files for `dbc`/`node` into ./CODE_GEN. Returns a GenerationResult."""
    context = {"DBC file": dbc, "Node": node, "Working folder": os.getcwd()}
    try:
        msg_cfg = _check_inputs(dbc, node)
        _check_multiplex(dbc, node, msg_cfg)
        plan, fifo_config = _check_fifo(dbc, node, msg_cfg)
        _run_generators(dbc, node, time_str)
        _check_generated_rules(plan)
        manual = _write_reports(plan, fifo_config, dbc, node, msg_cfg)
        _publish()
    except CogentError as err:
        err.log_path = log_failure("Code generation", err, context, extra_file=ERROR_LOG)
        raise
    finally:
        shutil.rmtree(STAGING_DIR, ignore_errors=True)
    if os.path.exists(ERROR_LOG):
        os.remove(ERROR_LOG)  # the last run succeeded; an old failure log would mislead
    return GenerationResult(list(GENERATED_FILES), list(REPORT_FILES), manual, plan.fifo_counts(),
                            fifo_config.max_rx_rules)


def _check_inputs(dbc, node):
    if not os.path.isfile(dbc):
        raise CogentError("Code generation", "DBC file not found: %s" % dbc, item="reading the DBC file",
                          hint="Select the DBC with 'Browse ..', press 'Load DBC', then run code gen again.")
    loaded = {}
    for name, page in ((MSG_DATA_FILE, MSG_PAGE), (SIG_DATA_FILE, SIG_PAGE)):
        path = os.path.join(DATA_DIR, name)
        if not os.path.isfile(path):
            raise CogentError("Code generation", "data\\%s does not exist (the page has not been saved yet)" % name,
                              item="reading the saved configuration",
                              hint="Open '%s' and press 'Save and Back', then run code gen again." % page)
        try:
            with open(path, encoding='utf-8') as fh:
                loaded[name] = json.load(fh)
        except ValueError as exc:  # JSONDecodeError and UnicodeDecodeError
            raise CogentError("Code generation", "data\\%s is damaged (%s)" % (name, exc),
                              item="reading the saved configuration",
                              hint="Open '%s' and press 'Save and Back' to write it again, or use "
                                   "'load_cofiguration' to load a saved configuration." % page) from exc
    return loaded[MSG_DATA_FILE]


def multiplex_error(msg_name, multiplexor, problem):
    return CogentError(
        "Code generation",
        "message %s is multiplexed (multiplexor %s) and %s. CoGeNT can only generate multiplexed messages "
        "laid out like VCU5_500: every multiplexed signal starts at bit 0 and the multiplexor is in byte 7"
        % (msg_name, multiplexor, problem),
        item="generating nw_il_msg.h",
        hint="Untick the Rx enable box of %s in '%s' and press 'Save and Back', then run code gen again. "
             "Generating this multiplex layout needs a generator extension (contact the tool maintainer)."
             % (msg_name, MSG_PAGE))


def _check_multiplex(dbc, node, msg_cfg):
    from Dbc_Parser import dbc_parser
    import msg
    found = msg.find_unsupported_multiplex(dbc_parser(dbc, node), msg_cfg)
    if found:
        raise multiplex_error(*found)


def _check_fifo(dbc, node, msg_cfg):
    """Plan the CAN receive rules and check them against the controller before any file is written."""
    import can_rx_filt_gen
    from Dbc_Parser import dbc_parser
    op, item = "Code generation", "planning the CAN receive rules (can_rxrule.cfg, nw_can_dll.h)"
    try:
        config = cogent_fifo.load_config(DATA_DIR)
    except cogent_fifo.FifoConfigError as exc:
        raise CogentError(op, str(exc), item="reading the FIFO configuration",
                          hint="No file was changed. Correct data\\%s (see FIFO_MULTIPLEXING.md) or delete it to "
                               "use the platform defaults, then run code gen again." % cogent_fifo.CONFIG_FILE) from exc
    try:
        plan = can_rx_filt_gen.plan_rx_rules(dbc_parser(dbc, node), msg_cfg, config)
    except cogent_fifo.FifoPlanError as exc:
        raise CogentError(op, "; ".join(exc.problems), item=item,
                          hint="No file was changed. Correct merge_blocks / additional_rx_messages in data\\%s or the "
                               "Rx settings on '%s', then run code gen again." % (cogent_fifo.CONFIG_FILE, MSG_PAGE)) from exc
    except KeyError as exc:
        err = missing_config_entry(exc.args[0], "can_rxrule.cfg / nw_can_dll.h") if exc.args and isinstance(exc.args[0], str) else None
        if err is None:
            raise
        raise err from exc
    problems = cogent_fifo.check_limits(plan, config)
    if problems:
        raise CogentError(op, "; ".join(problems), item=item, hint=cogent_fifo.overflow_hint(plan, config))
    return plan, config


def _check_generated_rules(plan):
    """The staged can_rxrule.cfg and nw_can_dll.h must contain exactly the planned rules."""
    def staged(name):
        with open(os.path.join(STAGING_DIR, name), encoding='latin-1') as fh:
            return fh.read()
    want = [(r.can_id, r.mask, r.ptr1) for r in plan.rules()]
    got = cogent_fifo.read_rule_table(staged("can_rxrule.cfg"))
    vectors = cogent_fifo.read_dispatch_counts(staged("nw_can_dll.h"))
    if got != want or vectors != plan.fifo_counts():
        raise CogentError("Code generation", "the generated receive rules do not match the receive-rule plan "
                          "(can_rxrule.cfg: %d rules, planned %d; nw_can_dll.h dispatch entries %s, planned %s)"
                          % (len(got), len(want), vectors, plan.fifo_counts()),
                          item="checking can_rxrule.cfg and nw_can_dll.h",
                          hint="No file was changed. This is a problem in the generator; please send "
                               "CODE_GEN\\errorlog.txt to the tool maintainer.")


def _write_reports(plan, config, dbc, node, msg_cfg):
    """CODE_GEN/fifo_plan.json and CODE_GEN/MANUAL_ACTIONS.md (staged with the generated files)."""
    disabled = [n for n in config.additional_rx_messages
                if msg_cfg.get(n.upper() + '_rx_enable') not in ('on', 'ON', 'On', 1, '1')]
    text, entries = cogent_fifo.manual_actions(plan, config, os.path.basename(dbc), node, disabled)
    with open(os.path.join(STAGING_DIR, MANUAL_ACTIONS), 'w', encoding='utf-8') as fh:
        fh.write(text)
    with open(os.path.join(STAGING_DIR, FIFO_PLAN), 'w', encoding='utf-8') as fh:
        json.dump(cogent_fifo.plan_summary(plan, config), fh, indent=1)
        fh.write("\n")
    return entries


def _run_generators(dbc, node, time_str):
    shutil.rmtree(STAGING_DIR, ignore_errors=True)
    os.makedirs(STAGING_DIR)
    old_dir, old_stdout = cogent_io.CODE_GEN_DIR, sys.stdout
    cogent_io.CODE_GEN_DIR = STAGING_DIR
    files = GENERATED_FILES[:1]
    try:
        for module_name, funcs in PLAN:
            module = importlib.import_module(module_name)
            files = funcs[0][1]
            cogent_io.current_output = None
            module.set_file_node_il(dbc, node)
            module.set_init_global(time_str)
            for func, files in funcs:
                cogent_io.current_output = None
                getattr(module, func)()
    except CogentError:
        cogent_io.abort_output()
        raise
    except Exception as exc:
        output = cogent_io.current_output or " / ".join(files)
        cogent_io.abort_output()
        raise _explain(exc, output) from exc
    finally:
        sys.stdout = old_stdout
        cogent_io.CODE_GEN_DIR = old_dir
        cogent_io.current_output = None


def _explain(exc, output):
    import msg
    if isinstance(exc, msg.UnsupportedMultiplexLayout):
        return multiplex_error(exc.msg_name, exc.multiplexor, exc.problem)
    if isinstance(exc, (cogent_fifo.FifoConfigError, cogent_fifo.FifoPlanError)):
        return CogentError("Code generation", str(exc), item="generating " + output,
                           hint="Correct data\\%s or the Rx settings on '%s', then run code gen again."
                                % (cogent_fifo.CONFIG_FILE, MSG_PAGE))
    if isinstance(exc, KeyError) and exc.args and isinstance(exc.args[0], str):
        err = missing_config_entry(exc.args[0], output)
        if err is not None:
            return err
    if isinstance(exc, FileNotFoundError):
        return CogentError("Code generation", "file not found: %s" % exc.filename, item="generating " + output,
                           hint="Check that the file exists and that the tool runs from its own folder.")
    if isinstance(exc, PermissionError):
        return CogentError("Code generation", "access denied to %s" % exc.filename, item="generating " + output,
                           hint="Close the file in any program that has it open, or check the folder permissions.")
    return CogentError("Code generation", "internal error %s: %s" % (type(exc).__name__, exc),
                       item="generating " + output,
                       hint="This looks like a problem in the generator rather than in your input. Please send "
                            "CODE_GEN\\errorlog.txt to the tool maintainer.")


def _publish():
    """Move the staged files into CODE_GEN."""
    replaced = []
    for name in GENERATED_FILES + REPORT_FILES:
        target = os.path.join(OUTPUT_DIR, name)
        try:
            os.replace(os.path.join(STAGING_DIR, name), target)
        except PermissionError as exc:
            done = (" Already updated: %s." % ", ".join(replaced)) if replaced else " No file was updated."
            raise CogentError("Code generation", "CODE_GEN\\%s could not be replaced (%s)" % (name, exc.strerror),
                              item="saving the generated files",
                              hint="Close CODE_GEN\\%s in any program that has it open (editor, compare tool) and "
                                   "run code gen again.%s" % (name, done)) from exc
        replaced.append(name)
