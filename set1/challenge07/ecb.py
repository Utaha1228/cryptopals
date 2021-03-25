from Crypto.Cipher import AES
import base64
key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)

ciphertext = open("text.txt", "r").read()
ciphertext = bytes("".join(ciphertext.split('\n')), 'utf_8')
ciphertext = base64.b64decode(ciphertext)

plaintext = cipher.decrypt(ciphertext)
print(plaintext)