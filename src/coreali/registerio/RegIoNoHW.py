import numpy as np
from coreali.registerio import RegIo


class RegIoNoHW(RegIo):
    """Register IO class that does not need any hardware to access
    This class is intended for testing and demonstration purposes.
    """

    def __init__(self, mem=None):
        """ Create a RegIo object which does not access any hardware

        Args:
            mem (optional): Array that is accessible with []. Defaults to None.
        """
        self.mem = mem
        self.verbose = False

    def _write_raw(self, address, data):
        """Write raw bytes 

        Args:
            address: start address in bytes
            data: array/list of bytes
        """
        if not self.mem is None:
            for i in range(len(data)):
                self.mem[int(address/self.mem.itemsize)+i] = data[i]

    def _read_raw(self, address, num_bytes):
        """Read raw bytes

        Args:
            address: start address in bytes
            num_bytes: number of bytes to be read

        Returns:
            ndarray: array of read bytes
        """
        return self.mem.tobytes()[address:address+num_bytes]

    def _read_word(self, address, word_size):
        """Read a single word

        Args:
            address: address of register in byte
            word_size: size of word in byte

        Returns:
            np.uint64: value of word at address
        """
        ret = np.uint64(0)
        raw_bytes = self._read_raw(address, word_size)
        for i in range(word_size-1, -1, -1):
            ret *= np.uint64(2**8)
            ret += np.uint64(raw_bytes[i])
        return ret

    def _write_word(self, address, word_size, word):
        """Write a single word

        Args:
            address: address of register in byte
            word_size: size of word in byte
            word: word that is written to locoation with address
        """
        if word_size < self.mem.itemsize:
            aligned_address = int(address/self.mem.itemsize)*self.mem.itemsize
            data = (word % 2**(8*word_size))*2**(8*(address-aligned_address))
            mask = (2**(8*word_size)-1)*2**(8*(address-aligned_address))
            self.write_words_masked(
                aligned_address, self.mem.itemsize, self.mem.itemsize, [data], mask)
        else:
            for i in range(int(word_size/self.mem.itemsize)):
                self._write_raw(address+i*self.mem.itemsize,
                                [np.mod(word, 2**(self.mem.itemsize*8))])
                word = int(word/2**(8*self.mem.itemsize))

    def _is_native_access(self, address, word_size, address_stride,  num_words):
        return word_size == self.mem.itemsize and (address % word_size) == 0

    def _prepare_native_access(self, address, word_size, address_stride,  num_words):
        start = int(address/word_size)
        if num_words > 1:
            step = int(address_stride/word_size)
        else:
            step = 1
        stop = start + num_words*step
        return start, stop, step

    def read_words(self, address, word_size, address_stride=0,  num_words=1):
        """Read multiple words starting from address

        Args:
            address: start address in byte
            address_stride: address increment for every word (usually the word_size)
            word_size: size of one word in byte
            num_words: number of words that are read
        """
        if self._is_native_access(address, word_size, address_stride,  num_words):
            start, stop, step = self._prepare_native_access(
                address, word_size, address_stride,  num_words)
            return self.mem[start:stop:step].astype(np.uint64)
        ret = np.empty([num_words], np.uint64)
        for i in range(num_words):
            ret[i] = self._read_word(address+i*address_stride, word_size)
        return ret

    def write_words(self, address, word_size, address_stride, data):
        """Write multiple words starting from address

        Args:
            address: start address in byte
            address_stride: address increment for every word (usually the word_size)
            word_size: size of one word in byte
            data: array of words to be written
        """
        num_words = len(data)
        if self._is_native_access(address, word_size, address_stride,  num_words):
            start, stop, step = self._prepare_native_access(
                address, word_size, address_stride,  num_words)
            self.mem[start:stop:step] = data
            return
        for idx, value in enumerate(data):
            self._write_word(address+idx*address_stride, word_size, value)
