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
                self.mem[address+i] = data[i]

    def _read_raw(self, address, num_bytes):
        """Read raw bytes

        Args:
            address: start address in bytes
            num_bytes: number of bytes to be read

        Returns:
            ndarray: array of read bytes
        """
        ret = np.empty([num_bytes], np.uint8)
        if not self.mem is None:
            for i in range(num_bytes):
                ret[i] = self.mem[address+i]
        return ret

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
            ret += raw_bytes[i]
        return np.uint64(ret)

    def _write_word(self, address, word_size, word):
        """Write a single word

        Args:
            address: address of register in byte
            word_size: size of word in byte
            word: word that is written to locoation with address
        """
        for i in range(word_size):
            self._write_raw(address+i, [np.mod(word, 256)])
            word /= 256

    def read_words(self, address, word_size, address_stride=0,  num_words=1):
        """Read multiple words starting from address

        Args:
            address: start address in byte
            address_stride: address increment for every word (usually the word_size)
            word_size: size of one word in byte
            num_words: number of words that are read
        """
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
        for idx, value in enumerate(data):
            self._write_word(address+idx*address_stride, word_size, value)