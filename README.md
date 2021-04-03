# coreali - Convenient Register Access Library
Generates Python code from a register model. This python code can the be used to access the registers of an FPGA, a MCU or another device which has a register map.
## Installation
Coreali can be installed with pip by executing the following command

    pip install -i https://test.pypi.org/simple/ coreali

## How to use
The typical use case for coreali is:
1. Make a register description of your system in [systemRDL](https://www.accellera.org/activities/working-groups/systemrdl)
2. Compile the register description with the [systemrdl-compiler](https://github.com/SystemRDL/systemrdl-compiler)
3. Generate the hierarchical register model class and objects with the **coreali.PythonExporter**
4. Access the registers of your FPGA device with **coreali.registerio**

## Quickstart - I2C Example


Coreali is typically used with an existing register description. 

To have an example use case a systemRDL description of the I2C-Master Core from [opencores](https://opencores.org/projects/i2c) was 



