"""Code generation for the GUI's 'code gen' button.

Runs the generators in the legacy order into CODE_GEN/.staging. Only when every generator succeeded
the staging folder becomes the run folder CODE_GEN/<dd-mm-yyyy_hh-mm-ss>/, so a failed run leaves
nothing behind and earlier runs are never changed. The run folder holds the configuration archive of
the run (<run>.cfg, as 'Save configuration' writes it), MANUAL_ACTIONS.md, fifo_plan.json and the
generated files in the folders of the S2XX repository (OUTPUT_LAYOUT), ready to copy over it.
Failures are raised as CogentError with a user-facing explanation; the traceback goes to
CODE_GEN/errorlog.txt and logs/cogent.log.

The CAN receive rules are planned and checked against the controller limits (cogent_fifo,
data/CanFifoConfiguration.data) before any generator runs, and the generated can_rxrule.cfg and
nw_can_dll.h are checked against that plan before they are published. Every run also writes
CODE_GEN/fifo_plan.json and CODE_GEN/MANUAL_ACTIONS.md."""
import datetime
import glob
import importlib
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field

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

# Where each file lives in the S2XX repository (dc.app.scl.vehiclecomm), relative to its root.
OUTPUT_LAYOUT = {
    "can_rxrule.cfg": os.path.join("app.nos.arch3", "src"),
    "nw_can_dll.h": os.path.join("app.nos.arch3", "src"),
    "nw_il_msg.h": os.path.join("app.nos.arch3", "src"),
    "nw_il_par.h": os.path.join("app.nos.arch3", "src"),
    "nw_il_par.c": os.path.join("app.nos.arch3", "src"),
    "nw_nm_par.h": os.path.join("app.nos.arch3", "src"),
    "nw_vnim_app_signals_par.c": os.path.join("app.vnim.arch3", "src"),
    "nw_vnim_app_signals_par.h": "app.vnim.arch3",
    "vnim.msg.resource": "app.vnim.arch3",
    "vnim.txrx.resource": "app.vnim.arch3",
    "nw_host_mgr_txrx.resource": "app.host.manager",
}
RUN_FOLDER = re.compile(r"^(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})(?:_(\d+))?$")
ARCHIVE_SOURCES = (('html', '*.html'), ('data', '*.data'), ('js', '*.js'))


@dataclass
class GenerationResult:
    files: list            # generated source files (names)
    reports: list          # REPORT_FILES
    manual_actions: int    # entries of MANUAL_ACTIONS.md that need the user
    fifo_counts: tuple     # receive rules per FIFO
    max_rx_rules: int
    folder: str = ""       # the run folder CODE_GEN/<date_time>
    paths: list = field(default_factory=list)   # generated files relative to the run folder
    config_archive: str = ""                    # <date_time>.cfg in the run folder


def output_relpath(name):
    """Path of a generated file inside a run folder (the S2XX repository layout)."""
    return os.path.join(OUTPUT_LAYOUT.get(name, ""), name)


def _run_stamp():
    return datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')


def run_folders(output_dir=OUTPUT_DIR):
    """Run folders in output_dir, oldest first."""
    def key(name):
        d, mo, y, h, mi, s, n = RUN_FOLDER.match(name).groups()
        return (y, mo, d, h, mi, s, int(n or 1))
    if not os.path.isdir(output_dir):
        return []
    names = [n for n in os.listdir(output_dir) if RUN_FOLDER.match(n) and os.path.isdir(os.path.join(output_dir, n))]
    return [os.path.join(output_dir, n) for n in sorted(names, key=key)]


def latest_run(output_dir=OUTPUT_DIR):
    folders = run_folders(output_dir)
    return folders[-1] if folders else None


def write_config_archive(target):
    """Configuration archive of the current settings (html/*.html, data/*.data, js/*.js of the working
    folder), as 'Save configuration' writes it."""
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for folder, pattern in ARCHIVE_SOURCES:
            for path in sorted(glob.glob(os.path.join('.', folder, pattern))):
                archive.write(path, folder + '/' + os.path.basename(path))


def run_code_generation(dbc, node, time_str):
    """Generate all files for `dbc`/`node` into a new run folder CODE_GEN/<date_time>. Returns a GenerationResult."""
    context = {"DBC file": dbc, "Node": node, "Working folder": os.getcwd()}
    try:
        _check_output_dir()
        run = _new_run_name()
        msg_cfg = _check_inputs(dbc, node)
        _check_multiplex(dbc, node, msg_cfg)
        plan, fifo_config = _check_fifo(dbc, node, msg_cfg)
        _run_generators(dbc, node, time_str)
        _check_generated_rules(plan)
        manual = _write_reports(plan, fifo_config, dbc, node, msg_cfg, os.path.join("CODE_GEN", run))
        folder = _publish(run)
    except CogentError as err:
        err.log_path = log_failure("Code generation", err, context, extra_file=ERROR_LOG)
        raise
    finally:
        shutil.rmtree(STAGING_DIR, ignore_errors=True)
    if os.path.exists(ERROR_LOG):
        os.remove(ERROR_LOG)  # the last run succeeded; an old failure log would mislead
    return GenerationResult(list(GENERATED_FILES), list(REPORT_FILES), manual, plan.fifo_counts(),
                            fifo_config.max_rx_rules, folder, [output_relpath(f) for f in GENERATED_FILES],
                            run + ".cfg")


