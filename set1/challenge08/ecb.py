ls = open('text.txt', 'r').read().split('\n')
ls = map(bytes.fromhex, ls)
for s in ls:
	assert len(s) == 160
	flag = 0
	for i in range(0, len(s), 16):
		for j in range(i+16, len(s), 16):
			if s[i:i+16] == s[j:j+16]:
				flag = 1
	if flag:
		print(s)