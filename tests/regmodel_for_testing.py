import os
import sys
from os.path import dirname
if not dirname(__file__) + "/../src/" in sys.path:
    sys.path.insert(0, dirname(__file__) + "/../src/")
from systemrdl import RDLCompiler, RDLCompileError
from coreali import PythonExporter

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

pythonExporter = PythonExporter()
pythonExporter.source_files = input_files
pythonExporter.export(root, dirname(__file__) + "/generated/python/test_register_description.py")
if not dirname(__file__) + "/./generated/python/" in sys.path:
    sys.path.insert(0, dirname(__file__) + "/./generated/python/")
