# -*- coding: utf-8 -*-
"""Headless driver for the CoGeNT pipeline. Mirrors BackEnd.code_gen() and the
page generators. Must stay Python 2.7 + 3.x compatible (it is also the oracle runner)."""
from __future__ import print_function

import argparse
import os
import shutil
import sys
import tempfile
import traceback

DEFAULT_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXED_TIME = "2000-01-01 00:00"
TEST_USER = "cogent-test"

CODE_FILES = [
    "can_rxrule.cfg", "nw_can_dll.h", "nw_il_msg.h", "nw_il_par.h", "nw_il_par.c",
    "nw_vnim_app_signals_par.c", "nw_vnim_app_signals_par.h", "vnim.msg.resource",
    "vnim.txrx.resource", "nw_host_mgr_txrx.resource", "nw_nm_par.h",
]
PAGE_FILES = [
    "html/CanDbcMsgConfiguration.html", "js/CanDbcMsgConfiguration.js",
    "html/CanDbcSigConfiguration.html", "js/CanDbcSigConfiguration.js",
    "html/CanFilterconfiguration.html", "js/CanFilterconfiguration.js",
]

# Same order and calls as back_end.BackEnd.code_gen
CODE_PLAN = [
    ("can_rx_filt_gen", ["filter_gen"]),
    ("msg", ["msg_struct_generation"]),
    ("il_par_h_generation", ["il_par_h_gen_function"]),
    ("il_par_c_generation", ["il_par_c_gen_function"]),
    ("vnim_app_signals_par", ["vnim_app_c_gen", "vnim_app_h_gen", "vnim_resource_gen", "nm_par_gen"]),
]


def _run_code(dbc, node, real_stdout):
    for module_name, funcs in CODE_PLAN:
        mod = __import__(module_name)
        mod.set_file_node_il(dbc, node)
        mod.set_init_global(FIXED_TIME)
        for name in funcs:
            getattr(mod, name)()
            sys.stdout = real_stdout


def _run_pages(dbc, node, real_stdout):
    dbc_gen = __import__("Can_dbc_gen")
    filt = __import__("Can_filter_python_gen")
    dbc_gen.html_mes(dbc, node)
    dbc_gen.html_sig(dbc, node)
    filt.html(dbc, node)
    sys.stdout = real_stdout


def run(dbc, node, data_dir, out_dir, stage="code", app_dir=DEFAULT_APP_DIR):
    dbc = os.path.abspath(dbc).replace("\\", "/")
    app_dir = os.path.abspath(app_dir)
    work = tempfile.mkdtemp(prefix="cogent_")
    old_cwd, real_stdout = os.getcwd(), sys.stdout
    os.environ["LOGNAME"] = TEST_USER  # getpass.getuser() checks LOGNAME first
    try:
        shutil.copytree(os.path.abspath(data_dir), os.path.join(work, "data"))
        for sub in ("html", "js"):
            shutil.copytree(os.path.join(app_dir, sub), os.path.join(work, sub))
        if app_dir not in sys.path:
            sys.path.insert(0, app_dir)
        os.chdir(work)
        try:
            if stage in ("code", "all"):
                _run_code(dbc, node, real_stdout)
            if stage in ("pages", "all"):
                _run_pages(dbc, node, real_stdout)
        finally:
            sys.stdout = real_stdout
            os.chdir(old_cwd)
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)
        if stage in ("code", "all"):
            for name in CODE_FILES:
                shutil.copy2(os.path.join(work, "CODE_GEN", name), os.path.join(out_dir, name))
        if stage in ("pages", "all"):
            for rel in PAGE_FILES:
                shutil.copy2(os.path.join(work, rel), os.path.join(out_dir, os.path.basename(rel)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dbc", required=True)
    p.add_argument("--node", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--stage", choices=["code", "pages", "all"], default="code")
    p.add_argument("--app-dir", default=DEFAULT_APP_DIR)
    a = p.parse_args(argv)
    try:
        run(a.dbc, a.node, a.data, a.out, a.stage, a.app_dir)
    except Exception:
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
