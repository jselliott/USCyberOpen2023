import random
import math
import socket
import time
import json

FLAG = open("/flag.txt","r").read()


print("Connected to USCG Earth Orbital Defense Platform...\n")
print("*** WARNING: Asteroid Strike Imminent in T-5 seconds ***")
print("Recommend defensive fire. Input coordinates for laser bombardment.\n")
print("Laser Field of View (meters): 0 <= x <= 1000, 0 <= y <= 1000")
print("Entry format (Aiming coordinates): [[x1,y1],[x2,y2].....[x10,y10]]")
print("Response format (Distance from target): [d1,d2....d10]")

T = time.time()

# Random position near the center of the view
x = 500 + random.randint(-50,50)
y = 500 + random.randint(-50,50)

# Random velocity
dX = random.randint(-10,10)
dY = random.randint(-10,10)

# How close do they need to be to hit
DISTANCE_THRESHHOLD = 5

dT = 0

print("\n\nBegin targeting sequence, please enter coordinates:\n")

while True:

    resp = input("")

    dT = time.time() - T

    if dT >= 5:
        print("ASTEROID IMPACT DETECTED! Mission failed....")

    x1 = x + (dX * dT)
    y1 = y + (dY * dT)

    C = []

    try:
        C = json.loads(resp)

        if len(C) != 10:
            print("Incorrect number of coordinates (laser array has 10 guns). Mission failed....")
            exit()

        if any([x2 < 0 or x2 > 1000 or y2 < 0 or y2 > 1000 for x2,y2 in C]):
            print("Coordinates out of valid range (0-1000,0-1000). Mission failed....")
            exit()

        D = [math.sqrt(pow(x2-x1, 2)+pow(y2-y1, 2)) for x2, y2 in C]

        hit_target = False

        for d in D:
            if d <= DISTANCE_THRESHHOLD:
                hit_target = True
        
        if hit_target:
            print("\n\nTARGET DESTROYED! Great work!\n\nFlag: %s" % FLAG)
            exit()

        print(json.dumps(D))

    except json.JSONDecodeError:
        print("Invalid input formatting. Mission failed....")
        exit()
    except Exception as e:
        print("Input error. Mission failed....")
        exit()