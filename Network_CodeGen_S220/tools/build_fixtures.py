"""Build tests/fixtures/<name>/ from saved .cfg archives + DBC files in the repo."""
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "fixtures"
# The legacy 40024 runs used "..._Edited.dbc", which is not in the repo. The saved
# configuration (data/*.data keys) and the legacy outputs show how the edited DBC differs:
# two diagnostic messages are received (Rx) instead of transmitted (Tx), three mixed-case
# message names are upper-case, and two received signals lost a trailing "_".
# Reconstruct exactly those edits:
EDITED_40024 = [
    ("BO_ 2015 GLOBAL_DIAG_REQ: 8 SMART_CORE", "BO_ 2015 GLOBAL_DIAG_REQ: 8 Vector__XXX"),
    ("BO_ 1919 MGM_DIAG_RES: 8 SMART_CORE", "BO_ 1919 MGM_DIAG_RES: 8 Vector__XXX"),
    ("BO_ 344 BMS_IVT_Msg_Result_U1:", "BO_ 344 BMS_IVT_MSG_RESULT_U1:"),
    ("BO_ 345 BMS_IVT_Msg_Result_U2:", "BO_ 345 BMS_IVT_MSG_RESULT_U2:"),
    ("BO_ 352 BMS_IVT_Msg_Result_U3:", "BO_ 352 BMS_IVT_MSG_RESULT_U3:"),
    (" SG_ SBW1_CRC_ :", " SG_ SBW1_CRC :"),
    (" SG_ TCU6_CRC_ :", " SG_ TCU6_CRC :"),
]
FIXTURES = [
    ("s2xx_40024", "CODE_GEN/DBC_40024_2/26-02-2026_17-37-49.cfg",
     "CODE_GEN/DBC_40024_2/S2XX_SMART_CORE_SVNID_40024_25_02_2026.dbc", "SMART_CORE", EDITED_40024),
    # Config_DBC_35354_1.cfg was saved against a DBC whose SBW1_CRC signal was named "SBW1_CRC_";
    # _2 matches the DBC in DBC/.
    ("s237_35354", "Config/Config_DBC_35354_2.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev35354_180923_Edited.dbc", "SMART_CORE"),
    ("s237_35891", "Config/Config_DBC_35891.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev35891_111223_Edited.dbc", "SMART_CORE"),
    ("s237_36026", "Config/Config_DBC_36026.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36026_110124_Edited.dbc", "SMART_CORE"),
    ("s237_36144", "Config/Config_DBC_36144.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc", "SMART_CORE"),
    ("s237_100723", "Config/Config_S237_Common_DBC_Itr12.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_100723_Edited.dbc", "SMART_CORE"),
    # Pairs whose legacy CODE_GEN run was produced by the current (2024-07+) source:
    ("s2xx_40024_a", "CODE_GEN/DBC_40024/26-02-2026_12-10-10.cfg",
     "CODE_GEN/DBC_40024_2/S2XX_SMART_CORE_SVNID_40024_25_02_2026.dbc", "SMART_CORE", EDITED_40024),
    ("s237_36144_2", "Config/Config_DBC_36144_2.cfg",
     "DBC/S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc", "SMART_CORE"),
]


def build(name, cfg, dbc, node, dbc_patches=()):
    dst = OUT / name
    if dst.exists():
        shutil.rmtree(dst)
    (dst / "data").mkdir(parents=True)
    with zipfile.ZipFile(ROOT / cfg) as z:
        members = [m for m in z.namelist() if m.startswith("data/") and m.endswith(".data")]
        for m in members:
            (dst / "data" / Path(m).name).write_bytes(z.read(m))
    if not (dst / "data" / "CanDbcMsgConfiguration.data").exists():
        raise SystemExit(f"{cfg}: no data/CanDbcMsgConfiguration.data")
    dbc_name = Path(dbc).name
    if dbc_patches:
        text = (ROOT / dbc).read_bytes()
        for old, new in dbc_patches:
            assert text.count(old.encode("latin-1")) == 1, old
            text = text.replace(old.encode("latin-1"), new.encode("latin-1"))
        dbc_name = Path(dbc).stem + "_Edited_reconstructed.dbc"
        (dst / dbc_name).write_bytes(text)
    else:
        shutil.copyfile(ROOT / dbc, dst / dbc_name)  # content only: some source DBCs are read-only
    meta = {"dbc": dbc_name, "node": node, "source_cfg": cfg, "source_dbc": dbc,
            "dbc_patches": [list(p) for p in dbc_patches]}
    (dst / "fixture.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{name}: {len(members)} data files")


if __name__ == "__main__":
    for row in FIXTURES:
        build(*row)
