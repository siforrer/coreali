import time
import sys
import unittest
import numpy as np
from io import StringIO
from regmodel_for_testing import root
from coreali.registerio import RegIoNoHW
from coreali.regmodel import Selector
from coreali import RegisterModel


class TestUseCases(unittest.TestCase):
    """
    Test common use cases
    """

    def test_writeread(self):
        """
        Test that the write and read functions write to the right location
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)

        test_reg_desc.AnAddrmap.AnotherRegAt20.write(0x12345678)
        test_reg_desc.AnotherAddrmap.AnotherRegAt20.write(0x87654321)

        self.assertEqual(
            test_reg_desc.AnAddrmap.AnotherRegAt20.read(), 0x12345678)
        self.assertEqual(
            test_reg_desc.AnAddrmap.AnotherRegAt20.VAL.read(), 0x12345678)
        self.assertEqual(test_reg_desc._rio.mem[0x20], 0x78)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.AnotherRegAt20.read(), 0x87654321)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.AnotherRegAt20.VAL.read(), 0x87654321)
        self.assertEqual(test_reg_desc._rio.mem[0x120], 0x21)

        test_reg_desc.AnotherAddrmap.ARegWithFields.FIELD13DOWNTO4.write(3)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARegWithFields.FIELD13DOWNTO4.read(), 3)

    def test_arrays(self):
        """
        Test the accessibility of arrays through the __get_item__ or [] method
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)
        test_reg_desc._rio.verbose = False

        # Elementwise access
        test_reg_desc.AnAddrmap.ARepeatedReg[0].write(11)
        test_reg_desc.AnAddrmap.ARepeatedReg[1].write(12)
        test_reg_desc.AnAddrmap.ARepeatedReg[2].write(13)
        test_reg_desc.AnotherAddrmap.ARepeatedReg[0].write(1)
        test_reg_desc.AnotherAddrmap.ARepeatedReg[1].write(2)
        test_reg_desc.AnotherAddrmap.ARepeatedReg[2].write(3)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[0].read(), 11)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[1].read(), 12)
        self.assertEqual(test_reg_desc.AnAddrmap.ARepeatedReg[2].read(), 13)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg[0].read(), 1)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg[1].read(), 2)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg[2].read(), 3)
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.ARepeatedReg[0:3].read(), [1, 2, 3]))
        self.assertTrue(
            np.array_equal(test_reg_desc.AnAddrmap.ARepeatedReg[0:3].read(), [11, 12, 13]))

        # Read and write back test
        test_reg_desc.AnotherAddrmap.ARepeatedReg.write(
            test_reg_desc.AnotherAddrmap.ARepeatedReg[0:3].read())
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.ARepeatedReg.read(), [1, 2, 3]))

        # Write starting from index
        test_reg_desc.AnotherAddrmap.ARepeatedReg[1:].write([4, 5])
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.ARepeatedReg.read(), [1, 4, 5]))

        # Write and read a slice
        test_reg_desc.AnotherAddrmap.TenRegs[4:7].write([4, 5, 6])
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.TenRegs.read(), [
                0, 0, 0, 0, 4, 5, 6, 0, 0, 0]))
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.TenRegs[2:6].read(), [0, 0, 4, 5]))
        test_reg_desc.AnotherAddrmap.TenRegs.write([0]*10)
        test_reg_desc.AnotherAddrmap.TenRegs[2:7:2].write([2, 4, 6])
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.TenRegs.read(), [
                0, 0, 2, 0, 4, 0, 6, 0, 0, 0]))
        self.assertTrue(
            np.array_equal(test_reg_desc.AnotherAddrmap.TenRegs[2:7:2].read(), [2, 4, 6]))

        test_reg_desc.AnAddrmap.AnotherRegfile[0].AReg.write(1111)
        test_reg_desc.AnAddrmap.AnotherRegfile[1].AReg.write(2222)
        self.assertTrue(
            np.array_equal(test_reg_desc.AnAddrmap.AnotherRegfile.AReg.read(), [1111, 2222]))

        test_reg_desc.AnAddrmap.AnotherRegfile.AnotherReg.write([1, 2])
        self.assertEqual(
            test_reg_desc.AnAddrmap.AnotherRegfile[0].AnotherReg.read(), 1)
        self.assertEqual(
            test_reg_desc.AnAddrmap.AnotherRegfile[1].AnotherReg.read(), 2)

    def test_arrays_of_array(self):
        """
        Test the accessibility of arrays through the __get_item__ or [] method
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)

        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[0].write(1)
        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[1].write(2)
        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[2].write(3)
        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[3].write(4)
        test_reg_desc.AnAddrmap.ARegfile[1].ARegInARegFile[0].write(11)
        test_reg_desc.AnAddrmap.ARegfile[1].ARegInARegFile[1].write(12)
        test_reg_desc.AnAddrmap.ARegfile[1].ARegInARegFile[2].write(13)
        test_reg_desc.AnAddrmap.ARegfile[1].ARegInARegFile[3].write(14)
        self.assertTrue(
            np.array_equal(test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile.read(), [1, 2, 3, 4]))
        self.assertTrue(
            np.array_equal(test_reg_desc.AnAddrmap.ARegfile[1].ARegInARegFile.read(), [11, 12, 13, 14]))

    def test_mem(self):
        """
        Test the accessibility of memories and arrays of memories
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)

        self.assertTrue(
            np.array_equal(test_reg_desc.Mem64x32.read(), [0]*64))

        test_reg_desc.Mem64x32.write(0, list(range(0, 64, 1)))
        self.assertTrue(
            np.array_equal(list(range(0, 64, 1)),
                           test_reg_desc._rio.read_words(0x800, 4, 4, 64)))

        self.assertTrue(
            np.array_equal(test_reg_desc.Mem64x32.read(), list(range(0, 64, 1))))

        self.assertTrue(
            np.array_equal(test_reg_desc.Mem64x32.read(10, 40), list(range(10, 40, 1))))

        test_reg_desc.ABlockWithMemory.AMemory.write(0, list(range(0, 128, 2)))
        self.assertTrue(
            np.array_equal(list(range(0, 128, 2)),
                           test_reg_desc._rio.read_words(0x500, 4, 4, 64)))

        test_reg_desc.TwoMemories.write(
            0, [list(range(100, 164, 1)), list(range(200, 264, 1))])
        self.assertTrue(
            np.array_equal(test_reg_desc.TwoMemories.read(), [list(range(100, 164, 1)), list(range(200, 264, 1))]))

    def test_mem_write(self):
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint32)

        test_reg_desc.TwoMemories.write(
            0, [list(range(100, 164, 1)), list(range(200, 264, 1))])

        test_reg_desc.TwoMemories.node.current_idx = [0]
        self.assertEqual(test_reg_desc._rio.read_words(
            test_reg_desc.TwoMemories.node.absolute_address, 4)[0], 100)
        self.assertEqual(test_reg_desc._rio.read_words(
            test_reg_desc.TwoMemories.node.absolute_address+10*4, 4)[0], 110)

        test_reg_desc.TwoMemories.node.current_idx = [1]
        self.assertEqual(test_reg_desc._rio.read_words(
            test_reg_desc.TwoMemories.node.absolute_address, 4)[0], 200)
        self.assertEqual(test_reg_desc._rio.read_words(
            test_reg_desc.TwoMemories.node.absolute_address+10*4, 4)[0], 210)

    def test_mem_read(self):
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)
        test_reg_desc._rio.write_words(0, 4, 4, np.arange(
            0, test_reg_desc.node.size-4, 4, dtype=np.uint64))

        read_data = test_reg_desc.TwoMemories.read()

        test_reg_desc.TwoMemories.node.current_idx = [0]
        self.assertEqual(
            test_reg_desc.TwoMemories.node.absolute_address, read_data[0][0])
        self.assertEqual(
            test_reg_desc.TwoMemories.node.absolute_address+6*4, read_data[0][6])

        test_reg_desc.TwoMemories.node.current_idx = [1]
        self.assertEqual(
            test_reg_desc.TwoMemories.node.absolute_address, read_data[1][0])
        self.assertEqual(
            test_reg_desc.TwoMemories.node.absolute_address+6*4, read_data[1][6])

    def test_tostr(self):
        """
        Test that the tostr function generates the desired output
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.array(
            list(range(test_reg_desc.node.size)), np.uint8)
        test_reg_desc._rio.verbose = False

        test_reg_desc.AnAddrmap.AnotherRegAt20.write(0x12345678)
        test_reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4.write(3)

        test_reg_desc.AnotherAddrmap.AnotherRegAt20.write(0x87654321)
        test_reg_desc.AnotherAddrmap.ARegWithFields.FIELD0DOWNTO0.write(1)

        test_reg_desc.Mem64x32.write(0, list(range(0, 20, 2)))

        test_reg_desc.AnotherAddrmap.TenRegs[4:7].write([4, 5, 6])
        test_reg_desc.TwoMemories[0].write(0, list(range(10, 120, 1)))
        test_reg_desc.TwoMemories[1].write(0, list(range(10, 120, 2)))

        result = str(test_reg_desc)
        expected = """test_register_description:
  AnAddrmap           :
    ARegWithFields    :   50462768 = 0x03020030
      FIELD0DOWNTO0   :          0 = 0x00000000
      FIELD13DOWNTO4  :          3 = 0x00000003
    ARepeatedReg      : [117835012 185207048 252579084]
      VAL             : [117835012 185207048 252579084]
    AnotherRegAt20    :  305419896 = 0x12345678
      VAL             :  305419896 = 0x12345678
    TenRegs           : [ 656811300  724183336  791555372  858927408  926299444  993671480 ...
      VAL             : [ 656811300  724183336  791555372  858927408  926299444  993671480 ...
    ARegfile          :
      ARegInARegFile  : [[1397903696 1465275732 1532647768 1600019804] ...
        VAL           : [[1397903696 1465275732 1532647768 1600019804] ...
    AnotherRegfile    :
      AReg            : [1936879984 2071624056]
        VAL           : [1936879984 2071624056]
      AnotherReg      : [2004252020 2138996092]
        VAL           : [2004252020 2138996092]
  AnotherAddrmap      :
    ARegWithFields    :   50462977 = 0x03020101
      FIELD0DOWNTO0   :          1 = 0x00000001
      FIELD13DOWNTO4  :         16 = 0x00000010
    ARepeatedReg      : [117835012 185207048 252579084]
      VAL             : [117835012 185207048 252579084]
    AnotherRegAt20    : 2271560481 = 0x87654321
      VAL             : 2271560481 = 0x87654321
    TenRegs           : [ 656811300  724183336  791555372  858927408          4          5 ...
      VAL             : [ 656811300  724183336  791555372  858927408          4          5 ...
    ARegfile          :
      ARegInARegFile  : [[1397903696 1465275732 1532647768 1600019804] ...
        VAL           : [[1397903696 1465275732 1532647768 1600019804] ...
    AnotherRegfile    :
      AReg            : [1936879984 2071624056]
        VAL           : [1936879984 2071624056]
      AnotherReg      : [2004252020 2138996092]
        VAL           : [2004252020 2138996092]
  ABlockWithMemory    :
    AReg              :   50462976 = 0x03020100
      VAL             :   50462976 = 0x03020100
    AMemory           : [  50462976  117835012  185207048  252579084  319951120  387323156 ...
    HundredRegs       : [  50462976  117835012  185207048  252579084  319951120  387323156 ...
      VAL             : [  256  1284  2312  3340  4368  5396  6424  7452  8480  9508 10536 11564 ...
  Mem64x32            : [         0          2          4          6          8         10 ...
  TwoMemories         : [[        10         11         12         13         14         15 ...
  AnAddrmapWith8bitRegs:
    AReg0             :          0 = 0x00
      VAL             :          0 = 0x00
    AReg1             :          1 = 0x01
      FIELD3DOWNTO0   :          1 = 0x01
      FIELD7DOWNTO4   :          0 = 0x00"""

        if result != expected:
            print(result)
            print(expected)
        self.assertEqual(result, expected)

    def test_help(self):
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        test_reg_desc.TwoMemories.help()
        sys.stdout = old_stdout
        result = mystdout.getvalue()
        expected = """name: 2x 64x32 Memory
desc: This are two memories
mementries: 64
memwidth: 32
"""
        if result != expected:
            print(result)
        self.assertEqual(result, expected)

    def test_performance(self):
        """
        Measure the performance and check if it is suitable
        """
        t = time.time()
        test_reg_desc = RegisterModel(root, RegIoNoHW())

        elapsed = time.time() - t
        print("Model creation time =" + str(elapsed) + "s")
        self.assertLess(elapsed, 0.2)

        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint32)

        access_cnt = 0
        ACCESSES = 10e3

        t = time.time()
        while access_cnt < ACCESSES:
            test_reg_desc.AnAddrmap.AnotherRegAt20.write(36)
            access_cnt += 1
            test_reg_desc.AnAddrmap.ARegWithFields.FIELD0DOWNTO0.write(1)
            access_cnt += 1
            test_reg_desc.AnAddrmap.AnotherRegAt20.read()
            access_cnt += 1
            test_reg_desc.AnAddrmap.ARepeatedReg[1].write(12)
            access_cnt += 1
            test_reg_desc.AnAddrmap.ARepeatedReg[1:3].read()
            access_cnt += 2
            test_reg_desc.Mem64x32.read(10, 20)
            access_cnt += 10

        elapsed = time.time() - t
        accesses_per_second = ACCESSES/elapsed
        print("Accesses = " + str(int(accesses_per_second)) + "/s")
        self.assertGreater(accesses_per_second, 20e3)

    def test_selectable(self):
        """
        Test is the selectable class is properly integrated
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)
        test_reg_desc._rio.verbose = False

        selector = Selector()
        test_reg_desc.AnotherAddrmap.ARepeatedReg[2]._construct_selector(
            selector.selected)
        self.assertEqual(selector.selected, [0, 0, 2])

        test_reg_desc.AnotherAddrmap.ARepeatedReg[2]._set_current_idx(
            selector.selected)
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg.node.current_idx, [2])
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg.node.parent.current_idx, [0])
        self.assertEqual(
            test_reg_desc.AnotherAddrmap.ARepeatedReg.node.parent.parent.current_idx, [0])

    def test_selectable_with_slice(self):
        """
        Test is the selectable class is properly integrated
        """
        test_reg_desc = RegisterModel(root, RegIoNoHW())
        test_reg_desc._rio.mem = np.zeros([test_reg_desc.node.size], np.uint8)
        test_reg_desc._rio.verbose = False

        selector = Selector()
        test_reg_desc.AnAddrmap.ARegfile.ARegInARegFile._construct_selector(
            selector.selected)
        self.assertEqual(selector.selected, [
                         0, 0, slice(0, 2, 1), slice(0, 4, 1)])

        selector = Selector()
        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[0:3:2]._construct_selector(
            selector.selected)
        self.assertEqual(selector.selected, [0, 0, 0, slice(0, 3, 2)])

        selector = Selector()
        test_reg_desc.AnAddrmap.ARegfile[0].ARegInARegFile[2]._construct_selector(
            selector.selected)
        self.assertEqual(selector.selected, [0, 0, 0, 2])

        selector = Selector()
        test_reg_desc.AnotherAddrmap.TenRegs[2:7:2]._construct_selector(
            selector.selected)
        self.assertEqual(selector.selected, [0, 0, slice(2, 7, 2)])


if __name__ == '__main__':
    unittest.main()
