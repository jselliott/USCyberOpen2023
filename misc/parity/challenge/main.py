import numpy as np
import random
import time

flag = b"USCG{fl1pp1ng_s0m3_b1t5}"
msg = b"--- BEGINNING USCG JOKE COMMUNICATION ---\n\nThere are 10 types of people in this world. Those who understand binary and those who don't.\n\nAlso the flag is %s\n\n--- END USCG JOKE COMMUNICATION ---\n\n" % flag


def char_to_binary_vector(c):
    return [1 if x == "1" else 0 for x in '{0:08b}'.format(c)]

pos = 0

# Hamming 8,4 code with extra parity bit
def encode_vector(v):

    x = v + [0,0,0,0]
    x[4] = x[0] ^ x[2] ^ x[3]
    x[5] = x[0] ^ x[1] ^ x[3]
    x[6] = x[0] ^ x[1] ^ x[2]
    x[7] = x[0] ^ x[1] ^ x[2] ^ x[3] ^ x[4] ^ x[5] ^ x[6]

    # Random noise
    idx = random.randint(0,7)
    x[idx] = (x[idx]+1)%2

    return x

while True:

    C1 = msg[pos%len(msg)]

    C = char_to_binary_vector(C1)

    c1 = C[:4]
    c2 = C[4:]

    x1 = encode_vector(c1)
    x2 = encode_vector(c2)
    
    print("".join(map(str,x1)))
    print("".join(map(str,x2)))
    pos += 1