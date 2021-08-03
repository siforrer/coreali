

class TestConfig():
    def __init__(self):
        self.word_size = 4
        self.address_incr = 4
        self.testmem_address = 0
        self.testmem_size = 16*4
        

class Tester():

    def __init__(self, rio):
        self.rio = rio
        self.config = TestConfig()
        
        
    def test_all(self):
        self.test_single_access()
        self.test_multi_access_read()
        self.test_multi_access_write()


    def test_single_access(self):
        cfg = self.config
        test_value = 1234567 % 2**(cfg.word_size*8)
        self.rio.write_words(cfg.testmem_address,cfg.word_size,cfg.address_incr,[test_value])
        assert self.rio.read_words(cfg.testmem_address,cfg.word_size,cfg.address_incr,1)[0] == test_value
        for address in range(cfg.testmem_address,cfg.testmem_address+4*cfg.word_size,cfg.word_size):
            self.rio.write_words(address,cfg.word_size,4,[address])
        for address in range(cfg.testmem_address,cfg.testmem_address+4*cfg.word_size,cfg.word_size):
            assert self.rio.read_words(address,cfg.word_size,4,1)[0] == address
        
        
    def test_multi_access_read(self):
        cfg = self.config
        # initialize 
        address = list(range(cfg.testmem_address,cfg.testmem_address+4*cfg.address_incr,cfg.address_incr))
        written_words = address
        for i in range(len(address)):
            self.rio.write_words(address[i],cfg.word_size,cfg.address_incr,[written_words[i]])
        read_words = self.rio.read_words(cfg.testmem_address,cfg.word_size,cfg.address_incr,3)
        assert list(read_words) == written_words[0:3]
        read_words = self.rio.read_words(cfg.testmem_address+2*cfg.address_incr,cfg.word_size,cfg.address_incr,2)
        assert list(read_words) == written_words[2:4]
    
    def test_multi_access_write(self):
        cfg = self.config
        self.rio.write_words(cfg.testmem_address,cfg.word_size,cfg.address_incr,[10,20,30])
        for i in range(3):
            assert self.rio.read_words(cfg.testmem_address+i*cfg.address_incr,cfg.word_size,4,1)[0] == i*10+10
        
        self.rio.write_words(3*cfg.word_size,cfg.word_size,cfg.address_incr,[10,20,30])
        for i in range(3):
            assert self.rio.read_words(cfg.testmem_address+i*cfg.address_incr,cfg.word_size,4,1)[0] == i*10+10
        