# Assembly

A CTFd compatible docker image for a web challenge. Scenario:

The Edison car company is trying to get their newest model to market ASAP but hackers hired by a rival manufacturer have apparently broken in and disabled several of the parts of the assembly line. Can you investigate and see if they left anything behind?

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.

## Solution

The page runs a WebAssembly binary (main.wasm) which handles secure communication with the backend PLC. Every 30 seconds, it sends an encrypted packet to /api/modbus and received an encrypted response. This response is then somehow used to mark the operational status of the five assembly line components.

Players can may attempt to fuzz the endpoint and will see descriptive error messages regarding proper base-64 encoding as well as AES-128-CBC decryption. Investigating the WebAssembly file, they will need to find the AES password which is embedded in plaintext. Once they do this, they are able to decrypt one of the encrypted packets and see that it is a modbus Read Holding Registers query, which requests registers 1-5 from device ID 1. Then, if the decrypt the response, they will see it is a modbus Read Holding Registers response, with the five requested register values [0,1,1,0,0].

The goal is for players to begin forging their own valid modbus requests to read other registers on the system, encrypting them, and passing them to the modbus endpoint. If they do this correctly, then they will be able to query values in those registers which are the characters of a message left behind by the hackers:

```Hackers were here! Also the flags is: USCG{r1d1ng_th3_bu5_t0_f1ag5}```


### Solution Code

The code below correctly encrypts a modbus payload to get registers 6-73 where the flag is hidden.

```python

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64
import requests
import struct

# Request register 6 - 73
data = b"\x01\x03\x00\x06\x00\x43\x00\x00"

# Random IV
iv = os.urandom(16)

key = b'SecurePassword1!'
cipher = AES.new(key, AES.MODE_CBC,iv=iv)

# Encrypt modbus packet
ciphertext = cipher.encrypt(pad(data,16))
payload = base64.b64encode(iv+ciphertext)

# Send to modbus endpoint
R = requests.post("http://127.0.0.1:1337/api/modbus",data=payload)

# Get back response and decrypt it
ciphertext = base64.b64decode(R.text)
cipher = AES.new(key, AES.MODE_CBC,iv=ciphertext[:16])
plaintext = unpad(cipher.decrypt(ciphertext[16:]),16)

# Unpack response as uint16 for each register
msg = struct.unpack_from(">%dH" % 67,plaintext,3)
print("".join(map(chr,msg)))
```