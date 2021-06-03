def solve(s):
	s = bytes.fromhex(s)
	t = bytes.fromhex("686974207468652062756c6c277320657965")
	res = bytes([s[i]^t[i] for i in range(len(s))])
	print(res.hex())

inputString = "1c0111001f010100061a024b53535009181c"
solve(inputString)