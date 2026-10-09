import shutil
import sys

from support import load_fixture, run_harness


def test_page_generation_passes_dbc_bytes_through_unchanged(tmp_path):
    """Python 2 copied DBC bytes into the pages verbatim. A byte that cp1252 cannot encode
    (0x81) must reach the generated page unchanged instead of raising UnicodeEncodeError."""
    fx = load_fixture("s237_36144_2")
    raw = fx.dbc.read_bytes()
    old = b" SG_ OBC_UV_STS :"
    assert raw.count(old) == 1
    dbc = tmp_path / "odd_bytes.dbc"
    dbc.write_bytes(raw.replace(old, b" SG_ OBC_UV_STS\x81 :"))
    data = tmp_path / "data"
    shutil.copytree(fx.data_dir, data)
    out = tmp_path / "pages"
    run_harness(sys.executable, fx, out, "pages", dbc=dbc, data_dir=data)
    assert b"OBC_UV_STS\x81" in (out / "CanDbcSigConfiguration.html").read_bytes()
