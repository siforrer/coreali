
import sys
from systemrdl import RDLCompiler
from coreali import PythonExporter
from coreali.registerio import RegIoNoHW

# Compile register model with systemrdl-compiler
rdlc = RDLCompiler()
rdlc.compile_file("../systemrdl/i2c_master_core.rdl")
root = rdlc.elaborate()

# Generate hierarchical register model 
pythonExporter = PythonExporter()
pythonExporter.source_files = ["../systemrdl/i2c_master_core.rdl"]
pythonExporter.export(root, "generated_regmodel.py")
sys.path.insert(0, "generated/python/")

# Use the generated register model
import generated_regmodel
i2c = generated_regmodel.i2c_master_core(root, RegIoNoHW())

print(i2c)

i2c.PRERlo.read()