import pytest
import os
import sys
from os.path import dirname
if not dirname(__file__) + "/../src/" in sys.path:
    sys.path.insert(0, dirname(__file__) + "/../src/")
from systemrdl import RDLCompiler, RDLCompileError
from coreali import RegisterModel
from coreali.registerio import RegIoNoHW
import numpy as np


@pytest.fixture(scope="module")
def root():
    input_files = [dirname(__file__) + "/test_register_description.rdl"]

    if not os.path.exists(dirname(__file__) + "/generated/python/"):
        os.makedirs(dirname(__file__) + "/generated/python/")

    rdlc = RDLCompiler()

    try:
        for input_file in input_files:
            rdlc.compile_file(input_file)
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)
    return root


@pytest.fixture(scope="module")
def reg_desc(root):
    reg_desc = RegisterModel(root, RegIoNoHW())
    reg_desc._rio.mem = np.zeros([reg_desc.node.size], np.uint8)
    return reg_desc