import re

X = open("groot.txt","rb").read()

matches = re.findall(b"\xef\xbb\xbf(.{24})\xef\xbb\xbf",X)

for m in matches:
    m = m.replace(b"\xe2\x80\x8b",b"0")
    m = m.replace(b"\xe2\x80\x8c",b"1")
    print(hex(int(m,2))[2:].zfill(2),end="")