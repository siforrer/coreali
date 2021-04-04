# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 22:11:56 2021

@author: sforr
"""

import numpy as np

class RegIo:
    
    def read_word(self, address, word_size):
        ret = np.uint64(0)
        raw_bytes = self.read_raw(address,word_size)
        for i in range(word_size-1,-1,-1):
            ret *= np.uint64(2**8)
            ret += raw_bytes[i]
        return np.uint64(ret)
    
    def write_word(self, address, word_size, word):
        for i in range(word_size):
            self.write_raw(address+i,[np.mod(word,256)])
            word /= 256
        
    def read_words(self, address, word_size, num_words):
        """ Read words starting from address

        Parameters
        ----------
        address
            address in bytes
        num_elements
            number of elements
        word_size
            number of bytes / word
        """
        ret = np.empty([num_words],np.uint64)
        for i in range(num_words):
            ret[i] = self.read_word(address+i*word_size, word_size)
        return ret

    def write_words(self, address, word_size, data):
        """Write words starting from address

        Parameters
        ----------
        address
            address in byte
        word_size
            Size of each word in bytes
        data
            array of words to be written starting from address

        """
        for idx, value in enumerate(data):
            self.write_word(address+idx*word_size, word_size, value)