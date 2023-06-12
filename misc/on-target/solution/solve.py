import numpy as np
from pwn import *
import json
import time

class laser_guess:

    def __init__(self,x,y,dx,dy):

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def get_position(self,T):
        return [self.x + self.dx * T,self.y + self.dy * T]

C = remote("0.cloud.chals.io",32121)
x = C.recvuntil(b"enter coordinates:\n\n")

print(x.decode())

guesses = [laser_guess(np.random.randint(0,1000),
                       np.random.randint(0,1000),
                       np.random.randint(0,10),
                       np.random.randint(0,10)) for i in range(10)]

T = time.time()

T1 = 0

while T1 <= 5:

    T1 = time.time() - T

    positions = [g.get_position(T1) for g in guesses]

    # Send estimates
    C.sendline(json.dumps(positions).encode())

    #print("Sending: %s" % json.dumps(positions))

    # Get back distances
    resp = C.recv(1024).decode()

    #print(resp)

    if "USCG{" in resp:
        print(resp)
        exit()

    # Sort guessed by distance and save the top half

    try:
        d = json.loads(resp)
        print("Closest shot: %f" % sorted(d)[0])
        survivors = [x for _, x in sorted(zip(d,guesses))][:5]
    except Exception as e:
        print(e)
        exit()

    # Next generation
    new_guesses = survivors

    for i in range(5):

        # Choose two random parents
        p1, p2 = random.sample(survivors,2)

        # Create a new child from random parent attributes plus mutation noise
        child = laser_guess(random.choice([p1.x,p2.x]) + np.random.randint(-20,20),
                            random.choice([p1.y,p2.y]) + np.random.randint(-20,20),
                            random.choice([p1.dx,p2.dx]) + np.random.randint(-1,1),
                            random.choice([p1.dy,p2.dy]) + np.random.randint(-1,1))

        # Add to population
        new_guesses.append(child)

    guesses = new_guesses