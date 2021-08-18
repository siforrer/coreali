import unittest
import runpy
import os
import sys

root = os.path.dirname(__file__)+"/"
if not "../src/" in sys.path:
    sys.path.insert(0, root+"../src/")


class TestExamples(unittest.TestCase):
    def test_quickstart(self):
        runpy.run_path(root+"../examples/quickstart/run_example.py")


if __name__ == '__main__':
    unittest.main()
