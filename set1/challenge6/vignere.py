import base64

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

def vignereEncrypt(s, key): 
	return bytes([s[i] ^ key[i%len(key)] for i in range(len(s))])

def distance(s, t):
	score = 0
	for x, y in zip(s, t):
		tmp = x ^ y
		for j in range(8):
			if tmp & (1 << j):
				score += 1
	return score

def scoreKeySize(cipher, sz):
	return (distance(cipher[:sz], cipher[sz:sz+sz]) + distance(cipher[sz*2:sz*3], cipher[sz*3:sz*4])) / sz

def findKeySize(cipher):
	pos = []
	for sz in range(2, 40):
		pos.append((sz, scoreKeySize(cipher, sz)))
	pos.sort(key = lambda x: x[1])
	return [x[0] for x in pos]

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

cipher = open('text.txt').read()
cipher = "".join(cipher.split('\n'))
cipher = base64.b64decode(cipher)

keySize = findKeySize(cipher)
possible_answer = []
for sz in keySize[:10]:
	res, key = solveVignere(cipher, sz)
	possible_answer.append((res, getScore(res), key))

possible_answer.sort(key = lambda x: x[1], reverse = True)
for ans in possible_answer:
	print(ans[2], ans[1])
	print(ans[0])
