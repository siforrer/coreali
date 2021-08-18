import numpy as np


class Component:
    def __init__(self, root, path, parent):
        self._root = root
        self.node = root.find_by_path(path)
        self._parent = parent

    def _format_string(self, indent, value=None):
        formstr = " "*indent + "{:" + str(22-indent) + "}:"
        if value is None:
            ret = formstr.format(self.node.inst_name)
        elif isinstance(value, (list, np.ndarray)):
            formstr += " " + str(value)
            ret = formstr.format(self.node.inst_name)
            if len(ret) > 100:
                ret = ret[0:100] + " ..."
        else:
            formstr += " {:10d} = 0x{:0" + str(self.node.size*2) + "x}"
            ret = formstr.format(self.node.inst_name, value, value)
        return ret

    def help(self):
        for property_name in self.node.list_properties():
            print(property_name + ": " +
                  str(self.node.get_property(property_name)))
