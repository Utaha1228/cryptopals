import base64

def solve(s):
	s = bytes.fromhex(s)
	print(base64.b64encode(s))

inputString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
solve(inputString)