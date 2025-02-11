from abc import ABC, abstractmethod
import numpy as np


class Printer(ABC):

    def __init__(self):
        self.indentation = 0
        self.string = ""

    def indent(self):
        self.indentation += 1

    def outdent(self):
        self.indentation -= 1
        assert self.indentation >= 0

    @abstractmethod
    def print(self, value=None):
        pass


class StrPrinter(Printer):

    def print(self, name, value=None, value_size=None):
        self.string += self._format_string(self.indentation*2,
                                           name, value, value_size) + "\n"

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


class HtmlPrinter(Printer):
    def print2(self, name, value=None, value_size=None):
        self.string += f"""<tr style="text-align: left;">
                        <th style="text-align: left;"><span style="margin-left:{20*self.indentation}px">{name}</span></th>
                        <td>{value}</td>
                        <td>{value}</td>
                    </tr>"""

    def print(self, name, value=None, value_size=None):
        self.string += f"""<tr style="text-align: left;">
                        <th style="text-align: left;"><span style="margin-left:{20*self.indentation}px">{name}</span></th>"""
        match value:
            case None:
                self.string += f"<td></td><td></td>"
            case str() | list() | np.ndarray():
                self.string += f'<td colspan="2">{value}</td>'
            case _:
                hex_string = ("0x{:0" + str(value_size*2) + "x}").format(value)
                self.string += f"<td>{value}</td><td>{hex_string}</td>"
        self.string += "</tr>"

    def tostr(self):
        return f"""<table border="1" class="dataframe">
                    <tbody>{self.string}</tbody>
                </table>"""
