"""Generate tests/expected/<fixture>/ with the Python 2.7 oracle on the baseline commit.

The baseline source is extracted with `git archive` into a folder OUTSIDE the repo
(no worktree, no nested .git). Requires a Python 2.7 interpreter (COGENT_PY27)."""
import io
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY27 = os.environ.get("COGENT_PY27", r"C:\Python27\python.exe")
BASELINE_REF = os.environ.get("COGENT_BASELINE_REF", "83612bb88e15950f106efae85885f2627819a944")
BASE = Path(os.environ.get("COGENT_BASELINE_DIR", Path(tempfile.gettempdir()) / "cogent_py27_baseline"))
SUBDIR = "Network_CodeGen_S220"


def extract_baseline():
    app = BASE / SUBDIR
    if app.exists():
        return app
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, check=True,
                         capture_output=True, text=True).stdout.strip()
    blob = subprocess.run(["git", "archive", "--format=zip", BASELINE_REF, SUBDIR], cwd=top,
                          check=True, capture_output=True).stdout
    zipfile.ZipFile(io.BytesIO(blob)).extractall(BASE)
    return app


def main():
    if not Path(PY27).exists():
        raise SystemExit(f"Python 2.7 oracle not found at {PY27} (set COGENT_PY27)")
    base_app = extract_baseline()
    harness = ROOT / "tools" / "gen_harness.py"
    dump = ROOT / "tools" / "dump_dbc.py"
    for fdir in sorted((ROOT / "tests" / "fixtures").iterdir()):
        meta_file = fdir / "fixture.json"
        if not meta_file.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        exp = ROOT / "tests" / "expected" / fdir.name
        dbc = fdir / meta["dbc"]
        for stage in ("code", "pages"):
            subprocess.run([PY27, "-B", str(harness), "--dbc", str(dbc), "--node", meta["node"],
                            "--data", str(fdir / "data"), "--out", str(exp / stage),
                            "--stage", stage, "--app-dir", str(base_app)], check=True)
        env = dict(os.environ, COGENT_APP_DIR=str(base_app))
        out = subprocess.run([PY27, "-B", str(dump), str(dbc), meta["node"]],
                             check=True, capture_output=True, env=env).stdout
        (exp / "parser.json").write_bytes(out)
        print(f"{fdir.name}: ok")


if __name__ == "__main__":
    sys.exit(main())
