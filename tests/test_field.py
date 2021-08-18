import unittest
import numpy as np
from regmodel_for_testing import root
from coreali.registerio import RegIoNoHW
from test_register_description import test_register_description


class TestAccessableFieldNode(unittest.TestCase):

    def test_write_read(self):
        test_reg_desc = test_register_description(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint32)
        test_reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4.write(3)
        self.assertEqual(test_reg_desc.AnAddrmap.ARegWithFields.read(), 3*2**4)
        self.assertEqual(
            test_reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4.read(), 3)

        test_reg_desc.AnAddrmap.ARepeatedReg[0].VAL.write(1)
        test_reg_desc.AnAddrmap.ARepeatedReg[1].VAL.write(2)
        test_reg_desc.AnAddrmap.ARepeatedReg[2].VAL.write(3)

        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[0].read(), 1)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[1].read(), 2)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[2].read(), 3)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[0].VAL.read(), 1)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[1].VAL.read(), 2)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[2].VAL.read(), 3)


if __name__ == '__main__':
    unittest.main()
