def padding(s, num):
	s += bytes([num])*num
	return s

print(padding(b"YELLOW SUBMARINE", 4))