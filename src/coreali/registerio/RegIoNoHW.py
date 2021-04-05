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

    def write_raw(self, address, data):
        """Write raw bytes 

        Args:
            address: start address in bytes
            data: array/list of bytes
        """
        if not self.mem is None:
            for i in range(len(data)):
                self.mem[address+i] = data[i]

    def read_raw(self, address, num_bytes):
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
