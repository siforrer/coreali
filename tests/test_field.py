import unittest
import numpy as np
from regmodel_for_testing import root
from coreali.registerio import RegIoNoHW
from test_register_description import test_register_description

class TestAccessableFieldNode(unittest.TestCase):
    def test_modify_register_value(self):
        test_reg_desc = test_register_description(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.empty([test_reg_desc.node.size], np.uint8)   
        
        field = test_reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4
        self.assertEqual(field._modify_register_value(np.uint64(0),np.uint64(12)), 12*2**4)
        field_value = field._register_to_field_value(np.uint64(22))
        self.assertTrue(isinstance(field_value, np.uint64))
        
    
if __name__ == '__main__':
    unittest.main()
