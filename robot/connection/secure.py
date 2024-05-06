
from Crypto.Cipher import AES
import hashlib


def decrypt(data,key,iv):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.decrypt(data)


def encrypt(data,key,iv):
    # Pad data as needed
    data += " "*(16 - len(data) % 16)

    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.encrypt(bytes(data,"utf-8"))


def _hash(data):
    a = 37
    hash = 0
    for index, char in enumerate(data):
        hash += ord(char) * pow(a, index)
        hash %= 2147483647
    
    return hash

