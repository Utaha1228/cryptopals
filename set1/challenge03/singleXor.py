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
		pos.append((res, getScore(res)))
	pos.sort(key = lambda x: x[1], reverse = True)
	return pos

def solve(s):
	s = bytes.fromhex(s)
	res = solveSingleXor(s)
	if len(res) > 5:
		res = res[:5]
	for x in res:
		print(x[0], x[1])

inputString = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
solve(inputString)