from bin2coe.convert import *
import io

import pytest

def test_bits():
    assert [0,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0] == list(bits(b'0x'))

def test_chunks():
    assert [['a','b','c'],['d','e','f'],['g','h']] == list(chunks('abcdefgh', 3))

def test_bitsn_pow2():
    assert [5,4,6,5,7,3,7,4] == list(bitsn(b'Test', 4))

def test_bitsn_nonpow2():
    assert [0,0,2,0,1,0,0,3] == list(bitsn(bytes([1,2,3]), 3))

def test_convert_nofill():
    f = io.BytesIO()
    convert(f, bytes([1,2,3,47,1,3,3,7]), 32, 2, None, 16)
    f.seek(0)
    expected = b'''
memory_initialization_radix = 16;
memory_initialization_vector =
0102032f,
01030307;
'''.lstrip()
    assert expected == f.read()

def test_convert_fill():
    f = io.BytesIO()
    convert(f, bytes([1, 7]), 16, 3, 12, 4)
    f.seek(0)
    expected = b'''
memory_initialization_radix = 4;
memory_initialization_vector =
00010013,
00000030,
00000030;
'''.lstrip()
    assert expected == f.read()
