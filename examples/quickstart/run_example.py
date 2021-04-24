""" Simple Example using coreali to access a register model. Needs no h^ardware"""

# Import dependencies and compile register model with systemrdl-compiler
from systemrdl import RDLCompiler
import coreali 
import numpy as np
import os
root = os.path.dirname(__file__)+"/"
rdlc = RDLCompiler()
rdlc.compile_file(root+"../systemrdl/logger.rdl")
root = rdlc.elaborate()

# Generate hierarchical register model 
pythonExporter = coreali.PythonExporter()
pythonExporter.export(root, "generated_regmodel.py")

# Create the generated register model object
import generated_regmodel
rio = coreali.registerio.RegIoNoHW(np.zeros([256], np.uint8()))
logger = generated_regmodel.logger(root, rio)

# Use the generated register model
logger.Ctrl.read()
logger.LogMem.write(0,[1,2,3])
logger.LogMem.read()
logger.LogMem[1].write(0,[11,12,13])
print(logger)
