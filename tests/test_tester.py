import numpy as np
import unittest
import sys
sys.path.insert(0, "../src/")

from coreali.registerio import RegIoNoHW, Tester

class TestRegisterIoTester(unittest.TestCase):
    
    def test_successful (self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([40],np.uint8)        
        tester = Tester(rio)
        
        tester.test_all()

        tester.config.word_size = 2;
        tester.config.address_incr = 2;
        tester.test_all()
        
        tester.config.word_size = 4;
        tester.config.address_incr = 8;
        tester.test_all()

        tester.config.word_size = 1;
        tester.config.address_incr = 8;
        tester.test_all()
       
    def test_error(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
