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
            if isinstance(self, AccessableFieldNode):
                formstr += " {:10d} = 0x{:0" + str(self.node.parent.size*2) + "x}"
            else:               
                formstr += " {:10d} = 0x{:0" + str(self.node.size*2) + "x}"
            ret = formstr.format(self.node.inst_name, value, value)
        return ret
    
    def help(self):        
        for property_name in self.node.list_properties():
            print(property_name + ": " + str(self.node.get_property(property_name)))


class AccessableFieldNode(AccessableBaseNode):
    def __init__(self, root, path, parent):
        AccessableBaseNode.__init__(self, root, path, parent)
        self._parent = parent

    def _register_to_field_value(self, register_value):
        field_value = np.uint64(register_value*2**(-self.node.lsb))
        field_value = np.mod(field_value,np.uint64(2**(self.node.msb-self.node.lsb+1)))
        return field_value
    
    def _modify_register_value(self, register_value, field_value):
        mask = 2**(self.node.msb-self.node.lsb+1)-1
        mask = mask << self.node.lsb
        mask = np.uint64(mask)
        register_value = np.bitwise_and(np.uint64(register_value),np.invert(mask))
        register_value += field_value*np.uint64(2**self.node.lsb)
        return register_value
        
    def read(self):
        return self._register_to_field_value(self._parent.read())

    def write(self, data):
        register_value = self._parent.read()
        register_value = self._modify_register_value(register_value, data)
        self._parent.write(register_value)

    def _tostr(self, indent, value):
        field_value = self._register_to_field_value(value)
        return self._format_string(indent, field_value)

class AccessableNode(AccessableBaseNode, Selectable):
    def __init__(self, root, path, parent, rio):
        AccessableBaseNode.__init__(self, root, path, parent)
        Selectable.__init__(self, parent)
        self._rio = rio
        self._select = None

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
                
    def read(self):
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() :
            self._set_current_idx(selector.selected)
            return self._rio.read_word(self.node.absolute_address, self.node.size)
        
        flat_data = np.empty([selector.numel()],dtype=np.uint64)  
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            self._set_current_idx(sel_idx)
            flat_data[flat_idx:flat_idx+selector.flat_len()] = self._rio.read_words(self.node.absolute_address, self.node.array_stride*selector.selected[-1].step, self.node.size, selector.flat_len())
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
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() : # single access
            self._set_current_idx(selector.selected)
            self._rio.write_word(self.node.absolute_address, self.node.size, value)
        else:
            flat_data = np.uint64(value).flatten()
            for _idx, (flat_idx, sel_idx) in enumerate(selector):
                self._set_current_idx(sel_idx)
                self._rio.write_words(self.node.absolute_address, self.node.array_stride*selector.selected[-1].step, self.node.size, flat_data[flat_idx:flat_idx+selector.flat_len()])
            
        

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
        return self._rio.read_words(self.node.absolute_address+start_idx*word_size, word_size, word_size, num_elements)

    def _write(self, start_idx, value):
        word_size = int(self.node.get_property('memwidth') / 8)
        if isinstance(value, (list,np.ndarray)):
            self._rio.write_words(self.node.absolute_address+start_idx*word_size, word_size, word_size, value)
        else: 
            self._rio.write_word(self.node.absolute_address+start_idx*word_size, word_size, word_size, value)
            
    def read(self, start_idx=0, num_elements=None):
        word_size = int(self.node.get_property('memwidth') / 8)
        if num_elements is None:
            assert start_idx == 0, "start_idx must be 0 when num_elements is not specified"
            num_elements = int(self.node.get_property('mementries'))
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() :
            self._set_current_idx(selector.selected)
            return self._read(start_idx, num_elements)

        selector.selected.append(slice(start_idx,num_elements,1))
        flat_data = np.empty(selector.numel(), np.uint64)
        flat_len = selector.flat_len()
        for idx,(flat_idx, sel_idx) in enumerate(selector):
            self._set_current_idx(sel_idx[:-1])
            flat_data[flat_idx:flat_idx+flat_len] = self._rio.read_words(self.node.absolute_address, word_size*selector.selected[-1].step, word_size, flat_len)
        data = flat_data.reshape(selector.data_shape())
        return data

    def write(self, start_idx, value):
        data = np.uint64(value)
        word_size = int(self.node.get_property('memwidth') / 8)
        selector = Selector();
        self._construct_selector(selector.selected)
        if not selector.data_shape() : # single access
            self._set_current_idx(selector.selected)
            self._write(start_idx, data)
        else:
            selector.selected.append(slice(start_idx,start_idx+data.shape[-1],1))
            flat_data = np.uint64(value).flatten();
            flat_len = selector.flat_len()
            for idx,(flat_idx, sel_idx) in enumerate(selector):
                self._set_current_idx(sel_idx[:-1])
                self._rio.write_words(self.node.absolute_address, word_size*selector.selected[-1].step, word_size, flat_data[flat_idx:flat_idx+flat_len])

    def __str__(self):
        return self._tostr()
    
class AccessableTopNode(AccessableNode):
    def __init__(self, root, rio):
        AccessableNode.__init__(self, root, root.top.get_path(), None, rio)
