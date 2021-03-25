from Crypto.Cipher import AES
import os
import base64

BLACKMAGIC = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
magicString = base64.b64decode(BLACKMAGIC)
magicKey = os.urandom(16)
ECBcipher = AES.new(magicKey, AES.MODE_ECB)

def pad(s, num):
	s += bytes([num])*num
	return s

def ECBoracle(plaintext):
	plaintext += magicString
	if len(plaintext) % 16:
		plaintext = pad(plaintext, 16 - len(plaintext) % 16)
	return ECBcipher.encrypt(plaintext)

def breakECB(oracle):
	# Discover the block size
	blockSize = 2
	pre = oracle(b'\x00\x00')
	while True:
		cur = oracle(b'\x00' * (blockSize + 1))
		if pre[:blockSize] == cur[:blockSize]:
			# Double check
			if oracle(b'\x01' * blockSize)[:blockSize] == oracle(b'\x01' * (blockSize + 1))[:blockSize]:
				break
		pre = cur
		blockSize += 1

	# Check if it is ECB
	res = oracle(b'\x00' * (blockSize * 2))
	if res[: blockSize] != res[blockSize: blockSize * 2]:
		print("Maybe not ECB.")
		return

	print(f"It is ECB with block size {blockSize}")
	# Actual breaking ECB cipher
	roughLength = len(oracle(b""))
	ans = []
	for i in range(roughLength):
		tmp = oracle(b'\x00' * (blockSize - 1 - i % blockSize))
		tmp = tmp[i // blockSize * blockSize: i // blockSize * blockSize + blockSize]
		block = []
		for j in range(i - blockSize + 1, i):
			if j < 0:
				block.append(0)
			else:
				block.append(ans[j])

		found = 0
		for last in range(256):
			res = oracle(bytes(block + [last]))
			if res[:blockSize] == tmp:
				ans.append(last)
				found = 1
				break
		if not found:
			return bytes(ans)[:-1] # ans has a trailing \x01 byte

print(breakECB(ECBoracle))

