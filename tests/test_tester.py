from coreali.registerio import RegIoNoHW, Tester
import numpy as np

def test_successful():
    rio = RegIoNoHW()
    rio.mem = np.zeros([1024], np.uint32)
    tester = Tester(rio)

    tester.test_all()

    for log2_word_size in range(5):
        tester.config.word_size = 2**log2_word_size
        tester.config.testmem_address = 16
        for log2_address_incr in range(log2_word_size, 5):
            tester.config.address_incr = 2**log2_address_incr
            tester.test_all()

def test_performance():
    rio = RegIoNoHW()
    rio.mem = np.zeros([40], np.uint32)
    tester = Tester(rio)
    tester.config.testmem_size = len(rio.mem)*rio.mem.itemsize
    tester.test_performance()

