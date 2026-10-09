"""Output helpers for the code generators: fixed encoding and guaranteed stdout restore."""
import os
import sys

CODE_GEN_DIR = './CODE_GEN'
current_output = None  # name of the file a generator is writing (used in error messages)
_current_file = None


def open_output(file_name):
    global current_output, _current_file
    if not os.path.exists(CODE_GEN_DIR):
        os.mkdir(CODE_GEN_DIR)
    current_output = file_name
    f = open(CODE_GEN_DIR + '/' + file_name, 'w', encoding='latin-1')
    _current_file = f
    sys.stdout = f
    return f


def close_output(f):
    global current_output, _current_file
    f.close()
    sys.stdout = sys.__stdout__
    current_output = None
    _current_file = None


def abort_output():
    """Close the file a failed generator left open (Windows cannot delete open files)."""
    global _current_file
    if _current_file is not None and not _current_file.closed:
        _current_file.close()
    _current_file = None
