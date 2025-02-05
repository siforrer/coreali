import numpy as np
from .Printer import StrPrinter

class Component:
    def __init__(self, root, node, parent):
        self._root = root
        self.node = node
        self._parent = parent
        self._update_attr()

    def _update_attr(self):
        pass

    def _print(self, printer, value=None):
        printer.print(self.node.inst_name, value, self.node.size)

    def help(self):
        for property_name in self.node.list_properties():
            print(property_name + ": " +
                  str(self.node.get_property(property_name)))
