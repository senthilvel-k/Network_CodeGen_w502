"""List '/' and '/=' operator tokens (strings and comments excluded)."""
import sys
import tokenize

for path in sys.argv[1:]:
    with open(path, "rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type == tokenize.OP and tok.string in ("/", "/="):
                print(f"{path}:{tok.start[0]}:{tok.start[1] + 1}: {tok.line.strip()}")
