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
    
    def test_write_words(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([40],np.uint8)        
        
        rio.write_words(12, 4, 4, [1,2,3])

        self.assertEqual(rio.read_words( 8,4)[0],0)
        self.assertEqual(rio.read_words(12,4)[0],1)
        self.assertEqual(rio.read_words(16,4)[0],2)
        self.assertEqual(rio.read_words(20,4)[0],3)
        self.assertEqual(rio.read_words(24,4)[0],0)
        
    def test_read_words(self):
        rio = RegIoNoHW()
        rio.mem = np.zeros([64],np.uint8)        
        
        rio.write_words(0, 4, 4, np.arange(0,16))

        self.assertTrue(np.array_equal(
                rio.read_words(10*4,4,4,6),np.arange(10,16)))


if __name__ == '__main__':
    unittest.main()
