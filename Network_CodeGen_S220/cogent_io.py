"""Output helpers for the code generators: fixed encoding and guaranteed stdout restore."""
import os
import sys

CODE_GEN_DIR = './CODE_GEN'


def open_output(file_name):
    if not os.path.exists(CODE_GEN_DIR):
        os.mkdir(CODE_GEN_DIR)
    f = open(CODE_GEN_DIR + '/' + file_name, 'w', encoding='latin-1')
    sys.stdout = f
    return f


def close_output(f):
    f.close()
    sys.stdout = sys.__stdout__
