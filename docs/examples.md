# Examples
## Quickstart - Logger example
Create a register description of your system or module
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
Import dependencies and compile register model with systemrdl-compiler

```python
import sys
from systemrdl import RDLCompiler
import coreali 
import numpy as np
rdlc = RDLCompiler()
rdlc.compile_file("../systemrdl/logger.rdl")
root = rdlc.elaborate()
```

Generate hierarchical register model with the PythonExporter from coreali

```python
pythonExporter = coreali.PythonExporter()
pythonExporter.export(root, "generated_regmodel.py")
```

Create the register model object
```python
import generated_regmodel
rio = coreali.registerio.RegIoNoHW(np.zeros([256], np.uint8()))
logger = generated_regmodel.logger(root, rio)
```


In this step the rio register input/output obkect is created. This object handles the low level access. The RegIoNoHW class allows to access virtual registers without having a hardware at hand. The XXXXX example shows how to create your own RegIo class to access your own hardware.**`TODO`**

Use the generated register model
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
[examples/quickstart/](https://github.com/siforrer/coreali/tree/develop/examples/quickstart)



## Create your customized RegIo class

## Access Intel FPGAs through JTAG
