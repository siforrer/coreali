import os
import sys
if not "../src/" in sys.path:
    sys.path.insert(0, "../src/")
from systemrdl import RDLCompiler, RDLCompileError
from coreali import PythonExporter

input_files = ["./test_register_description.rdl"]

if not os.path.exists("generated/python/"):
    os.makedirs("generated/python/")

rdlc = RDLCompiler()

try:
    for input_file in input_files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()
except RDLCompileError:
    sys.exit(1)

pythonExporter = PythonExporter()
pythonExporter.source_files = input_files
pythonExporter.export(root, "generated/python/test_register_description.py")
if not "./generated/python/" in sys.path:
    sys.path.insert(0, "./generated/python/")
