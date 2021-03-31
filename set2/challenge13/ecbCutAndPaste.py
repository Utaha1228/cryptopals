from Crypto.Cipher import AES
import os
KEY = os.urandom(16)
cipher = AES.new(KEY, AES.MODE_ECB)

def profile_for(email):
	email.replace('&', '')
	email.replace('=', '')
	return {
		'email': email,
		'uid': 10,
		'role': 'user'
	}

def encodeToString(e):
	ret = ""
	for key in e.keys():
		ret += str(key) + "=" + str(e[key]) + "&"
	ret = ret[:-1]
	return ret

def decodeToJSON(s):
	ret = {}
	a = s.split('&')
	for t in a:
		idx = t.find('=')
		ret[t[:idx]] = t[idx+1:]
	return ret

def padding(s, num):
	s += bytes([num])*num
	return s

def ecbEncrypt(s):
	if type(s) == str:
		s = s.encode('utf-8')
	if len(s) % 16:
		s = padding(s, 16 - len(s) % 16)
	return cipher.encrypt(s)

def ecbDecrypt(s):
	ret = cipher.decrypt(s)
	# unpad
	tmp = ret[-1]
	if ret[-tmp:] == bytes([tmp] * tmp):
		ret = ret[:-tmp]
	return ret.decode('utf-8')

def forge():
	# email=AAAAAAAAAA admin\x11... BBB&uid=10&role= user
	magic = "A" * 10 + "admin" + "\x0B" * 11 + 'B' * 3
	magic = encodeToString(profile_for(magic))
	cip = ecbEncrypt(magic)
	myForge = cip[:16] + cip[32:48] + cip[16:32]
	dec = ecbDecrypt(myForge)
	print(decodeToJSON(dec))

forge()