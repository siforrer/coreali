import numpy as np
from .SelectableComponent import SelectableComponent
from .Selector import Selectable, Selector


class Memory(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)

    def _read(self, start_idx=0, num_elements=None):
        word_size = int(self.node.get_property('memwidth') / 8)
        return self._rio.read_words(self.node.absolute_address+start_idx*word_size, word_size, word_size, num_elements)

    def _prepare_read(self, selector, mementries, args):
        if len(args) == 0:
            start = 0
            stop = mementries
            step = 1
        elif len(args) == 3:
            start = args[0]
            stop = args[1]
            step = args[2]
        elif len(args) == 1:
            start = args[0]
            stop = start+1
            step = 1
        elif len(args) == 2:
            start = args[0]
            stop = args[1]
            step = 1
        selector.selected.append(slice(start, stop, step))
        flat_data = np.empty(selector.numel(), np.uint64)
        flat_len = selector.flat_len()
        return selector, flat_data, flat_len

    def read(self, *args):
        """Read content of a memory

           read() # Read entire memory

           read(stop) # Read first "stop" entries

           read(start, stop[, step])

        Args:
            stop: index until (not included) the data is readout, ,  defaults to mementries
            start: start index of readout,  defaults to 0
            step: step index of readout,  defaults to 1

        Returns:
            Array of values
        """
        word_size = int(self.node.get_property('memwidth') / 8)
        mementries = self.node.get_property('mementries')
        selector = Selector()
        self._construct_selector(selector.selected)
        arglist = []
        for x in args:
            arglist.append(x)
        selector, flat_data, flat_len = self._prepare_read(
            selector, mementries, arglist)

        for idx, (flat_idx, sel_idx) in enumerate(selector):
            self._set_current_idx(sel_idx[:-1])
            flat_data[flat_idx:flat_idx+flat_len] = self._rio.read_words(
                self.node.absolute_address+sel_idx[-1]*word_size, word_size*selector.selected[-1].step, word_size, flat_len)
        data = flat_data.reshape(selector.data_shape())
        return data

    def _prepare_write(start_idx, value, selector):
        data = np.uint64(value)
        if np.isscalar(data):
            data = np.uint64([data])
        selector.selected.append(slice(start_idx, start_idx+data.shape[-1], 1))
        flat_data = np.uint64(value).flatten()
        flat_len = selector.flat_len()
        return selector, flat_data, flat_len

    def write(self, start_idx, value):
        """Write to a memory location

        Args:
            start_idx : Start index where the value is written to
            value : single value or array of values
        """
        data = np.uint64(value)
        if np.isscalar(data):
            data = np.uint64([data])
        word_size = int(self.node.get_property('memwidth') / 8)
        selector = Selector()
        self._construct_selector(selector.selected)
        selector.selected.append(slice(start_idx, start_idx+data.shape[-1], 1))
        flat_data = np.uint64(value).flatten()
        flat_len = selector.flat_len()
        for idx, (flat_idx, sel_idx) in enumerate(selector):
            self._set_current_idx(sel_idx[:-1])
            self._rio.write_words(self.node.absolute_address+sel_idx[-1]*word_size, word_size *
                                  selector.selected[-1].step, word_size, flat_data[flat_idx:flat_idx+flat_len])

    def __str__(self):
        return self._tostr()

    def _tostr(self, indent=0):
        if not self._do_print:
            return ""
        mementries = self.node.get_property('mementries')
        value = self.read(0, min(mementries, 100))
        s = self._format_string(indent, value)
        return s
