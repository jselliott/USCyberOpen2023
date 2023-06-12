# The Final Countdown

A CTFd compatible docker image for a web challenge. Scenario:

The US Cyber Games program has decided to celebrate the final 24 hours of the competition with a little flag lottery. However, the odds seem just about impossible! Maybe you can find a way to game the system and win the prize!

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.

## Solution

Players will likely attempt a number of different techniques to try to crack the PRNG by capturing numbers or using the end time as a seed, etc. The actual vulnerability is that there is an expose .git folder which allows them to download lottery.py which contains the logic for the number drawing.

```python
import pyotp
import random
import time

class Lottery:

    def __init__(self):

        self.SECRET = "JBSWY3DPEHPK3PXP"

    def draw(self):

        #TOTP allows us to have the same number for a 30 second interval
        totp = pyotp.TOTP(self.SECRET)
        seed = totp.now()
        random.seed(seed)
        return random.randint(0,1000000)
    
    def last_n_draws(self,num_draws):

        curtime = int(time.time())
        totp = pyotp.TOTP(self.SECRET)

        ret = []

        for i in range(1,num_draws+1):
            seed = totp.at(curtime-(30*i))
            random.seed(seed)
            ret.append(random.randint(0,1000000))
        
        return ret
```

The app uses a time-based one time password (TOTP) with a secret to generate a new code every 30 seconds, and then uses that to generate a new random number. This allows us to change the magic number in a predictable way every 30 seconds. However, with this leak, the player can simply generate the current number themselves and submit it to win the flag. The lesson is to always use an addon like DotGit in your browser during CTF competitions in case the developer exposed the folder as part of the challenge or even by accident. You can also check this vulnerability by always checking "/.git/HEAD" as part of your enumeration. If the file exists then you're in business....