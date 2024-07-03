import unittest
from src.main import parseStringInt32, parseStringInt16, parseStringFloat

class TestUtilFuncs(unittest.TestCase):

    def test_parseStringInt32(self):
        data = b'\x01\x00\x00\x00\x02\x00\x00\x00'
        self.assertEqual(parseStringInt32(data, 0), 1)
        self.assertEqual(parseStringInt32(data, 4), 2)

    def test_parseStringInt16(self):
        data = b'\x01\x00\x02\x00'
        self.assertEqual(parseStringInt16(data, 0), 1)
        self.assertEqual(parseStringInt16(data, 2), 2)

    def test_parseStringFloat(self):
        data = struct.pack('f', 1.23) + struct.pack('f', 4.56)
        self.assertAlmostEqual(parseStringFloat(data, 0), 1.23, places=2)
        self.assertAlmostEqual(parseStringFloat(data, 4), 4.56, places=2)

if __name__ == '__main__':
    unittest.main()
