from Crypto.Cipher import AES
import base64

def solve(ciphertext, key):
	cipher = AES.new(key, AES.MODE_ECB)
	plaintext = cipher.decrypt(ciphertext)
	print(plaintext)

inputString = open("text.txt", "r").read()
ciphertext = bytes("".join(inputString.split('\n')), 'utf_8')
ciphertext = base64.b64decode(ciphertext)
key = b'YELLOW SUBMARINE'
solve(ciphertext, key)