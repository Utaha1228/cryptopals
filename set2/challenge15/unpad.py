def unpad(s):
	tmp = s[-1]
	assert s[-tmp:] == bytes([tmp] * tmp)
	return s[:-tmp]

print(unpad(b"abc\x02\x02"))