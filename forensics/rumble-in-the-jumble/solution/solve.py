import struct

X = open("jumble","rb").read()
for i in range(len(X)-256):
    window = X[i:i+256]
    if len(set(window)) == 256:

        mapping = {}

        for j in range(256):
            mapping[window[j]] = j

        with open("fixed","wb") as output:
            for x in X:
                output.write(struct.pack(">B",mapping[x]))
        exit()