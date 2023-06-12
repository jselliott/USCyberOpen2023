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
