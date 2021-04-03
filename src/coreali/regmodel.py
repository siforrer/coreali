import sys
import numpy as np
from systemrdl.node import AddrmapNode, FieldNode, MemNode, RegfileNode
from systemrdl import RDLCompiler, RDLCompileError
from .Selector import Selector, Selectable
import copy

        
class AccessableBaseNode:
    def __init__(self, root, path, parent):
        self._root = root
        self.node = root.find_by_path(path)
        self._parent = parent

    def _format_string(self, indent, value=None):
        formstr = " "*indent + "{:" + str(22-indent) + "}:"
        if value is None:
            ret = formstr.format(self.node.inst_name)
        elif isinstance(value, (list,np.ndarray)):
            formstr += " " + str(value)
            ret = formstr.format(self.node.inst_name)
            if len(ret) > 100:
                ret = ret[0:100] + " ..."
        else:
            formstr += " {:10d} = 0x{:08x}"
            ret = formstr.format(self.node.inst_name, value, value)
        return ret
    
    def help(self):        
        for property_name in self.node.list_properties():
            print(property_name + ": " + str(self.node.get_property(property_name)))


class AccessableFieldNode(AccessableBaseNode):
    def __init__(self, root, path, parent):
        AccessableBaseNode.__init__(self, root, path, parent)
        self._parent = parent

    def register_to_field_value(self, register_value):
        if isinstance(register_value, int):
            field_value = register_value >> self.node.lsb
            field_value = field_value % 2**(self.node.msb-self.node.lsb+1)
        else:
            field_value = register_value*2**(-self.node.lsb)
            field_value = np.mod(field_value,self.node.msb-self.node.lsb+1)
        return field_value

    def read(self):
        return self.register_to_field_value(self._parent.read())

    def write(self, data):
        mask = 2**(self.node.msb-self.node.lsb+1)-1
        mask = mask << self.node.lsb
        register_value = self._parent.read()
        register_value &= ~mask
        register_value += data << self.node.lsb
        self._parent.write(register_value)

    def _tostr(self, indent, value):
        field_value = self.register_to_field_value(value)
        return self._format_string(indent, field_value)


