import numpy as np


class RegIo:
    """Base class for accessing registers

    This base class handles the low level access to memory locations.
    It provides some functions for word accesses. To implement a real 
    register access a new class must be derived and this new class must 
    implement the methods write_raw and read_raw. For an example of this 
    please see the RegIoNoHW class.
    """

    def read_word(self, address, word_size):
        """Read a single word

        Args:
            address: address of register in byte
            word_size: size of word in byte

        Returns:
            np.uint64: value of word at address
        """
        ret = np.uint64(0)
        raw_bytes = self.read_raw(address, word_size)
        for i in range(word_size-1, -1, -1):
            ret *= np.uint64(2**8)
            ret += raw_bytes[i]
        return np.uint64(ret)

    def write_word(self, address, word_size, word):
        """Write a single word

        Args:
            address: address of register in byte
            word_size: size of word in byte
            word: word that is written to locoation with address
        """
        for i in range(word_size):
            self.write_raw(address+i, [np.mod(word, 256)])
            word /= 256

    def read_words(self, address, address_stride, word_size, num_words):
        """Read words starting from address

        Args:
            address: address of register in byte
            word_size: size of one word in byte
            num_words: number of words that are read
        """
        ret = np.empty([num_words], np.uint64)
        for i in range(num_words):
            ret[i] = self.read_word(address+i*address_stride, word_size)
        return ret

    def write_words(self, address, address_stride, word_size, data):
        """Write words starting from address

        Args:
            address: address of register in byte
            word_size: size of one word in byte
            data: array of words to be written starting from address
        """
        for idx, value in enumerate(data):
            self.write_word(address+idx*address_stride, word_size, value)
