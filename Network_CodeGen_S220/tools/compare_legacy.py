"""Compare harness output with a legacy CODE_GEN run, ignoring Date/By/Traceability lines."""
import re
import sys
from pathlib import Path

HEADER = re.compile(rb"^(Date|By|Traceability)[ \t]*:.*$", re.M)


def norm(path):
    return HEADER.sub(lambda m: m.group(1) + b": <normalized>", path.read_bytes())


def main(actual_dir, legacy_dir):
    bad = 0
    for f in sorted(Path(legacy_dir).iterdir()):
        a = Path(actual_dir) / f.name
        if f.suffix == ".cfg" and f.name != "can_rxrule.cfg":
            continue  # saved config archive, not an output
        if f.suffix == ".dbc" or f.suffix == ".ini":
            continue
        same = a.exists() and norm(a) == norm(f)
        bad += not same
        print(f"{'OK  ' if same else 'DIFF'} {f.name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
