#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:38:56 2021

@author: silvan
"""
import sys
if not "../src/" in sys.path:
    sys.path.insert(0, "../src/")
import unittest
import numpy as np
from coreali.regmodel import Selector, Selectable


    
class A(Selectable):
    def __init__(self):
        Selectable.__init__(self, None)
        self.b = B(self) 

    def default_start(self):
        return 0
    def default_stop(self):
        return 0
    def default_step(self):
        return 1


class B(Selectable):
    def __init__(self, parent):
        Selectable.__init__(self, parent)
        self.c = C(self)

    def default_start(self):
        return 0
    def default_stop(self):
        return 0
    def default_step(self):
        return 1


class C(Selectable):
    def __init__(self, parent):
        Selectable.__init__(self, parent)

    def default_start(self):
        return 0
    def default_stop(self):
        return 0
    def default_step(self):
        return 1



class TestSelector(unittest.TestCase):
    
    def test_data_shape(self):
        selector = Selector()
        selector.selected = [0, 0, slice(2, 7, 2)]
        self.assertEqual(selector.data_shape(), [3])

        selector.selected = [0, 0, slice(2, 8, 2)]
        self.assertEqual(selector.data_shape(), [3])

        selector.selected = [0, 0, slice(2, 3, 3)]
        self.assertEqual(selector.data_shape(), [1])

        selector.selected = [0, 0, slice(2, 4, 3)]
        self.assertEqual(selector.data_shape(), [1])

        selector.selected = [0, 0, slice(2, 5, 3)]
        self.assertEqual(selector.data_shape(), [1])

        selector.selected = [0, 0, slice(2, 6, 3)]
        self.assertEqual(selector.data_shape(), [2])
        
    def test_enumerate(self):
        selector = Selector()
        selector.selected = [1, slice(2,10,2),slice(0,2,1)]
        
        expected_flat_idx = [0, 2, 4, 6]
        expected_flat_len = 2
        expected_sel_idx = [[1, 2, 0],
                            [1, 4, 0],
                            [1, 6, 0],
                            [1, 8, 0]];
        
        self.assertEqual(selector.data_shape(), [4, 2])
        self.assertEqual(selector.numel(), 8)
        self.assertEqual(selector.flat_len(), expected_flat_len)        
        flat_data = np.empty([selector.numel()],dtype=np.uint64)            
        i = 0
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            self.assertEqual(flat_idx, expected_flat_idx[i])
            self.assertTrue(np.array_equal(sel_idx, expected_sel_idx[i]))
            flat_data[flat_idx:flat_idx+selector.flat_len()] = np.array([flat_idx, flat_idx+1])
            i+=1
        data = flat_data.reshape(selector.data_shape())
        expected_data = np.array([[0,1],[2,3],[4,5],[6,7]])
        self.assertTrue(np.array_equal(data,expected_data))
    
    def test_last_not_slice(self):
        selector = Selector([0, 0, slice(0, 2, 1), 0])
        self.assertEqual(selector.data_shape(), [2])    
        self.assertEqual(selector.flat_len(), 1)    
        flat_data = np.empty([selector.numel()],dtype=np.uint64)    
        flat_len = selector.flat_len()
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            flat_data[flat_idx:flat_idx+flat_len] = np.array([flat_idx])
            
    def test_no_slice(self):
        selector = Selector([0, 0, 0])
        self.assertEqual(selector.data_shape(), [])  
        
    def test_usecase(self):
        a = A()
        a.b.c        
        selector = Selector()
        a[0:2].b[0].c[4:10]._construct_selector(selector.selected)
        self.assertEqual(selector.selected,[slice(0,2,1), 0, slice(4,10,1)])
        self.assertEqual(selector.data_shape(), [2, 6])
        flat_data = np.empty([selector.numel()],dtype=np.uint64)            
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            flat_data[flat_idx:flat_idx+selector.flat_len()] = flat_idx+np.arange(selector.flat_len(),dtype=np.uint64)
        data = flat_data.reshape(selector.data_shape())
        self.assertTrue((data[0] == [ 0, 1, 2, 3, 4, 5]).all())
        self.assertTrue((data[1] == [ 6,7,8,9,10,11]).all())
        flat_data = np.empty([selector.numel()],dtype=np.uint64)            
        for _idx, (flat_idx, sel_idx) in enumerate(selector):
            addr = np.sum(sel_idx*[100,10,1])
            flat_data[flat_idx:flat_idx+selector.flat_len()] = addr+np.arange(selector.flat_len(),dtype=np.uint64)
        data = flat_data.reshape(selector.data_shape())
        self.assertTrue((data[0] == [ 4,5,6,7,8,9]).all())
        self.assertTrue((data[1] == [ 104,105,106,107,108,109]).all())
if __name__ == '__main__':
    unittest.main()
