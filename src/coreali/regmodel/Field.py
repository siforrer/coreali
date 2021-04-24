from .Component import Component
import numpy as np

class Field(Component):
    """Field class representing a register field

    This class allows the read and write access to fields in a register.
    """
    def __init__(self, root, path, parent):
        Component.__init__(self, root, path, parent)
        self._parent = parent

    def _register_to_field_value(self, register_value):
        field_value = np.uint64(register_value*2**(-self.node.lsb))
        field_value = np.mod(field_value,np.uint64(2**(self.node.msb-self.node.lsb+1)))
        return field_value
    
    def _modify_register_value(self, register_value, field_value):
        mask = 2**(self.node.msb-self.node.lsb+1)-1
        mask = mask << self.node.lsb
        mask = np.uint64(mask)
        register_value = np.bitwise_and(np.uint64(register_value),np.invert(mask))
        register_value += field_value*np.uint64(2**self.node.lsb)
        return register_value
        
    def read(self):
        """Read field value

        Returns:
            np.uint64: Field value
        """
        return self._register_to_field_value(self._parent.read())

    def write(self, data):
        register_value = self._parent.read()
        register_value = self._modify_register_value(register_value, data)
        self._parent.write(register_value)

    def _tostr(self, indent, value):
        field_value = self._register_to_field_value(value)
        return self._format_string(indent, field_value)

    def _format_string(self, indent, value=None):
        formstr = " "*indent + "{:" + str(22-indent) + "}:"
        if value is None:
            ret = formstr.format(self.node.inst_name)
        elif isinstance(value, (list,np.ndarray)):
            formstr += " " + str(value)
            ret = formstr.format(self.node.inst_name)
            if len(ret) > 100:
                ret = ret[0:100] + " ..."
        else:
            formstr += " {:10d} = 0x{:0" + str(self.node.parent.size*2) + "x}"
            ret = formstr.format(self.node.inst_name, value, value)
        return ret