def _check_output_dir():
    if os.path.exists(OUTPUT_DIR) and not os.path.isdir(OUTPUT_DIR):
        raise CogentError("Code generation", "CODE_GEN next to the tool is a file, not a folder",
                          item="preparing the output folder",
                          hint="Rename or remove the file CODE_GEN, then press Generate code again.")


def _new_run_name():
    stamp, n = _run_stamp(), 1
    name = stamp
    while os.path.exists(os.path.join(OUTPUT_DIR, name)):
        n += 1
        name = "%s_%d" % (stamp, n)
    return name


def _check_inputs(dbc, node):
    if not os.path.isfile(dbc):
        raise CogentError("Code generation", "DBC file not found: %s" % dbc, item="reading the DBC file",
                          hint="Select the DBC with 'Browse', press 'Load DBC', then press Generate code again.")
    loaded = {}
    for name, page in ((MSG_DATA_FILE, MSG_PAGE), (SIG_DATA_FILE, SIG_PAGE)):
        path = os.path.join(DATA_DIR, name)
        if not os.path.isfile(path):
            raise CogentError("Code generation", "data\\%s does not exist (the page has not been saved yet)" % name,
                              item="reading the saved configuration",
                              hint="Open '%s' and press 'Save and Back', then press Generate code again." % page)
        try:
            with open(path, encoding='utf-8') as fh:
                loaded[name] = json.load(fh)
        except ValueError as exc:  # JSONDecodeError and UnicodeDecodeError
            raise CogentError("Code generation", "data\\%s is damaged (%s)" % (name, exc),
                              item="reading the saved configuration",
                              hint="Open '%s' and press 'Save and Back' to write it again, or use "
                                   "'Load configuration' to load a saved configuration." % page) from exc
    return loaded[MSG_DATA_FILE]


def multiplex_error(msg_name, multiplexor, problem):
    return CogentError(
        "Code generation",
        "message %s is multiplexed (multiplexor %s) and %s. CoGeNT can only generate multiplexed messages "
        "laid out like VCU5_500: every multiplexed signal starts at bit 0 and the multiplexor is in byte 7"
        % (msg_name, multiplexor, problem),
        item="generating nw_il_msg.h",
        hint="Untick the Rx enable box of %s in '%s' and press 'Save and Back', then press Generate code again. "
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
        raise CogentError(op, str(exc), item="reading the Receive FIFO settings",
                          hint="Nothing was changed. Open 'Receive FIFO' (left menu) and press Apply to save the "
                               "settings again, then Generate code.") from exc
    try:
        plan = can_rx_filt_gen.plan_rx_rules(dbc_parser(dbc, node), msg_cfg, config)
    except cogent_fifo.FifoPlanError as exc:
        raise CogentError(op, "; ".join(exc.problems), item=item,
                          hint="Nothing was changed. Open 'Receive FIFO' (left menu), remove or change the flagged "
                               "block or receive-only message, press Apply, then Generate code again.") from exc
    except KeyError as exc:
        err = missing_config_entry(exc.args[0], "can_rxrule.cfg / nw_can_dll.h") if exc.args and isinstance(exc.args[0], str) else None
        if err is None:
            raise
        raise err from exc
    problems = cogent_fifo.check_limits(plan, config)
    if problems:
        counts = plan.fifo_counts()
        raise CogentError(op, "%d CAN receive rules are needed, but the controller accepts %d (FIFO 0/1/2: %s)"
                          % (sum(counts), config.max_rx_rules, "/".join(str(c) for c in counts)),
                          hint="Nothing was changed. Open 'Receive FIFO' (left menu, or the card on the home page): "
                               "the ID blocks to combine are already selected. Press Apply, then Generate code again.",
                          details="\n".join(problems) + "\n" + cogent_fifo.overflow_hint(plan, config))
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


def _write_reports(plan, config, dbc, node, msg_cfg, run_dir):
    """fifo_plan.json and MANUAL_ACTIONS.md of the run (staged with the generated files)."""
    disabled = [n for n in config.additional_rx_messages
                if msg_cfg.get(n.upper() + '_rx_enable') not in ('on', 'ON', 'On', 1, '1')]
    text, entries = cogent_fifo.manual_actions(plan, config, os.path.basename(dbc), node, disabled, run_dir)
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
                           hint="Correct data\\%s or the Rx settings on '%s', then press Generate code again."
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


def _publish(run):
    """Arrange the staged files in the repository layout, add the configuration archive and turn the
    staging folder into CODE_GEN/<run>. Returns the run folder."""
    target = os.path.join(OUTPUT_DIR, run)
    try:
        for name in GENERATED_FILES:
            dest = os.path.join(STAGING_DIR, output_relpath(name))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            os.replace(os.path.join(STAGING_DIR, name), dest)
        write_config_archive(os.path.join(STAGING_DIR, run + ".cfg"))
        os.replace(STAGING_DIR, target)
    except OSError as exc:
        raise CogentError("Code generation", "CODE_GEN\\%s could not be created (%s)" % (run, exc.strerror or exc),
                          item="saving the generated files",
                          hint="Check that CODE_GEN is writable and not open in a program that locks it (for "
                               "example a compare tool), then press Generate code again. Earlier runs were not "
                               "changed.") from exc
    return os.path.abspath(target)
