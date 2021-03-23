import base64
s = bytes.fromhex(input())
print(base64.b64encode(s))