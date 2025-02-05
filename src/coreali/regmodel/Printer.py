from abc import ABC, abstractmethod
import numpy as np


class Printer(ABC):
    @abstractmethod
    def print(self, value=None):
        pass


class StrPrinter(Printer):
    def __init__(self):
        self.indentation = 0
        self.string = ""

    def print(self, name, value=None, value_size=None):
        self.string += self._format_string(self.indentation*2,
                                           name, value, value_size) + "\n"

    def indent(self):
        self.indentation += 1

    def outdent(self):
        self.indentation -= 1
        assert self.indentation >= 0

    def tostr(self):
        return self.string[:-1]

    def _format_string(self, indent, inst_name, value=None, value_size=None):
        formstr = " "*indent + "{:" + str(22-indent) + "}:"
        if value is None:
            ret = formstr.format(inst_name)
        elif isinstance(value, (str)):
            formstr += " {:s}"
            ret = formstr.format(inst_name, value)
        elif isinstance(value, (list, np.ndarray)):
            formstr += " " + str(value)
            ret = formstr.format(inst_name)
            if ret.find('\n') >= 0:
                ret = ret[0:ret.find('\n')] + " ..."
            if len(ret) > 100:
                ret = ret[0:100] + " ..."
        else:
            formstr += " {:10d} = 0x{:0" + str(value_size*2) + "x}"
            ret = formstr.format(inst_name, value, value)
        return ret
