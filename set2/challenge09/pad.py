def pad(s, num):
	s += bytes([num])*num
	return s

print(pad(b"YELLOW SUBMARINE", 4))