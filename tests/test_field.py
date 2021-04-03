#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 17:25:25 2021

@author: silvan
"""
import os
import sys
sys.path.insert(0, "../src/")
import unittest
import numpy as np
from systemrdl import RDLCompiler, RDLCompileError
from coreali import PythonExporter
from coreali.registerio import RegIoNull

input_files = ["./test_register_description.rdl"]

if not os.path.exists("generated/python/"):
    os.makedirs("generated/python/")

rdlc = RDLCompiler()

try:
    for input_file in input_files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()
except RDLCompileError:
    sys.exit(1)

pythonExporter = PythonExporter()
pythonExporter.source_files = input_files
pythonExporter.export(root, "generated/python/test_register_description.py")
sys.path.insert(0, "generated/python/")
from test_register_description import test_register_description


class TestAccessableFieldNode(unittest.TestCase):
    def test_modify_register_value(self):
        test_reg_desc = test_register_description(RegIoNull())
        test_reg_desc._rio.mem = np.empty([test_reg_desc.node.size], np.uint8)
        test_reg_desc._rio.verbose = False
        
        field = test_reg_desc.AnAddrmap.ARegWithFields.FIELD13DOWNTO4
        self.assertEqual(field._modify_register_value(np.uint64(0),np.uint64(12)), 12*2**4)
        field_value = field._register_to_field_value(np.uint64(22))
        self.assertTrue(isinstance(field_value, np.uint64))
        
    
if __name__ == '__main__':
    unittest.main()
