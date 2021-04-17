# coreali - Convenient Register Access Library
Generates Python code from a register model. This python code can the be used to access the registers of an FPGA, a MCU or another device which has a register map.
## Installation
Coreali can be installed with pip by executing the following command

    pip install -i https://test.pypi.org/simple/ coreali

## How to use
The typical use case for coreali is:
1. Make a register description of your system in [systemRDL](https://www.accellera.org/activities/working-groups/systemrdl) or any other supported format (ipxact) of the [systemrdl-compiler](https://github.com/SystemRDL/systemrdl-compiler)
2. Compile the register description with the [systemrdl-compiler](https://github.com/SystemRDL/systemrdl-compiler)
3. Generate the hierarchical register model class and objects with the **coreali.PythonExporter**
4. Access the registers of your FPGA device with **coreali.registerio**

## Quickstart - Logger example
1. Create a register description of your system or module
```systemRDL
mem log_mem {
    mementries = 64;
    memwidth = 8;
};

addrmap logger { 
	reg  {	
		desc = "Control register";
		field {sw = rw; hw = r;} ENABLE;
		field {sw = rw; hw = r;} TRIGGERED;
	} Ctrl;
	reg  {	
		desc = "Trigger configuration for channel 0 and 1";
		field {sw = rw; hw = r;} SW_TRIG;
		field {sw = rw; hw = r;} LEVEL[8];
	} Trig[2];
  	external log_mem LogMem[2];
};

```
1. Import dependencies and compile register model with systemrdl-compiler

```python
import sys
from systemrdl import RDLCompiler
import coreali 
import numpy as np
rdlc = RDLCompiler()
rdlc.compile_file("../systemrdl/logger.rdl")
root = rdlc.elaborate()
```

2. Generate hierarchical register model with the PythonExporter from coreali

```python
pythonExporter = coreali.PythonExporter()
pythonExporter.export(root, "generated_regmodel.py")
```

3. Create the register model object
```python
import generated_regmodel
rio = coreali.registerio.RegIoNoHW(np.zeros([256], np.uint8()))
logger = generated_regmodel.logger(root, rio)
```


In this step the rio register input/output obkect is created. This object handles the low level access. The RegIoNoHW class allows to access virtual registers without having a hardware at hand. The XXXXX example shows how to create your own RegIo class to access your own hardware.**`TODO`**

4. Use the generated register model
```python
logger.Ctrl.read()
logger.LogMem.write(0,[1,2,3])
logger.LogMem.read()
logger.LogMem[1].write(0,[11,12,13])
print(logger)
```
The registers can now be read and written by hierarchically accessing them. With code completion of your python IDE the registers can be accessed conveniently. 

When using the print function on a register, register node or address map all registers and field will be readout and printed as a string.

The full source code of this example can be found in
[examples/quickstart/](../blob/master/LICENSE)
