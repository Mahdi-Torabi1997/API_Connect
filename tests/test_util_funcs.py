import struct
from unittest import TestCase
from src.main import parseStringInt32, parseStringInt16, parseStringFloat

class TestUtilFuncs(TestCase):

    def test_parseStringInt32(self):
        data = struct.pack('i', 12345)
        result = parseStringInt32(data, 0)
        self.assertEqual(result, 12345)

    def test_parseStringInt16(self):
        data = struct.pack('h', 12345)
        result = parseStringInt16(data, 0)
        self.assertEqual(result, 12345)

    def test_parseStringFloat(self):
        data = struct.pack('f', 1.23) + struct.pack('f', 4.56)
        result = parseStringFloat(data, 0)
        self.assertAlmostEqual(result, 1.23, places=5)
        result = parseStringFloat(data, 4)
        self.assertAlmostEqual(result, 4.56, places=5)
