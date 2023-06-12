import random
import string

letters = [ord(x) for x in string.ascii_uppercase]
indexes = [x for x in range(65,91)]

random.shuffle(indexes)

mapping = {}

for i in range(len(indexes)):
    mapping[letters[i]] = indexes[i]

letters = [ord(x) for x in string.ascii_lowercase]
indexes = [x for x in range(97,123)]
random.shuffle(indexes)

for i in range(len(indexes)):
    mapping[letters[i]] = indexes[i]

with open("rumble","rb") as F:
    with open("jumble","wb") as output:
        content = [b for b in F.read()]

        for c in content:
            if c in mapping:
                output.write(mapping[c].to_bytes(1,'big'))
            else:
                output.write(c.to_bytes(1,'big'))


