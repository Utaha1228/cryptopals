from Crypto.Cipher import AES
import os
import base64

def ctrDecrypt(s, key, nonce):
	cipher = AES.new(key, AES.MODE_ECB)
	keyStream = b""
	cnt = 0
	plainList = []
	for pt in range(len(s)):
		if pt >= len(keyStream):
			keyStream += cipher.encrypt(nonce + cnt.to_bytes(8, byteorder="little"))
			cnt += 1

		plainList.append(keyStream[pt] ^ s[pt])
	plaintext = bytes(plainList)
	print(plaintext)

inputString = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
inputString = base64.b64decode(inputString)
key = "YELLOW SUBMARINE"
nonce = b"\x00" * 8
ctrDecrypt(inputString, key, nonce)