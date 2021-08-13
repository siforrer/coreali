import numpy as np


class RegIo:
    """Base class for accessing registers

    This base class handles the low level access to memory locations.
    It provides some functions for word accesses. To implement a real 
    register access a new class must be derived and this new class must 
    implement the methods write_raw and read_raw. For an example of this 
    please see the RegIoNoHW class.
    """


    def read_words(self, address, word_size, address_stride=0,  num_words=1):
        """Read multiple words starting from address

        Args:
            address: start address in byte
            word_size: size of one word in byte
            address_stride: address increment for every word (usually the word_size)
            num_words: number of words that are read
        """
        assert False, "not implemented"

    def write_words(self, address, word_size, address_stride,  data):
        """Write multiple words starting from address

        Args:
            address: start address in byte
            word_size: size of one word in byte
            address_stride: address increment for every word (usually the word_size)
            data: array of words to be written
        """
        assert False, "not implemented"
        
    def write_words_masked(self,address, word_size, address_stride, data, mask):
        """Modify multiple words

        Args:
            address: start address in byte
            word_size: size of one word in byte
            address_stride: address increment for every word (usually the word_size)
            data: array of words to be written
            mask: array of mask words  
        """
        mask = np.uint64(mask)
        data = np.uint64(data)
        old_data = self.read_words(address, word_size, address_stride, len(data))
        new_data = np.bitwise_or(np.bitwise_and(old_data, np.bitwise_not(mask)), np.bitwise_and(data, mask))
        self.write_words(address, word_size, address_stride,new_data)
        
    def modify_words(self,address, word_size, address_stride, lsb, msb, data):
        """Modify multiple words

        Args:
            address: start address in byte
            word_size: size of one word in byte
            address_stride: address increment for every word (usually the word_size)
            data: array of words to be written
            mask: array of mask words  
        """
        mask = 2**(msb-lsb+1)-1
        mask = mask << lsb
        data = np.uint64(data)*2**lsb
        mask = np.repeat(np.uint64(mask),len(data))
        self.write_words_masked(address, word_size, address_stride, data, mask)
