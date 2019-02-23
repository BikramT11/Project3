class HuffmanEncodingError(Exception):
    pass

class HuffmanNode:

    def __init__(self, char, freq, left = None, right = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    # self.code = None

    # def set_code(self, code):
    #    self.code = code

    def set_right(self, node):
        self.right = node

    def set_left(self, node):
        self.left = node

    def leafy(self):
        return self.left is None and self.right is None

    def __eq__(self, other):
        if isinstance(other, HuffmanNode) and self.char == other.char and other.freq == self.freq:
            return True
        if other and other.left == self.left and self.right == other.right:
            return True
        return False

    def __lt__(self, other):
        if self.freq < other.freq:
            return True
        if other.freq == self.freq and other.char > self.char:
            return True
        return False

    def __repr__(self):
        if "indent" not in HuffmanNode.__dict__:
            HuffmanNode.indent = 0
        z = "HuffmanNode(ord({}), {}".format(repr(chr(self.char)),self.freq)
        if self.left:
            HuffmanNode.indent += 4
            z += ",\n" + " " * HuffmanNode.indent + "left  = {}".format(repr(self.left))
            HuffmanNode.indent -= 4
        if self.right:
            HuffmanNode.indent += 4
            z += ",\n" + " " * HuffmanNode.indent + "right = {}\n".format(repr(self.right))
            HuffmanNode.indent -= 4
        if self.left and not self.right:
            z += ",\n"
        if z[-1] == "\n":
            z += " " * (HuffmanNode.indent) + ")"
        else:
            z += ")"
        if HuffmanNode.indent == 0:
            del HuffmanNode.indent
        return z


#class HuffmanEncodingError(Exception):
#  pass

def count_freq(filename):
    with open(filename) as f:
        info = f.read()
    freq = [0] * 256
    for i in info:
        freq[ord(i)] += 1
    return freq
# f = open(filename)
# l = []
#  for i in range(256):
#     l.append(0)
#  while True:
#     b = f.read()
#    if not b:
#         break
#   if ord(b) < 256:
#       l[ord(b)] + 1
# f.close()
# return l

def first(x, y):
    if x.freq < y.freq:
        return True
    if x.freq == y.freq and x.char < y.char:
        return True
    return False

def combine(x, y):
    new = HuffmanNode(None, x.freq + y.freq)
    if first(x, y):
        new.set_right(y)
        new.set_left(x)
    else:
        new.set_right(x)
        new.set_left(y)
    if new.left.char < new.right.char:
        new.char = new.left.char
    else:
        new.char = new.right.char
    return new

    #if x.char < y.char:
    #    char = x.char
#   else:
#       char = y.char
#   p = HuffmanNode(char, x.freq + y.freq)
#   p.set_left(x)
#   p.set_right(y)
#   return p


def freq_list_maker(listy):
    if len(listy) == 1:
        return listy[0]
    for i in range(len(listy)):
        max = i
        for j in range(i + 1, len(listy)):
            if first(listy[max], listy[j]):
                max = j
        listy[i], listy[max] = listy[max], listy[i]
    p = combine(listy[-1], listy[-2])
    listy = listy[:-2]
    listy.append(p)
    return freq_list_maker(listy)

#def mini(listy):
#  min = listy[0]
#   count = 1
#   index = 0
#   while count < len(listy):
#       if first(listy[count], min):
##           min = listy[count]
#           index = count
# count += 1
#   return index

def create_huff_tree(freq_list):
    lis = [HuffmanNode(i, freq_list[i]) for i in range(len(freq_list)) if freq_list[i]]
    if not len(lis):
        return None
    lis.sort(key = lambda x: (x.freq, x.char))
    while len(lis) > 1:
        nodey = combine(lis[0], lis[1])
        lis = lis[2:]
        lis.append(nodey)
        lis.sort(key = lambda x: (x.freq, x.char))
    return lis[0]

# for i in range(len(freq_list)):
# if freq_list[i] > 0:
#     lis.append(HuffmanNode(i, freq_list[i]))
#  return freq_list_maker(lis)

#  new = freq_list_maker(freq_list)
#  if len(new) is 0:
#      return HuffmanNode(0,0)
#  h = None
#  while len(new) != 1:
#    b = mini(new)
#      first_node = new[b]
#     del new[b]
#     b = mini(new)
#     sec_node = new[b]
#     del new[b]
#     h = combine(first_node, sec_node)
#     new.append(h)
## start = new[0]
#  return start

def generate_codes(root_node):
    listy = [''] * 256
    def lister(char, code):
        listy[char] = code
    codes_iteration(root_node, "", None, lister)
    return listy

def codes_iteration(node, c, direction, adder):
    if node:
        if direction:
            if node.right == None and node.left == None:
                if direction == "l":
                    adder(node.char, c + "0")
                else:
                    adder(node.char, c + "1")
            else:
                if direction == "l":
                    c += "0"
                else:
                    c += "1"
        codes_iteration(node.left, c, "l", adder)
        codes_iteration(node.right, c, "r", adder)


# if node.leafy():
#   c[node.char] = node.code
# else:
#  if node.right is not None:
#    node.right.code = node.code + "1"
#    codes_iteration(node.right, c)
# if node.left is not None:
#     node.left.code = node.code + "0"
#     codes_iteration(node.left, c)
#  return c

def create_header(freq_list):
    head = ""
    for i in range(len(freq_list)):
        if freq_list[i]:
            head += str(i) + " " + str(freq_list[i]) + " "
    return head[:len(head) - 1]

def huffman_encode(in_file, out_file):
    freq = count_freq(in_file)
    huff_rooter = create_huff_tree(freq)
    c = generate_codes(huff_rooter)
    head = create_header(freq)
    with open(in_file, "r") as f:
        info = f.read()
    with open(out_file, "w") as o:
        if len(info):
            o.write(head + "\n")
            if sum(1 for i in freq if i) > 1:
                for x in info:
                    o.write(c[ord(x)])
    f.close()
    o.close()

def parse_header(header_string):
    f = [0] * 256
    listy = header_string.split()
    len_str = len(listy)
    for i in range(0, len_str, 2):
        f[int(listy[i])] = int(listy[i + 1])
    return f

def huffman_decode(in_file, out_file):
    with open(in_file, 'r') as f:
        chaar = parse_header(f.readline().strip())
        huffy = create_huff_tree(chaar)
        with open(out_file, 'w') as o:
            one_char = decode_char(f, huffy)
            if one_char:
                while one_char:
                    o.write(one_char)
                    one_char = decode_char(f, huffy)
            else:
                if any(i for i in chaar):
                    for newy, c in enumerate(chaar):
                        if c:
                            for b in range(c):
                                o.write(chr(newy))
    f.close()
    o.close()

def decode_char(file, n):
    code = file.read(1)
    if not code:
        return None
    while code:
        if code == '0':
            n = n.left
        else:
            n = n.right
        if n.left == None and n.right == None:
            return chr(n.char)
        code = file.read(1)


