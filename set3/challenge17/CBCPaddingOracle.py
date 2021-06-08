import os
from Crypto.Cipher import AES
import random
key = os.urandom(16)
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, IV=iv)

def pad(s, num):
	s += bytes([num])*num
	return s

def unpad(s):
	tmp = s[-1]
	assert s[-tmp:] == bytes([tmp] * tmp)
	return s[:-tmp]

def encrypt():
	ls = open("text.txt", "r").read().split('\n')
	plaintext = base64.b64decode(ls[random.randint(0, len(ls) - 1)])
