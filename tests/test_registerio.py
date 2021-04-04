#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:03:37 2021

@author: silvan
"""
import numpy as np
import unittest
import sys
sys.path.insert(0, "../src/")

from coreali.registerio import RegIoNoHW

class TestRegisterIo(unittest.TestCase):
    
    def test_write_raw(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([10],np.uint8)
        
        rio.write_raw(5,[2])
        self.assertEqual(rio.mem[5],2)
        
        rio.write_raw(3,[4, 5, 6, 7])
        self.assertTrue(np.array_equal(
                rio.mem, [0, 0, 0, 4, 5, 6, 7, 0, 0, 0]))

    def test_read_raw(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([10],np.uint8)
        for i in range(len(rio.mem)):
            rio.mem[i] = i+100
        
        self.assertEqual(rio.read_raw(5,1),105)
        
        self.assertTrue(np.array_equal(
                rio.read_raw(5,3), [105,106,107]))
        
    def test_write_word(self):
        rio = RegIoNoHW()
        rio.mem = np.arange(100, 116, dtype=np.uint8)        
        rio.write_word(8, 4, 0x04030201)
        self.assertTrue(np.array_equal(
                rio.mem[8:12], [1,2,3,4]))
        
        rio.write_word(10, 2, 0x0201)
        self.assertTrue(np.array_equal(
                rio.mem[10:12], [1,2]))
        
    def test_read_word(self):
        rio = RegIoNoHW()
        rio.mem = np.arange(0x10, 0x30, dtype=np.uint8)        

        self.assertEqual(rio.read_word(4,4),0x17161514)
        
        self.assertEqual(rio.read_word(6,2),0x1716)
        
    def test_write_words(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([40],np.uint8)        
        
        rio.write_words(12, 4, [1,2,3])

        self.assertEqual(rio.read_word(8,4),0)
        self.assertEqual(rio.read_word(12,4),1)
        self.assertEqual(rio.read_word(16,4),2)
        self.assertEqual(rio.read_word(20,4),3)
        self.assertEqual(rio.read_word(24,4),0)
        
    def test_read_words(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([64],np.uint8)        
        
        rio.write_words(0, 4, np.arange(0,16))

        self.assertTrue(np.array_equal(
                rio.read_words(10*4,4,6),np.arange(10,16)))


if __name__ == '__main__':
    unittest.main()
