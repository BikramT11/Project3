import unittest
import huffman#_inst
import subprocess

from huffman import *


class TestList(unittest.TestCase):
    
    def test_first(self):
        n1 = HuffmanNode(ord('a'), 150)
        n2 = HuffmanNode(ord('b'), 200)
        n3 = HuffmanNode(ord('c'), 100)
        n4 = HuffmanNode(ord('z'), 100)
        n5 = HuffmanNode(ord('a'), 100)
        self.assertTrue(first(n1, n2))
        self.assertFalse(first(n2, n1))
        self.assertTrue(first(n3, n4))
        self.assertFalse(first(n2, n1))
        self.assertFalse(first(n4, n5))

    def test_comnine(self):
        n1 = HuffmanNode(ord('a'), 150)
        n2 = HuffmanNode(ord('b'), 200)
        n3 = HuffmanNode(ord('c'), 100)
        n4 = HuffmanNode(ord('z'), 100)
        n5 = HuffmanNode(ord('a'), 100)
        self.assertEqual(combine(n1, n2), HuffmanNode(ord('a'), 350))
        self.assertEqual(combine(n2, n3), HuffmanNode(ord('b'), 300))
        self.assertEqual(combine(n5, n3), HuffmanNode(ord('a'), 200))




if __name__ == '__main__':
    unittest.main()
