# -*- coding: utf-8 -*-
"""Dump dbc_parser results as sorted JSON (oracle comparison of the parser)."""
from __future__ import print_function

import json
import os
import sys

APP_DIR = os.environ.get("COGENT_APP_DIR",
                         os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, APP_DIR)
from Dbc_Parser import dbc_parser  # noqa: E402


def dump(dbc, node):
    result = {"node_ok": dbc_parser(dbc, node).check__node(),
              "enums": dbc_parser(dbc, node).get_enum_values()}
    for msg_type in ("GenMsgILSupport", "ALL"):
        for direction in ("tx", "rx"):
            key = "%s/%s" % (msg_type, direction)
            result[key] = dbc_parser(dbc, node).get_msg_type(msg_type, direction)
    return result


if __name__ == "__main__":
    kwargs = {"encoding": "latin-1"} if sys.version_info[0] == 2 else {}
    print(json.dumps(dump(sys.argv[1], sys.argv[2]), sort_keys=True, indent=1, **kwargs))
