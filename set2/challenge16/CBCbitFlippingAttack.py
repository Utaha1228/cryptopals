import os
from Crypto.Cipher import AES
key = os.urandom(16)
iv = os.urandom(16)
def pad(s, num):
	s += bytes([num])*num
	return s

def unpad(s):
	tmp = s[-1]
	assert s[-tmp:] == bytes([tmp] * tmp)
	return s[:-tmp]

def encrypt(s):
	if type(s) == str:
		s = bytes.decode(s, "utf-8")
	cipher = AES.new(key, AES.MODE_CBC, IV=iv)
	s.replace(b';', b'')
	s.replace(b'=', b'')
	s = b"comment1=cooking%20MCs;userdata=" + s + b";comment2=%20like%20a%20pound%20of%20bacon"
	s = pad(s, 16 - len(s) % 16) # pad at least one byte
	return cipher.encrypt(s)

def decrypt(s):
	assert len(s) % 16 == 0
	cipher = AES.new(key, AES.MODE_CBC, IV=iv)
	res = cipher.decrypt(s)
	if res.find(b";admin=true;"):
		print("Successful Hack!")
		exit(0)

def solve():
	'''
	comment1=cooking
	%20MCs;userdata=
	****************
	*****;admin=true
	;comment2=%20lik
	'''
	magicString = b"*********************:admin<true"
	assert len(magicString) == 32

	ciphertext = encrypt(magicString)
	ls = list(ciphertext)
	ls[16 * 2 + 5] ^= 1
	ls[16 * 2 + 11] ^= 1
	newCiphertext = bytes(ls)
	decrypt(newCiphertext)

solve()