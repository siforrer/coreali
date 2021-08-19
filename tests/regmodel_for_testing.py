import os
import sys
from os.path import dirname
if not dirname(__file__) + "/../src/" in sys.path:
    sys.path.insert(0, dirname(__file__) + "/../src/")
from systemrdl import RDLCompiler, RDLCompileError

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
