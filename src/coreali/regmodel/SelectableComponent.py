import numpy as np
from systemrdl.node import AddrmapNode, FieldNode, MemNode, RegfileNode
from .Component import Component
from .Field import Field
from .Selector import Selectable, Selector


class SelectableComponent(Component, Selectable):
    def __init__(self, root, node, parent, rio):
        Component.__init__(self, root, node, parent)
        Selectable.__init__(self, parent)
        self._rio = rio
        self._do_print = True

    def _set_current_idx(self, selector):
        n = self.node
        for i in reversed(range(len(selector))):
            n.current_idx = [selector[i]]
            n = n.parent

    def _default_start(self):
        return 0

    def _default_stop(self):
        # TODO currently only 1d arrays are supported
        return self.node.array_dimensions[0]

    def _default_step(self):
        return 1

    def _default_selection(self):
        if self.node.is_array:
            return self._default_slice()
        return 0

    def modify(self, lsb, msb, value):

        selector = Selector()
        self._construct_selector(selector.selected)
        if not selector.data_shape():
            self._set_current_idx(selector.selected)
            self._rio.modify_words(
                self.node.absolute_address, self.node.size, self.node.size, lsb, msb, [value])

    def read(self):
        selector = Selector()
        self._construct_selector(selector.selected)
        if not selector.data_shape():
            self._set_current_idx(selector.selected)
            return self._rio.read_words(self.node.absolute_address, self.node.size, self.node.size, 1)[0]

        flat_data = np.empty([selector.numel()], dtype=np.uint64)
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            self._set_current_idx(sel_idx)
            if selector.flat_len() > 1:
                array_stride = self.node.array_stride * \
                    selector.selected[-1].step
            else:
                array_stride = self.node.size
            flat_data[flat_idx:flat_idx+selector.flat_len()] = self._rio.read_words(
                self.node.absolute_address, self.node.size, array_stride, selector.flat_len())
        data = flat_data.reshape(selector.data_shape())
        return data

    def write(self, value):
        """Write to register

            Use case examples based on the example register description
            Use case 1: Write 1 to 1
                Write single value to a single register
                test_reg_desc.AnAddrmap.ARegWithFields.write(100)

            Use case 2: Write n values without indexing
                Write n values to an array of register
                test_reg_desc.AnAddrmap.TenRegs.write([1,2,3,4])
                This will write 1 to TenRegs[0], 2 to TenRegs[1], 3 to TenRegs[2] and , 4 to TenRegs[3]

            Use case 2: Write n values with indexing
                test_reg_desc.AnAddrmap.TenRegs[0:4].write([1,2,3,4])
                This will write 1 to TenRegs[0], 2 to TenRegs[1], 3 to TenRegs[2] and , 4 to TenRegs[3]
                The indexed data shape must match the shate of the written values

        Args:
            value : Can be int for writing a single value or a list/numpy.array for writing multiple values to a register array
        """
        selector = Selector()
        self._construct_selector(selector.selected)
        if not selector.data_shape():  # single access
            self._set_current_idx(selector.selected)
            self._rio.write_words(self.node.absolute_address,
                                  self.node.size, self.node.size, [value])
        else:
            flat_data = np.uint64(value).flatten()
            for _idx, (flat_idx, sel_idx) in enumerate(selector):
                self._set_current_idx(sel_idx)
                if selector.flat_len() > 1:
                    array_stride = self.node.array_stride * \
                        selector.selected[-1].step
                else:
                    array_stride = self.node.size
                self._rio.write_words(self.node.absolute_address, self.node.size,
                                      array_stride, flat_data[flat_idx:flat_idx+selector.flat_len()])

    def __str__(self):
        return self._tostr()

    def _tostr(self, indent=0):
        if not self._do_print:
            return ""
        if isinstance(self.node, (AddrmapNode, RegfileNode)):
            s = self._format_string(indent)
        else:
            if self._read_has_side_effect():
                return self._format_string(indent, "(SIDE EFFECTS - NOT READ)")
            value = self.read()
            s = self._format_string(indent, value)
            
        for child in self.__dict__.keys():
            if not child == "_parent":
                if isinstance(self.__dict__[child], Field):
                    s += "\n" + self.__dict__[child]._tostr(indent+2,value)        
                elif isinstance(self.__dict__[child], Component):
                    s += "\n" + self.__dict__[child]._tostr(indent+2)

        return s
