import unittest
import numpy as np
import sys
if not "../src/" in sys.path:
    sys.path.insert(0, "../src/")
from coreali.regmodel import Memory,Selector
from coreali.registerio import RegIoNoHW

class DummyNode():
    def __init__(self):
        self.property = {"mementries": 8, 
                         "memwidth" : 32}
        self.parent = None
        self.is_array = False
        self.current_idx = [0]

    @property
    def absolute_address(self):
        return int(40 + self.current_idx[0]*self.property["mementries"]*self.property["memwidth"]/8)

    def get_property(self, key):
        return self.property[key]
    

class DummyMem(Memory):
    def __init__(self):
        self._select = None
        self._parent = None
        self.node = DummyNode()
        self._rio = RegIoNoHW()
        self._rio.mem = np.zeros(256,np.uint8)
        self._rio.mem[::4] = np.arange(len(self._rio.mem)/4, dtype=np.uint8)
    
    
        
class TestAccessableMemNode(unittest.TestCase):
    
    def test_prepare_read(self):
        mem = DummyMem()
        selector = Selector([0,0]) 
        selector, flat_data, flat_len = mem._prepare_read(selector, 10,[])
        self.assertEqual(flat_len,10)
        self.assertTrue(np.array_equal(flat_data.shape, [10]))
        self.assertEqual(selector.selected[0],0)
        self.assertEqual(selector.selected[1],0)
        self.assertEqual(selector.selected[2],slice(0,10,1))
        
        selector = Selector([1]) 
        selector, flat_data, flat_len = mem._prepare_read(selector,10, [3])
        self.assertEqual(flat_len,1)
        self.assertTrue(np.array_equal(flat_data.shape, [1]))
        self.assertEqual(selector.selected[0],1)
        self.assertEqual(selector.selected[1],slice(3,4,1))
        
        selector = Selector([1]) 
        selector, flat_data, flat_len = mem._prepare_read(selector,10,[20,30,2])
        self.assertEqual(flat_len,5)
        self.assertTrue(np.array_equal(flat_data.shape, [5]))
        self.assertEqual(selector.selected[0],1)
        self.assertEqual(selector.selected[1],slice(20,30,2))        
       
        selector = Selector([slice(3,5,1)]) 
        selector, flat_data, flat_len = mem._prepare_read(selector,10,[20,30,2])
        self.assertEqual(flat_len,5)
        self.assertTrue(np.array_equal(flat_data.shape, [10]))
        self.assertTrue(np.array_equal(selector.data_shape(), [2, 5]))
        self.assertEqual(selector.selected[0],slice(3,5,1))
        self.assertEqual(selector.selected[1],slice(20,30,2))     
        
        selector = Selector([0]) 
        selector, flat_data, flat_len = mem._prepare_read(selector,10,[4,8])
        self.assertEqual(flat_len,4)
        self.assertTrue(np.array_equal(flat_data.shape, [4]))
        self.assertTrue(np.array_equal(selector.data_shape(), [4]))
        self.assertEqual(selector.selected[0],0)
        self.assertEqual(selector.selected[1],slice(4,8,1))     

    def test_read(self):
        mem = DummyMem()
        self.assertTrue(np.array_equal(mem.read(),10+np.arange(8)))
        self.assertTrue(np.array_equal(mem.read(4,8),10+np.arange(4,8,1)))
        
    def test_write(self):
        mem = DummyMem()
        mem.write(0,1234567)
        self.assertEqual(mem._rio.read_words(40,4)[0],1234567)
        
        mem.write(1,2345678)
        self.assertEqual(mem._rio.read_words(44,4)[0],2345678)

        mem.write(6,[10001, 10002])
        self.assertTrue(np.array_equal(mem._rio.read_words(40+6*4,4,4,2),[10001, 10002]))
        mem.write(0,np.arange(8,dtype=np.uint64))
        self.assertTrue(np.array_equal(mem._rio.read_words(40,4,4,8),np.arange(8,dtype=np.uint32)))

    def test_write_array(self):
        mem = DummyMem()
        mem.node.is_array = True
        mem.node.array_dimensions = [3]
        
        for i in range(3):
            mem[i].write(0,i+1234567)
            self.assertEqual(mem._rio.read_words(i*4*8+40,4)[0],i+1234567)
            
            mem[i].write(1,i+2345678)
            self.assertEqual(mem._rio.read_words(i*4*8+44,4)[0],i+2345678)
    
            mem[i].write(6,[i+10001, i+10002])
            self.assertTrue(np.array_equal(mem[i]._rio.read_words(i*4*8+40+6*4,4,4,2),[i+10001, i+10002]))
            mem[i].write(0,i+np.arange(8,dtype=np.uint64))
            self.assertTrue(np.array_equal(mem[i]._rio.read_words(i*4*8+40,4,4,8),i+np.arange(8,dtype=np.uint32)))
    
    def test_read_array(self):
        mem = DummyMem()
        mem.node.is_array = True
        mem.node.array_dimensions = [2]
        mem.node.property = {"mementries": 4, 
                         "memwidth" : 8}
        mem.node.current_idx = [0]

        arr = np.array([[1,2,3,4],[11,12,13,14]],dtype=np.uint64)
        mem.write(0, arr)    
        self.assertTrue(np.array_equal(mem[0].read(),[1,2,3,4]))
        self.assertTrue(np.array_equal(mem[1].read(),[11,12,13,14]))
        self.assertTrue(np.array_equal(mem._rio.read_words(40,1,1,4),[1,2,3,4]))
        self.assertTrue(np.array_equal(mem._rio.mem[40:48], [1,2,3,4,11,12,13,14] ))
        self.assertTrue(np.array_equal(mem.read(),arr))

if __name__ == '__main__':
    unittest.main()
