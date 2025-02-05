from .Printer import StrPrinter
from .SelectableComponent import SelectableComponent
from .Component import Component

class RegisterFile(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)
        
    def _print(self, printer):
        if not self._do_print:
            return ""

        SelectableComponent._print(self, printer)

        printer.indent()
        for child in self.__dict__.keys():
            if not child == "_parent":
                if isinstance(self.__dict__[child], Component):
                    self.__dict__[child]._print(printer)
        printer.outdent()
