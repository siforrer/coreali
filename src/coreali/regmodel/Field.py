from .Component import Component
import numpy as np


class Field(Component):
    """Field class representing a register field

    This class allows the read and write access to fields in a register.
    """

    def __init__(self, root, node, parent, rio):
        Component.__init__(self, root, node, parent)

    def _update_attr(self):
        """
            Update attributes that object has a read/write function only
            if the field itself is read/writeable
        """
        if self.node.is_sw_writable:
            setattr(self, "write", self._write)
        if self.node.is_sw_readable:
            setattr(self, "read", self._read)

    def _register_to_field_value(self, register_value):
        field_value = np.uint64(register_value*2**(-self.node.lsb))
        field_value = np.mod(field_value, np.uint64(
            2**(self.node.msb-self.node.lsb+1)))
        return field_value

    def _read(self):
        """Read field value

        Returns:
            np.uint64: Field value
        """
        return self._register_to_field_value(self._parent.read())

    def _write(self, field_value):
        """Write field value

        """
        self._parent.modify(self.node.lsb, self.node.msb, field_value)

    def _tostr(self, indent, value):
        field_value = self._register_to_field_value(value)
        return self._format_string(indent, field_value)

    def _format_string(self, indent, value=None):
        formstr = " "*indent + "{:" + str(22-indent) + "}:"
        if value is None or isinstance(value, (list, np.ndarray)):
            ret = Component._format_string(self, indent, value)
        else:
            formstr += " {:10d} = 0x{:0" + str(self.node.parent.size*2) + "x}"
            ret = formstr.format(self.node.inst_name, value, value)
        return ret
