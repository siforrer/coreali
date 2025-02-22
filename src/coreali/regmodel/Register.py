from .SelectableComponent import SelectableComponent
from .Field import Field


class Register(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)

    def _update_attr(self):
        if self.node.has_sw_writable:
            setattr(self, "write", self._write)
        if self.node.has_sw_readable:
            setattr(self, "read", self._read)

    def _read_has_side_effect(self):
        for child in self.node.children():
            if "onread" in child.list_properties():
                return True
        return False

    def _print(self, printer):
        if not self._do_print:
            return
        if self._read_has_side_effect():
            printer.print(self.node.inst_name, "(SIDE EFFECTS - NOT READ)")
            return
        if not self.node.has_sw_readable:
            printer.print(self.node.inst_name, "(NOT READABLE)")
            return
        if self.node.is_array and self.node.array_dimensions[0] > 50:
            value = self[:50].read()
        else:
            value = self.read()
        printer.print(self.node.inst_name, value, self.node.size)

        printer.indent()
        for child in self.__dict__.keys():
            if not child == "_parent":
                if isinstance(self.__dict__[child], Field):
                    self.__dict__[child]._print(printer, value)
        printer.outdent()
