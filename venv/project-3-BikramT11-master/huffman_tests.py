import unittest
import huffman#_inst
import subprocess
import filecmp

from huffman import *


class TestList(unittest.TestCase):

    def test_node_simple(self):
        node = HuffmanNode(ord('a'), 150)
        self.assertEqual(node.char, ord('a'))
        self.assertEqual(node.freq, 150)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

        n1 = HuffmanNode(ord('a'), 150)
        n2 = HuffmanNode(ord('a'), 150)
        self.assertTrue(n1 == n2)
        self.assertEqual(n1, n2)
       # assert n1 != n2
        assert n1 == n2
        self.assertFalse(n1 is n2)
        n1 = HuffmanNode(ord('a'), 150)
        n2 = HuffmanNode(ord('b'), 200)
        n3 = HuffmanNode(ord('z'), 200)
        n4 = HuffmanNode(ord('l'), 500)
        self.assertTrue(n1 < n2)
        self.assertFalse(n2 < n1)
        self.assertTrue(n2 < n3)
        self.assertFalse(n2 > n4)

    def test_node_repr(self):
        # Leaf node
        n1 = HuffmanNode(ord('a'), 150)
        self.assertEqual(repr(n1), "HuffmanNode(ord('a'), 150)")

        # Parent node
        t1 = HuffmanNode(ord('x'), 200, left=n1, right=n1)
        t1_exp = (
            "HuffmanNode(ord('x'), 200,\n"
            "    left  = HuffmanNode(ord('a'), 150),\n"
            "    right = HuffmanNode(ord('a'), 150)\n"
            ")")
        self.assertEqual(repr(t1), t1_exp)

        # Big tree
        bt1 = HuffmanNode(ord(' '), 13,
            left  = HuffmanNode(ord(' '), 6,
                left  = HuffmanNode(ord(' '), 3),
                right = HuffmanNode(ord('b'), 3)
            ),
            right = HuffmanNode(ord('a'), 7,
                left  = HuffmanNode(ord('c'), 3,
                    left  = HuffmanNode(ord('d'), 1),
                    right = HuffmanNode(ord('c'), 2)
                ),
                right = HuffmanNode(ord('a'), 4)
            )
        )

        bt1_exp = (
            "HuffmanNode(ord(' '), 13,\n"
            "    left  = HuffmanNode(ord(' '), 6,\n"
            "        left  = HuffmanNode(ord(' '), 3),\n"
            "        right = HuffmanNode(ord('b'), 3)\n"
            "    ),\n"
            "    right = HuffmanNode(ord('a'), 7,\n"
            "        left  = HuffmanNode(ord('c'), 3,\n"
            "            left  = HuffmanNode(ord('d'), 1),\n"
            "            right = HuffmanNode(ord('c'), 2)\n"
            "        ),\n"
            "        right = HuffmanNode(ord('a'), 4)\n"
            "    )\n"
            ")")
        self.assertEqual(repr(bt1), bt1_exp)

    def test_count_freq(self):
        freqlist = count_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    def test_create_huff_tree(self):
        freqlist = count_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_header(self):
        freqlist = count_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

    def test_generate_codes(self):
        freqlist = count_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = generate_codes(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_file1(self):
        huffman_encode("file1.txt", "file1_out.txt")
        err = subprocess.call(
            "diff -wb file1_out.txt file1_soln.txt",
            shell=True)
        self.assertEqual(err, 0)

    def test_count_freq_2(self):
        f = count_freq("file1.txt")
        a = [4, 3, 2, 1, 0, 0, 0]
        self.assertListEqual(f[97:104], a)

    def test_create_huff_tree_2(self):
        f = count_freq("file1.txt")
        huff = create_huff_tree(f)
        self.assertEqual(huff.freq, 13)
        self.assertEqual(huff.char, 32)
        left = huff.left
        self.assertEqual(left.freq, 6)
        self.assertEqual(left.char, 32)
        right = huff.right
        self.assertEqual(right.freq, 7)
        self.assertEqual(right.char, 97)

    def test_create_header_2(self):
        f = count_freq("file1.txt")
        self.assertEqual(create_header(f), "32 3 97 4 98 3 99 2 100 1")

    def test_generate_codes_2(self):
        f = count_freq("file2.txt")
        huff = create_huff_tree(f)
        c = generate_codes(huff)
        self.assertEqual(c[ord('d')], '1')
        self.assertEqual(c[ord('a')], '0000')
        self.assertEqual(c[ord('f')], '0001')
        self.assertEqual(c[ord('c')], '01')

    def test_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        self.assertTrue(filecmp.cmp("file1_out.txt", "file1_soln.txt"))


    def test_textfile_02(self):
        huffman_encode("file2.txt", "file2_out.txt")
        self.assertTrue(filecmp.cmp("file2_out.txt", "file2_soln.txt"))


    def test_textfile_03(self):
        huffman_encode("multiline.txt", "multiline_out.txt")
        self.assertTrue(filecmp.cmp("multiline_out.txt", "multiline_soln.txt"))

    def test_textfile_04(self):
        huffman_encode("declaration.txt", "declaration_out.txt")
        self.assertTrue(filecmp.cmp("declaration_out.txt", "declaration_soln.txt"))


    def test_00_decodefile(self):
        huffman_decode("file1_out.txt", "file1.txt")
        self.assertTrue(filecmp.cmp("file1_soln.txt", "file1_out.txt"))

    def test_01_decodefile(self):
        huffman_decode("declaration_out.txt", "declaration.txt")
        self.assertTrue(filecmp.cmp("declaration_soln.txt", "declaration_out.txt"))

    def test_02_decodefile(self):
        huffman_decode("file2_out.txt", "file2.txt")
        self.assertTrue(filecmp.cmp("file2_soln.txt", "file2_out.txt"))

    def test_03_decodefile(self):
        huffman_decode("multiline_out.txt", "multiline.txt")
        self.assertTrue(filecmp.cmp("multiline_soln.txt", "multiline_out.txt"))

    def test_parse_header_01(self):
        f = count_freq("file1.txt")
        b = create_header(f)
        listy = [4, 3, 2, 1]
        self.assertEqual(parse_header(b)[97:101], listy)

if __name__ == '__main__': 
   unittest.main()
