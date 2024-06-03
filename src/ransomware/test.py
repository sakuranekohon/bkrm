import heapq
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 霍夫曼編碼和解碼
class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(freq, symbol) for symbol, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0]

def build_codes(node, prefix="", codebook={}):
    if node.symbol is not None:
        codebook[node.symbol] = prefix
    else:
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text):
    tree = build_huffman_tree(text)
    codebook = build_codes(tree)
    encoded_text = ''.join(codebook[symbol] for symbol in text)
    return encoded_text, tree

def huffman_decode(encoded_text, tree):
    decoded_text = []
    node = tree
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.symbol is not None:
            decoded_text.append(node.symbol)
            node = tree
    return ''.join(decoded_text)

# AES加密和解密
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

# RSA加密和解密
def rsa_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)

# 示例使用
text = "this is an example for huffman encoding and AES encryption"
key = get_random_bytes(16)  # AES-128

# 生成RSA密鑰對
rsa_key = RSA.generate(2048)
private_key = rsa_key
public_key = rsa_key.publickey()

# 霍夫曼編碼
encoded_text, tree = huffman_encode(text)

# AES加密
encrypted_text = aes_encrypt(encoded_text, key)

# RSA加密AES密鑰
encrypted_key = rsa_encrypt(key, public_key)

# RSA解密AES密鑰
decrypted_key = rsa_decrypt(encrypted_key, private_key)

# AES解密
decrypted_encoded_text = aes_decrypt(encrypted_text, decrypted_key)

# 霍夫曼解碼
decoded_text = huffman_decode(decrypted_encoded_text, tree)

assert text == decoded_text
print("原文: ", text)
print("加密後: ", encrypted_text)
print("RSA加密的AES密鑰: ", encrypted_key)
print("解密後: ", decoded_text)
