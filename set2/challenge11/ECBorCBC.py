from Crypto.Cipher import AES
import os
import random

def padding(s, num):
	s += bytes([num])*num
	return s

def myEncrypt(plaintext):
	key = os.urandom(16)

	plaintext += os.urandom(random.randint(5, 10))
	plaintext = os.urandom(random.randint(5, 10)) + plaintext

	plaintext = padding(plaintext, 16 - len(plaintext) % 16)

	tp = random.randint(0, 1)
	cipher = AES.new(key, AES.MODE_ECB if tp else AES.MODE_CBC, IV = os.urandom(16))
	return (cipher.encrypt(plaintext), "ECB" if tp else "CBC")

def myGuess(ciphertext):
	flag = 0
	for i in range(0, len(ciphertext), 16):
		for j in range(i+16, len(ciphertext), 16):
			if ciphertext[i:i+16] == ciphertext[j:j+16]:
				flag = 1

	return 'ECB' if flag else 'CBC'

def Guess():
	plaintext = b'A' * 64
	ciphertext, answer = myEncrypt(plaintext)
	guess = myGuess(ciphertext)
	print(answer, guess)
	return 1 if answer == guess else 0

T = 10000
cnt = 0
for i in range(T):
	cnt += Guess()

print(cnt)
