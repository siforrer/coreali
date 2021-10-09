from .SelectableComponent import SelectableComponent
from .Field import Field

class Register(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)
        
    def _read_has_side_effect(self):
        for child in self.node.children():
            if "onread" in child.list_properties():
                return True
        return False
    
    def _tostr(self, indent=0):
        if not self._do_print:
            return ""
        if self._read_has_side_effect():
            return self._format_string(indent, "(SIDE EFFECTS - NOT READ)")
        if self.node.is_array and self.node.array_dimensions[0] > 50:
            value = self[:50].read()
        else:
            value = self.read()
        s = self._format_string(indent, value)
        
        for child in self.__dict__.keys():
            if not child == "_parent":
                if isinstance(self.__dict__[child], Field):
                    s += "\n" + self.__dict__[child]._tostr(indent+2,value)   

        return s