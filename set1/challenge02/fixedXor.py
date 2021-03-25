s = bytes.fromhex(input())
t = bytes.fromhex("686974207468652062756c6c277320657965")

res = bytes([s[i]^t[i] for i in range(len(s))])
print(res.hex())