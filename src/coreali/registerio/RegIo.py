import numpy as np


class RegIo:
    """Base class for accessing registers

    This base class handles the low level access to memory locations.
    It provides some functions for word accesses. To implement a real 
    register access a new class must be derived and this new class must 
    implement the methods write_raw and read_raw. For an example of this 
    please see the RegIoNoHW class.
    """


    def read_words(self, address, word_size, address_stride=0,  num_words=1): # TODO swap position of word_size with address_stride
        """Read multiple words starting from address

        Args:
            address: start address in byte
            address_stride: address increment for every word (usually the word_size)
            word_size: size of one word in byte
            num_words: number of words that are read
        """
        assert False, "not implemented"

    def write_words(self, address, word_size, address_stride,  data):
        """Write multiple words starting from address

        Args:
            address: start address in byte
            address_stride: address increment for every word (usually the word_size)
            word_size: size of one word in byte
            data: array of words to be written
        """
        assert False, "not implemented"
