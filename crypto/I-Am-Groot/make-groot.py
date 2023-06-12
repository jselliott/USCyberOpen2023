import base64
import random
import io
import zipfile

infile = open("groot.zip","rb")
output = open("groot.txt","wb")

for f in infile.read():

    out = b" ".join([b"I am Groot."] * random.randint(0,10))
    idx = random.randint(0,len(out))
    x = b"\xef\xbb\xbf"+b"".join([b"\xe2\x80\x8c" if a == "1" else b"\xe2\x80\x8b" for a in bin(f)[2:].zfill(8)])+b"\xef\xbb\xbf"
    out = out[:idx] + x + out[idx:]

    output.write(out+b"\n")

