import base64
import os
from Crypto.Cipher import AES
from Crypto.Util import Counter
freq = {
    'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
    'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
    'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
    'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
    'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
    'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
    'y': .01974, 'z': .00074, '$': .00000
}
def getScore(s): # s : bytes
	myFreq = {}
	for i in freq.keys():
		myFreq[i] = 0

	validChrCount = 0
	for c in s:
		c = chr(c)
		if c in " '\"":
			continue

		validChrCount += 1
		if c.lower() in myFreq.keys():
			myFreq[c.lower()] += 1
		else:
			myFreq['$'] += 1
	for key in myFreq.keys():
		myFreq[key] /= validChrCount

	score = 1
	for c in freq:
		score -= (freq[c] - myFreq[c]) * (freq[c] - myFreq[c])
	return score

def solveSingleXor(s):
	pos = []
	for key in range(256):
		res = bytes([s[i]^key for i in range(len(s))])
		pos.append((res, getScore(res), key))
	pos.sort(key = lambda x: x[1], reverse = True)
	return pos[0]


def solveVignere(cipher, sz):
	key = []
	ans = [0] * len(cipher)
	for i in range(sz):
		part = []
		for j in range(i, len(cipher), sz):
			part.append(cipher[j])
		res, _, k = solveSingleXor(bytes(part))
		key.append(k)
		idx = i
		for j in res:
			ans[idx] = j
			idx += sz
	return (bytes(ans), bytes(key))

def sxor(a, b):
	return bytes([a[i] ^ b[i] for i in range(len(b))])

def solve(ls):
	l = min([len(s) for s in ls])
	ciphertext = b"".join([s[:l] for s in ls])

	_, key = solveVignere(ciphertext, l)
	for s in ls:
		print(sxor(s, key))


inputString = open("text.txt", "r").read().split('\n')
key = os.urandom(16)
nonce = os.urandom(8)
ls = []
for s in inputString:
	cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(64, prefix=nonce))
	ls.append(cipher.encrypt(base64.b64decode(s)))

solve(ls)