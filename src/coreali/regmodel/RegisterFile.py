from .SelectableComponent import SelectableComponent
from .Component import Component

class RegisterFile(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)
        
    def _tostr(self, indent=0):
        if not self._do_print:
            return ""
        s = self._format_string(indent)    
            
        for child in self.__dict__.keys():
            if not child == "_parent":
                if isinstance(self.__dict__[child], Component):
                    s += "\n" + self.__dict__[child]._tostr(indent+2)

        return s