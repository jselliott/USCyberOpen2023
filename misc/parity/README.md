# Parity

A CTFd compatible docker image for a misc challenge. Scenario: 

Dr. Brown said he wanted to send me a funny joke (he's always hamming it up during competition), but he wanted to be sure that it wasn't going to get corrupted by any stray cosmic rays or anything in transit. His server is broadcasting the joke but I can't seem to decode the message. Maybe you could give it a try?

He mentioned something about 4 data bits and 4 parity bits...

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.

## Solution

This is a bit of a programming challenge and an opportunity to learn about signal processing and automatic error correction. Doing a little research into [Hamming Codes](https://en.wikipedia.org/wiki/Hamming_code), you'll find that they are used for automatic error correction and add parity bits to blocks of data. Using some clever math, it allows the receiver to know at the other end if the signal has somehow been corrupted and correct it before reconstructing the original data.

Each line that is sent is a series of 8 binary digits which comprise the four data bits along with four parity bits for error correction. Each line has an error in it so that correction is mandatory in order to get the flag. The code below checks the parity bits and makes corrections before printing out the message as it is received.

```python

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
```

