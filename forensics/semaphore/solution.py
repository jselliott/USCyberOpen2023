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
