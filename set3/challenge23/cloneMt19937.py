class mt19937:
	def __init__(self, seed):
		(mt19937.w, mt19937.n, mt19937.m, mt19937.r) = (32, 624, 397, 31)
		mt19937.a = 0x9908B0DF
		(mt19937.u, mt19937.d) = (11, 0xFFFFFFFF)
		(mt19937.s, mt19937.b) = (7, 0x9D2C5680)
		(mt19937.t, mt19937.c) = (15, 0xEFC60000)
		mt19937.l = 18
		self.states = [seed]
		mt19937.lowerMask = (1 << mt19937.r) - 1
		mt19937.mask = (1 << mt19937.w) - 1
		mt19937.upperMask = mt19937.mask ^ mt19937.lowerMask
		self.index = mt19937.n
		mt19937.f = 1812433253

		for i in range(1, self.n):
			self.states.append(self.mask & (i + self.f * (self.states[i-1] ^ (self.states[i-1] >> (self.w - 2)))))

	def temper(self,num):
		num = num ^ ((num >> mt19937.u) & mt19937.d)
		# num = num ^ ((num << mt19937.s) & mt19937.b)
		# num = num ^ ((num << mt19937.t) & mt19937.c)
		# num = num ^ (num >> mt19937.l)
		return num
		
	def rand(self):
		if self.index >= mt19937.n:
			self.twist()
		y = self.states[self.index]
		self.index += 1
		return self.temper(y)

	def twist(self):
		for i in range(mt19937.n):
			x = (self.states[i] & mt19937.upperMask) ^ (self.states[(i + 1) % mt19937.n] & mt19937.lowerMask)
			xA = x >> 1
			if x & 1:
				xA = xA ^ self.a

			self.states[i] = self.states[(i + mt19937.m) % mt19937.n] ^ xA

		self.index = 0

def untemper(num):
	# num = num ^ (num >> mt19937.l)
	# for _ in range(2):
	# 	num = num ^ ((num << mt19937.t) & mt19937.c)
	# for _ in range(5):
	# 	num = num ^ ((num << mt19937.s) & mt19937.b)
	for _ in range(3):
		num = num ^ (num >> mt19937.u * (_ + 1))
	return num

import random
def testUntemper():
	rng = mt19937(0)
	for i in range(10):
		num = random.randint(0, (1<<32) - 1)
		print(untemper(rng.temper(num)) == num)

testUntemper()
