import numpy as np
import copy
from .Component import Component

class Selectable():
    def __init__(self, parent):
        self._parent = parent
        self._select = None
    
    def __getitem__(self, key):
        c = self._get_copy()
        c._select = key
        return c
    
    
    def _get_copy(self):
        c = copy.copy(self)        
        for child in self.__dict__.keys():
            if isinstance(self.__dict__[child], Selectable):
                if not child == "_parent":
                    c.__dict__[child] = self.__dict__[child]._get_copy()
                    c.__dict__[child]._parent = c
            elif isinstance(self.__dict__[child], Component):
                if not child == "_parent":
                    c.__dict__[child] = copy.copy(self.__dict__[child])
                    c.__dict__[child]._parent = c
        return c

    def _default_start(self):
        return 0
    
    def _default_stop(self):
        return 0
    
    def _default_step(self):
        return 1
    
    def _default_selection(self):
        return 0
    
    def _default_slice(self, slice_in=None):
        """
        Create a slice with default values or fill a slice with undefined values 
        that all values are defined
        """
        if slice_in is None:
            return slice(self._default_start(),self._default_stop(), self._default_step())
        start = self._select.start
        stop = self._select.stop
        step = self._select.step
        if start is None:
            start = self._default_start()
        if stop is None:
            stop = self._default_stop()
        if step is None:
            step = self._default_step()
        return slice(start,stop, step)
    
    def _get_selection(self):
        if self._select is None:
            return self._default_selection()      
        if isinstance(self._select, slice):
            self._select = self._default_slice(self._select)
        return self._select
    
    def _construct_selector(self, selector):
        selector.insert(0,self._get_selection())
        if not self._parent is None:
            self._parent._construct_selector(selector)


class Selector():
    
    def __init__(self,selected=None):
        if selected is None:
            selected = []
        self.selected = selected;
        
    def data_shape(self):
        dimension = []
        for _idx, val in enumerate(self.selected):
            if isinstance(val, slice):
                dimension.append(self.numel_of_slice(val))
        return dimension
    
    def numel_of_slice(self, s):
        return int((s.step+s.stop-s.start-1) / s.step)
    
    def idx_of_slice(self, s, i):
        return s.start+i*s.step

    def numel(self):
        ret = 1
        for n in self.data_shape():
            ret *= n
        return ret
    
    def flat_len(self):
        if isinstance(self.selected[-1],slice):
            return self.numel_of_slice(self.selected[-1])
        return 1
    
    def __iter__(self):
        tree_idx = np.empty(len(self.selected), int)
        slice_idx = []
        for i, val in enumerate(self.selected):
            if isinstance(val, slice):
                slice_idx.append(i)
            else:
                tree_idx[i] = val
        dim = self.data_shape()
        for flat_idx in range(0,self.numel(),self.flat_len()):
            data_idx = np.unravel_index(flat_idx,dim)
            for pos_in_data, pos_in_sel in enumerate(slice_idx):
                tree_idx[pos_in_sel] = self.idx_of_slice(self.selected[pos_in_sel], data_idx[pos_in_data])
            yield flat_idx, tree_idx
    
    def __str__(self):
        return "selected = " + str(self.selected) + ", data shape = " + str(self.data_shape())
    
        

