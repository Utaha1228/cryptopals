from Crypto.Cipher import AES
import os
import base64
import random

RANDOMPREFIX = os.urandom(random.randint(0, 127))
print(f"SECRET!!! The prefix length is {len(RANDOMPREFIX)}")
BLACKMAGIC = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
magicString = base64.b64decode(BLACKMAGIC)
magicKey = os.urandom(16)
ECBcipher = AES.new(magicKey, AES.MODE_ECB)

def pad(s, num):
	s += bytes([num])*num
	return s

def ECBoracle(plaintext):
	plaintext = RANDOMPREFIX + plaintext + magicString
	if len(plaintext) % 16:
		plaintext = pad(plaintext, 16 - len(plaintext) % 16)
	return ECBcipher.encrypt(plaintext)

def breakECB(oracle):
	zeroBlock = b""
	firstAppearance = -1
	# Discover the block size

	blockSize = 2
	test = oracle(b'\x00' * 1000)
	while blockSize < 30:
		for i in range(0, len(test) - 3 * blockSize + 1, blockSize):
			if test[i: i + blockSize] == test[i + blockSize: i + blockSize * 2] and test[i + blockSize: i + blockSize * 2] == test[i + blockSize * 2: i + blockSize * 3]:
				zeroBlock = test[i: i + blockSize]
				firstAppearance = i
				break
		if firstAppearance != -1:
			break
		blockSize += 1

	# Find prefix length
	prefixLen = firstAppearance
	for i in range(blockSize):
		test = oracle(b'\x00' * (blockSize + i))
		if test[firstAppearance: firstAppearance + blockSize] == zeroBlock:
			break
		prefixLen -= 1

	print(prefixLen)

	def newOracle(s):
		tmp = blockSize - prefixLen % blockSize
		res = oracle(b'\x00' * tmp + s)
		return res[prefixLen + tmp:]

	# Actual breaking ECB cipher
	roughLength = len(oracle(b"")) - prefixLen
	ans = []
	for i in range(roughLength):
		tmp = newOracle(b'\x00' * (blockSize - 1 - i % blockSize))
		tmp = tmp[i // blockSize * blockSize: i // blockSize * blockSize + blockSize]
		block = []
		for j in range(i - blockSize + 1, i):
			if j < 0:
				block.append(0)
			else:
				block.append(ans[j])

		found = 0
		for last in range(256):
			res = newOracle(bytes(block + [last]))
			if res[:blockSize] == tmp:
				ans.append(last)
				found = 1
				break
		if not found:
			return bytes(ans)[:-1] # ans has a trailing \x01 byte

print(breakECB(ECBoracle))

