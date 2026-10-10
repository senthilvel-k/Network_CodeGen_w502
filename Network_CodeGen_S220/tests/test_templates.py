"""Templates render data safely (values embedded in scripts cannot end the script)."""
import json
import sys

from support import ROOT

sys.path.insert(0, str(ROOT))


def test_json_embedded_in_a_script_cannot_close_it():
    from back_end import script_json
    text = script_json({"name": "</script><script>alert(1)</script>"})
    assert "</script" not in text.lower()
    assert json.loads(text) == {"name": "</script><script>alert(1)</script>"}
