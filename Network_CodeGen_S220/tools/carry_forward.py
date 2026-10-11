"""Command line for re-applying your hand edits to a new generation (the GUI page 'Re-apply edits'
does the same). The logic lives in cogent_carry.

Usage (from Network_CodeGen_S220):
  .venv/Scripts/python.exe tools/carry_forward.py --base <old generated files> --edited <workspace>
        --new CODE_GEN --out <new folder> [--report <file.md>]

  --base    the generated files your edits started from (e.g. CODE_GEN/DBC_40024)
  --edited  your workspace (or a folder); each file is found by its name and must be unique there
  --new     the newly generated files (normally CODE_GEN)
  --out     folder for the merged files; it must not exist yet or be empty, and must not be inside
            --edited, --base or --new

--base, --edited and --new are only read. Exit code: 0 when everything merged and every check passed,
1 when something needs you (see the report), 2 on usage errors."""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cogent_carry import (GENERATED_FILES, LABELS, UsageError, carry_forward, merge3, needs_attention,  # noqa: E402,F401
                          report, traceability)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in ("--base", "--edited", "--new", "--out"):
        p.add_argument(name, required=True)
    p.add_argument("--report", help="write the Markdown report here (default: <out>/CARRY_FORWARD.md)")
    a = p.parse_args(argv)
    try:
        results = carry_forward(a.base, a.edited, a.new, a.out)
    except UsageError as exc:
        print("carry_forward: %s" % exc, file=sys.stderr)
        return 2
    text = report(results, a.base, a.edited, a.new, a.out)
    report_path = a.report or os.path.join(a.out, "CARRY_FORWARD.md")
    Path(report_path).write_text(text, encoding="utf-8")
    print(text)
    print("\nReport: %s" % report_path)
    return 1 if needs_attention(results) else 0


if __name__ == "__main__":
    sys.exit(main())
