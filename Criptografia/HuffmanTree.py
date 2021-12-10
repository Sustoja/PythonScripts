class HuffmanNode:

    def __init__(self, symbol, count=0, left=None, right=None):
        # Character and the number of times it appears on the text
        self.symbol = symbol
        self.count = count

        # Child nodes
        self.left = left
        self.right = right

        # Tree direction 0/1
        self.bit = ''

    def print(self):
        print(self.symbol + ": " + str(self.count))


class HuffmanTree:

    def __HuffmanNodesArray(self, text):
        # Calculate frequency of every symbol using a dictionary
        symbols = dict()
        for elem in text:
            if elem in symbols:
                symbols[elem] += 1
            else:
                symbols[elem] = 1

        # Create an array of HuffmanNodes
        nodes = []
        for k, v in symbols.items():
            nodes.append(HuffmanNode(k, v))

        return nodes

    def __CalculateCodes(self, node, val=''):
        newVal = val + node.bit

        if (node.left):
            self.__CalculateCodes(node.left, newVal)
        if (node.right):
            self.__CalculateCodes(node.right, newVal)

        if (not node.left and not node.right):
            self.codes[node.symbol] = newVal

    def __init__(self, text):
        nodeArray = self.__HuffmanNodesArray(text)

        # https://towardsdatascience.com/huffman-encoding-python-implementation-8448c3654328
        while len(nodeArray) > 1:
            nodeArray = sorted(nodeArray, key=lambda x: x.count)

            left = nodeArray[0]
            right = nodeArray[1]
            left.bit = '0'
            right.bit = '1'

            newNode = HuffmanNode(left.symbol + right.symbol, left.count + right.count, left, right)
            nodeArray.remove(left)
            nodeArray.remove(right)
            nodeArray.append(newNode)

        self.root = nodeArray[0]
        self.codes = dict()
        self.__CalculateCodes(self.root)

    def EncodeText(self, text):
        output = ''
        for x in text:
            output += self.codes[x]
        return output

    def DecodeText(self, encoded_data):
        huffman_tree = self.root
        decoded_output = []
        for x in encoded_data:
            if x == '1':
                huffman_tree = huffman_tree.right
            elif x == '0':
                huffman_tree = huffman_tree.left
            try:
                if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                    pass
            except AttributeError:
                decoded_output.append(huffman_tree.symbol)
                huffman_tree = self.root

        string = ''.join([str(item) for item in decoded_output])
        return string


# Input text to compress
text = "CUENTAN DE UN SABIO QUE UN DIA TAN TRISTE Y MISERO ESTABA QUE SOLO SE ALIMENTABA DE LAS HIERBAS QUE RECOGIA"

tree = HuffmanTree(text)
encodedText = tree.EncodeText(text)

print(tree.DecodeText(encodedText))

print("\nTamaño original = " + str(len(text) * 8) + " bytes")
print("Tamaño comprimido = " + str(len(encodedText)) + " bytes")
print("Relación de compresión = " + "{:.2f}".format(100 * len(encodedText) / (len(text) * 8)) + "%\n")
