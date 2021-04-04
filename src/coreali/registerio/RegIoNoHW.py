# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 22:17:09 2021

@author: sforr
"""

import numpy as np
from  coreali.registerio import RegIo

class RegIoNoHW(RegIo):
    """Register IO class that does not need any hardware to access"""

    def __init__(self, offset=0, mem=None):
        self.offset = offset
        self.mem = mem
        self.verbose = False


    def write_raw(self, address, data):
        if not self.mem is None:
            for i in range(len(data)):
                self.mem[address+i] = data[i]

    def read_raw(self, address, num_bytes):
        ret = np.empty([num_bytes], np.uint8)
        if not self.mem is None:
            for i in range(num_bytes):
                ret[i] = self.mem[address+i]
        return ret
                