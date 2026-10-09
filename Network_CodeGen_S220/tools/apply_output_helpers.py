"""Replace  f=open("./CODE_GEN/X",'w') + sys.stdout = f  with  f=open_output("X"),
and f.close() with close_output(f); add the import. Prints counts for review."""
import re
import sys
from pathlib import Path

EOL = r"[ \t]*(?=\r?$)"
OPEN = re.compile(r"""^(?P<ind>[ \t]*)f\s*=\s*open\(\s*["']\./CODE_GEN/(?P<name>[^"']+)["']\s*,\s*["']w\+?["']\s*\)[ \t]*\r?\n[ \t]*sys\.stdout\s*=\s*f""" + EOL, re.M)
CLOSE = re.compile(r"^(?P<ind>[ \t]*)f\.close\(\)" + EOL, re.M)
DATA = re.compile(r"""open\((?P<arg>\w+_data_dir\s*\+\s*["'][^"']+\.data["'])\s*,\s*'r'\)""")
IMPORT_OS = re.compile(r"^import os(?P<nl>\r?\n)", re.M)

for path in map(Path, sys.argv[1:]):
    with open(path, encoding="latin-1", newline="") as fh:   # keep CRLF/LF exactly
        src = fh.read()
    src, n_open = OPEN.subn(lambda m: f'{m["ind"]}f=open_output("{m["name"]}")', src)
    src, n_close = CLOSE.subn(lambda m: f'{m["ind"]}close_output(f)', src)
    src, n_data = DATA.subn(lambda m: f"open({m['arg']},'r',encoding='utf-8')", src)
    src, n_imp = IMPORT_OS.subn(lambda m: "import os" + m["nl"] + "from cogent_io import open_output, close_output" + m["nl"], src, count=1)
    with open(path, "w", encoding="latin-1", newline="") as fh:
        fh.write(src)
    print(f"{path}: open_output={n_open} close_output={n_close} data_reads={n_data} import_added={n_imp}")
