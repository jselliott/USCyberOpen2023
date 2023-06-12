# Semaphore

Bob's Donut Factory has suspected for a while that competitors have been sending hackers into the facility to try to gain access to their precious secrets recipes. The SOC capture some suspicious traffic coming from a workstation going to a smart thermostat of all places. The compromised thermostat has been shut down to prevent it being used as a pivot point but we'd like to know what message, if any, was sent to the outside.

## Provided Files

* [semaphore.pcap](semaphore.pcap)

## Solution

Examining the provided PCAP file, it is obvious that something weird is going on. There are lots of red markings everywhere and invalid packets being sent. Some research will reveal that it is because of a lot of TCP flags that are not set to standard. The solution is that the TCP flags are being set to the bits corresponding to ASCII letters.

After running a script or using tshasrk to extract all of the TCP flags from the capture, the player is able to convert the bits back to ASCII and find a base64 encoded message that had been sent.


### Solution Code

```python
from scapy.all import wrpcap, Ether, IP, TCP
import base64

from scapy.all import *

flags = ["C","E","U","A","P","R","S","F"]

cap = rdpcap('semaphore.pcap')

output = ""

for packet in cap:
    f = packet[TCP].flags
    output += chr(int("".join(["1" if flag in f else "0" for flag in flags]),2))

print(base64.b64decode(output))

```