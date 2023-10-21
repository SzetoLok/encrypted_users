#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
"""
AES key and iv used to encrypt and decrypt
"""
key = b'Forest landscape'
iv = b'An orange banana'
segment_size = 128
block_size = 16
def pad_string(s: str, multiple: int) -> str:
    extra = len(s) % multiple
    if extra > 0:
        s += ' ' * (multiple - extra)
    return s
def encrypt(plaintext: str) -> str:
    """
    Encrypt a plaintext, and base64encode bytes (plaintext -> cipher bytes -> base64encoded str)
    :param plaintext: string of plaintext to encrypt
    :return: cipher text
    """
    encryption_suite = AES.new(key, AES.MODE_CFB, iv, segment_size=segment_size)
    plaintext = pad_string(plaintext, block_size)
    cipher_text = encryption_suite.encrypt(bytes(plaintext,'utf-8'))
    return b64encode(cipher_text).decode('utf8')
def decrypt(cipher_text: str) -> str:
    """
    Decrypt cipher that's encrypted by the "encrypt" method
    :param cipher_text:
    :return: decrypted plain text
    """
    cipher_text = b64decode(cipher_text)
    decryption_suite = AES.new(key, AES.MODE_CFB, iv, segment_size=segment_size)
    return decryption_suite.decrypt(cipher_text).decode('utf8').rstrip(' ')
def test():
    # Have a test
    plaintext = '1 - Cole'
    cipher_text = encrypt(plaintext)
    decrypted_text = decrypt(cipher_text)
    print(plaintext, decrypted_text)
    assert plaintext == decrypted_text
    print(decrypt('vPMXltcUQWd9jkF49sP5Zfd/d3I/TxLIcNlWoSSGG7k='))
if __name__ == '__main__':
    test()