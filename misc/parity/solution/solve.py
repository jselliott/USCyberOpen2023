from pwn import *
import numpy as np

C = remote("0.cloud.chals.io",21396)

buffer = []


E = {"001":6,
     "010":5,
     "011":1,
     "100":4,
     "101":2,
     "110":3,
     "111":0}


while True:

    x = C.recvline().strip().decode()
    x = [1 if y == "1" else 0 for y in x]

    #print(x)

    c1 = x[4] ^ x[3] ^ x[2] ^ x[0]
    c2 = x[5] ^ x[0] ^ x[1] ^ x[3]
    c3 = x[6] ^ x[0] ^ x[1] ^ x[2]

    #print(c1,c2,c3)

    if sum([c1,c2,c3]) != 0:
        idx = E["%d%d%d" % (c1,c2,c3)]
        x[idx] = (x[idx] + 1) % 2

    buffer = buffer + x[:4]

    if len(buffer) == 8:

        x = int("".join(map(str,buffer)),2)
        print(chr(x),end="")
        buffer = []

    time.sleep(0.05)
    #exit()
