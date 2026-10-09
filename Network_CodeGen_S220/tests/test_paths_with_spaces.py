import shutil
import sys

from support import CODE_FILES, ROOT, load_fixture, normalize_header, run_harness

APP_ITEMS = ["Dbc_Parser.py", "can_rx_filt_gen.py", "msg.py", "il_par_h_generation.py",
             "il_par_c_generation.py", "vnim_app_signals_par.py", "cogent_io.py", "py2compat.py",
             "html", "js"]


def test_generation_with_spaces_in_dbc_data_output_and_app_paths(tmp_path, generated):
    fx = load_fixture("s2xx_40024")
    base = tmp_path / "Network CodeGen & Tests"
    dbc = base / "DBC files" / "S2XX SMART CORE 40024.dbc"
    data = base / "saved data"
    out = base / "generated output" / "CODE GEN"
    app = base / "App Copy With Spaces"
    dbc.parent.mkdir(parents=True)
    shutil.copyfile(fx.dbc, dbc)
    shutil.copytree(fx.data_dir, data)
    app.mkdir()
    for item in APP_ITEMS:
        src = ROOT / item
        (shutil.copytree if src.is_dir() else shutil.copyfile)(src, app / item)

    cmd_fx = fx.__class__(fx.name, fx.dir, dbc, fx.node, data)
    run_harness(sys.executable, cmd_fx, out, "code")
    reference = generated("s2xx_40024", "code")
    for name in CODE_FILES:
        assert (out / name).is_file(), name
        assert normalize_header((out / name).read_bytes()) == normalize_header((reference / name).read_bytes()), name
    # The DBC file name (with spaces) is what the generators record for traceability.
    assert b"S2XX SMART CORE 40024.dbc" in (out / "nw_il_par.h").read_bytes()

    out2 = base / "generated output" / "from app copy"
    import subprocess
    r = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "gen_harness.py"), "--dbc", str(dbc),
                        "--node", fx.node, "--data", str(data), "--out", str(out2), "--stage", "code",
                        "--app-dir", str(app)], capture_output=True, text=True, errors="replace")
    assert r.returncode == 0, r.stderr[-4000:]
    for name in CODE_FILES:
        assert (out2 / name).read_bytes() == (out / name).read_bytes(), name
