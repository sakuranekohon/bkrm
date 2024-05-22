from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def generate_aes_key(length=32):
    """生成AES密钥"""
    return os.urandom(length)

def aes_encrypt(data, key):
    """使用AES加密"""
    # 生成一个随机的初始向量
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 使用PKCS7填充
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # 加密数据
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def aes_decrypt(encrypted_data, key):
    """使用AES解密"""
    # 分离初始向量和加密数据
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密数据
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # 去除填充
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

def main():
    # 原始消息
    message = "AA"
    message_bytes = message.encode('utf-8')

    # 生成密钥
    key = generate_aes_key()

    # 加密消息
    encrypted_message = aes_encrypt(message_bytes, key)
    print("Encrypted message:", encrypted_message)

    # 解密消息
    decrypted_message = aes_decrypt(encrypted_message, key)
    print("Decrypted message:", decrypted_message.decode('utf-8'))

if __name__ == "__main__":
    main()
