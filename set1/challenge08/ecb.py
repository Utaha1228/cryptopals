def solve(ls):
	for s in ls:
		flag = 0
		st = set({})
		for i in range(0, len(s), 16):
			st.add(s[i:i+16])
		if len(st) != len(s) // 16:
			print(s)

inputList = open('text.txt', 'r').read().split('\n')
inputList = map(bytes.fromhex, inputList)
solve(inputList)