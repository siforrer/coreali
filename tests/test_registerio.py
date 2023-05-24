#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 16:03:37 2021

@author: silvan
"""
from coreali.registerio import RegIoNoHW
import numpy as np


def test_write_words():
    rio = RegIoNoHW()
    rio.mem = np.zeros([40], np.uint8)

    rio.write_words(12, 4, 4, [1, 2, 3])

    assert rio.read_words(8, 4)[0] == 0
    assert rio.read_words(12, 4)[0] == 1
    assert rio.read_words(16, 4)[0] == 2
    assert rio.read_words(20, 4)[0] == 3
    assert rio.read_words(24, 4)[0] == 0


def test_read_words():
    rio = RegIoNoHW()
    rio.mem = np.zeros([64], np.uint8)

    rio.write_words(0, 4, 4, np.arange(0, 16))

    assert np.array_equal(
        rio.read_words(10*4, 4, 4, 6), np.arange(10, 16))


def test_uint32():
    rio = RegIoNoHW()
    rio.mem = np.zeros([16], np.uint32)
    rio.write_words(0, 4, 4, np.arange(0, 16))
    assert np.array_equal(
        rio.mem, np.arange(0, 16))
    assert np.array_equal(
        rio.read_words(10*4, 4, 4, 6), np.arange(10, 16))


def test_write_words_masked():
    rio = RegIoNoHW()
    rio.mem = np.zeros([16], np.uint32)
    rio.write_words_masked(4, 4, 4, [0x1234567], [0x000000ff])
    assert rio.mem[1] == 0x67
    rio.write_words_masked(4, 4, 4, [0x12345678], [0x10000000])
    assert rio.mem[1] == 0x10000067


def test_modify_words():
    rio = RegIoNoHW()
    rio.mem = np.zeros([16], np.uint32)
    rio.modify_words(4, 4, 4, 0, 31, [0x12345678])
    assert rio.mem[1] == 0x12345678
    rio.modify_words(4, 4, 4, 28, 31, [0xf])
    assert rio.mem[1] == 0xf2345678
    rio.modify_words(4, 4, 4, 0, 3, [0x0])
    assert rio.mem[1] == 0xf2345670
