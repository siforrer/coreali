#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:38:56 2021

@author: silvan
"""
import sys
sys.path.insert(0, "../src/")
import unittest
import numpy as np
from coreali.Selector import Selector, Selectable


    
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
        
        self.assertEqual(selector.data_shape(), [4, 2])
        self.assertEqual(selector.numel(), 8)
        
        for flat_idx, sel_idx in enumerate(selector):
            self.assertEqual(sel_idx[0][1], flat_idx % 2)
            self.assertEqual(sel_idx[0][0], int(flat_idx / 2))
            self.assertEqual(sel_idx[1][0], 1)
            self.assertEqual(sel_idx[1][1], int(flat_idx / 2)*2+2)
            self.assertEqual(sel_idx[1][2], flat_idx % 2)
        
    def test_usecase(self):
        a = A()
        a.b.c
        
        selector = Selector()
        a[0:2].b[0].c[4:10]._construct_selector(selector.selected)
        self.assertEqual(selector.selected,[slice(0,2,1), 0, slice(4,10,1)])
        self.assertEqual(selector.data_shape(), [2, 6])
        data = np.empty(selector.data_shape(), np.uint64);
        for flat_idx, sel_idx in enumerate(selector):
            data[np.unravel_index(flat_idx,selector.data_shape())] = flat_idx
        self.assertTrue((data[0] == [ 0, 1, 2, 3, 4, 5]).all())
        self.assertTrue((data[1] == [ 6,7,8,9,10,11]).all())
        for flat_idx, sel_idx in enumerate(selector):
            addr = np.sum(sel_idx[1]*[100,10,1])
            data[np.unravel_index(flat_idx,selector.data_shape())] = addr 
        self.assertTrue((data[0] == [ 4,5,6,7,8,9]).all())
        self.assertTrue((data[1] == [ 104,105,106,107,108,109]).all())
if __name__ == '__main__':
    unittest.main()