class AccessableNode(AccessableBaseNode, Selectable):
    def __init__(self, root, path, parent, rio):
        AccessableBaseNode.__init__(self, root, path, parent)
        Selectable.__init__(self, parent)
        self._rio = rio
        self._select = None


    def _current_range(self, select):
        start = 0
        stop = self.node.array_dimensions[0]
        step = 1
        if isinstance(select, slice):
            if not select.start is None:
                start = select.start
            if not select.stop is None:
                stop = select.stop
            if not select.step is None:
                step = select.step
        return range(start, stop, step)

    def _set_current_idx(self, selector):
        n = self.node
        for i in reversed(range(len(selector))):
            n.current_idx = [selector[i]]
            n = n.parent
            
    def _default_start(self):
        return 0
    
    def _default_stop(self):
        return self.node.array_dimensions[0] # TODO currently only 1d arrays are supported
    
    def _default_step(self):        
        return 1
    
    def _default_selection(self):
        if self.node.is_array:
            return self._default_slice()
        return 0
        
    def _read(self):
        if self.node.is_array:
            select = self.node.current_idx
            if isinstance(select, list):
                self.node.current_idx = select
                ret = self._rio.read(self.node.absolute_address)
            else:
                ret = []
                for i in self._current_range(select):
                    self.node.current_idx = [i]
                    ret.append(self._rio.read(self.node.absolute_address))
        else:
            ret = self._rio.read(self.node.absolute_address)
        return ret
    
    
    def read(self):
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() :
            self._set_current_idx(selector.selected)
            return self._rio.read(self.node.absolute_address)
        
        data = np.empty(selector.data_shape(), np.uint64);
        for flat_idx, sel_idx in enumerate(selector):
            self._set_current_idx(sel_idx[1])
            data[np.unravel_index(flat_idx,selector.data_shape())] = self._rio.read(self.node.absolute_address)
        return data

    def _write(self, value):
        if self.node.is_array:
            select = self.node.current_idx
            if isinstance(select, list):
                self.node.current_idx = select
                self._rio.write(self.node.absolute_address, value)
            else:
                start = select.start
                step = select.step
                if start is None:
                    start = 0
                if step is None:
                    step = 1
                if step == 1:
                    self.node.current_idx = [start]
                    self._rio.write(self.node.absolute_address, value)
                else:
                    node_idx = self._current_range(select)
                    for data_idx in range(len(node_idx)):
                        self.node.current_idx = [node_idx[data_idx]]
                        self._rio.write(
                            self.node.absolute_address, value[data_idx])
        else:
            self._rio.write(self.node.absolute_address, value)

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
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() : # single access
            self._set_current_idx(selector.selected)
            self._rio.write(self.node.absolute_address, value)
        else:
            for flat_idx, sel_idx in enumerate(selector):
                self._set_current_idx(sel_idx[1])
                self._rio.write(self.node.absolute_address,value[flat_idx])
            
        

    def __str__(self):
        return self._tostr()

    def _tostr(self, indent=0):
        if isinstance(self.node, (AddrmapNode, RegfileNode)):
            s = self._format_string(indent)
        else:
            value = self.read()
            s = self._format_string(indent, value)
        for child in self.node.children():
            if isinstance(child, (FieldNode)):
                tmp = AccessableFieldNode(
                    self._root, child.get_path(empty_array_suffix=""), self)
                s += "\n" + tmp._tostr(indent+2, value)
            elif isinstance(child, (MemNode)):
                tmp = AccessableMemNode(self._root, child.get_path(
                    empty_array_suffix=""), self, self._rio)
                s += "\n" + tmp._tostr(indent+2)
            else:
                tmp = AccessableNode(self._root, child.get_path(
                    empty_array_suffix=""), self, self._rio)
                s += "\n" + tmp._tostr(indent+2)
        return s


class AccessableMemNode(AccessableNode):
    def __init__(self, root, path, parent, rio):
        AccessableNode.__init__(self, root, path, parent, rio)

    def _read(self, start_idx=0, num_elements=None):
        word_size = int(self.node.get_property('memwidth') / 8)
        return self._rio.read(self.node.absolute_address+start_idx*word_size, num_elements, word_size)

    def _write(self, start_idx, value):
        word_size = int(self.node.get_property('memwidth') / 8)
        return self._rio.write(self.node.absolute_address+start_idx*word_size, value, word_size)

    def read(self, start_idx=0, num_elements=None):
        if num_elements is None:
            assert start_idx == 0
            num_elements = self.node.get_property('mementries')

        if self.node.is_array:
            if isinstance(self._select, int):
                self.node.current_idx = [self._select]
                ret = self._read(start_idx, num_elements)
            else:
                ret = []
                for i in self._current_range(self._select):
                    self.node.current_idx = [i]
                    ret.append(self._read(start_idx, num_elements))
            self._select = None
        else:
            ret = self._read(start_idx, num_elements)
        return ret

    def write(self, start_idx, value):
        if self.node.is_array:
            if isinstance(self._select, int):
                self.node.current_idx = [self._select]
                self._write(start_idx, value)
            else:
                for i in self._current_range(self._select):
                    self.node.current_idx = [i]
                    self._write(start_idx, value[i])
            self._select = None
        else:
            self._write(start_idx, value)

    def __str__(self):
        return self._tostr()
    
class AccessableTopNode(AccessableNode):
    def __init__(self, rdl_source_files, rio):
        # TODO check if the rdl and python files match
        rdlc = RDLCompiler()
        try:
            for input_file in rdl_source_files:
                rdlc.compile_file(input_file)
            root = rdlc.elaborate()
        except RDLCompileError:
            sys.exit(1)
        AccessableNode.__init__(self, root, root.top.get_path(), None, rio)
