def vignereEncrypt(s, key): 
	return bytes([s[i] ^ key[i%len(key)] for i in range(len(s))])

plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"
print(vignereEncrypt(plaintext.encode('utf-8'), key).hex())