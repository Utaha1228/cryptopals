from Crypto.Cipher import AES
import base64

def byteXor(a, b):
	if len(a) < len(b):
		a += b'\x00' * (len(b) - len(a))
	else:
		b += b'\x00' * (len(a) - len(b))
	return bytes([a[i]^b[i] for i in range(len(a))])

def cbcEncrypt(plaintext, key, iv = b'\x00' * 16):
	cipher = AES.new(key, AES.MODE_ECB)
	ciphertext = b""
	for i in range(0, len(plaintext), 16):
		iv = byteXor(iv, plaintext[i:min(i + 16, len(plaintext))])
		iv = cipher.encrypt(iv)
		ciphertext += iv
	return ciphertext

def cbcDecrypt(ciphertext, key, iv = b'\x00' * 16):
	cipher = AES.new(key, AES.MODE_ECB)
	blocks = []
	for i in range(0, len(ciphertext), 16):
		pre_block = iv if i == 0 else ciphertext[i-16:i]
		blocks.append(byteXor(cipher.decrypt(ciphertext[i:i+16]), pre_block))
	return b"".join(blocks)

ciphertext = open("text.txt", "r").read()
ciphertext = "".join(ciphertext.split('\n'))
ciphertext = base64.b64decode(ciphertext)

key = b"YELLOW SUBMARINE"
plaintext = cbcDecrypt(ciphertext, key)
print(plaintext)
