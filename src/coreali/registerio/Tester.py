import numpy as np
import time


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
# TODO better use a dict        self.config = ["word_size": 4,"address_incr": 4, "testmem_address": 0, "testmem_size" :16*4]

    def test_all(self):
        self.test_single_access()
        self.test_multi_access_read()
        self.test_multi_access_write()

    def test_single_access(self):
        cfg = self.config
        test_value = 1234567 % 2**(cfg.word_size*8)
        self.rio.write_words(cfg.testmem_address,
                             cfg.word_size, cfg.address_incr, [test_value])
        assert self.rio.read_words(
            cfg.testmem_address, cfg.word_size, cfg.address_incr, 1)[0] == test_value
        for address in range(cfg.testmem_address, cfg.testmem_address+4*cfg.word_size, cfg.word_size):
            self.rio.write_words(address, cfg.word_size, 4, [address])
        for address in range(cfg.testmem_address, cfg.testmem_address+4*cfg.word_size, cfg.word_size):
            assert self.rio.read_words(address, cfg.word_size, 4, 1)[
                0] == address

        test_mask = np.uint64(int("0f", 16))
        test_value = np.uint64(int("55", 16))
        self.rio.write_words(cfg.testmem_address,
                             cfg.word_size, cfg.address_incr, [0])
        self.rio.write_words_masked(
            cfg.testmem_address, cfg.word_size, cfg.address_incr, [test_value], [test_mask])
        assert self.rio.read_words(
            cfg.testmem_address, cfg.word_size, cfg.address_incr, 1)[0] == int("05", 8)

    def test_multi_access_read(self):
        cfg = self.config
        # initialize
        address = list(range(cfg.testmem_address,
                             cfg.testmem_address+4*cfg.address_incr, cfg.address_incr))
        written_words = address
        for i in range(len(address)):
            self.rio.write_words(
                address[i], cfg.word_size, cfg.address_incr, [written_words[i]])
        read_words = self.rio.read_words(
            cfg.testmem_address, cfg.word_size, cfg.address_incr, 3)
        assert list(read_words) == written_words[0:3]
        read_words = self.rio.read_words(
            cfg.testmem_address+2*cfg.address_incr, cfg.word_size, cfg.address_incr, 2)
        assert list(read_words) == written_words[2:4]

    def test_multi_access_write(self):
        cfg = self.config
        self.rio.write_words(cfg.testmem_address,
                             cfg.word_size, cfg.address_incr, [10, 20, 30])
        for i in range(3):
            assert self.rio.read_words(
                cfg.testmem_address+i*cfg.address_incr, cfg.word_size, 4, 1)[0] == i*10+10

        self.rio.write_words(3*cfg.word_size, cfg.word_size,
                             cfg.address_incr, [10, 20, 30])
        for i in range(3):
            assert self.rio.read_words(
                cfg.testmem_address+i*cfg.address_incr, cfg.word_size, 4, 1)[0] == i*10+10

    def _test_performance_of_function(self, name, function, factor, minimum_requirement=0):
        cfg = self.config
        iterations = 0
        t = time.time()
        while True:
            function()
            iterations += 1
            elapsed = time.time() - t
            if elapsed > 0.1:
                break
        print("{:<20}  {:>10} bit/s = {:>10} accesses/s".format(name,
                                                                int(cfg.word_size*8*factor*iterations/elapsed), int(factor*iterations/elapsed)))
        assert int(factor*iterations/elapsed) > minimum_requirement

    def test_performance(self, minimum_requirement=0):
        cfg = self.config
        num_words = min(int(cfg.testmem_size/cfg.address_incr), 1000)
        write_values = np.arange(num_words, dtype=np.uint64)

        use_cases = {
            "name": ["Single write", "Single read", "Single modify", "Burst write", "Burst read", "Burst modify"],
            "function": [
                lambda: self.rio.write_words(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, [0]),
                lambda: self.rio.read_words(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, 1),
                lambda: self.rio.write_words_masked(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, [1], [1]),
                lambda: self.rio.write_words(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, write_values),
                lambda: self.rio.read_words(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, num_words),
                lambda: self.rio.write_words_masked(
                    cfg.testmem_address, cfg.word_size, cfg.address_incr, write_values, write_values),
            ],
            "factor": [1, 1, 1, num_words, num_words, num_words]
        }

        for i in range(len(use_cases["name"])):
            self._test_performance_of_function(
                use_cases["name"][i], use_cases["function"][i], use_cases["factor"][i], minimum_requirement)
