from scapy.all import wrpcap, Ether, IP, TCP
import random
import base64

flag = "USCG{s3map4h0r3_tcp_f1ag5}"

message = "Good afternoon, crew! We are nearing our mission objective of stealing the secret recipe for our client. We've had several setbacks but should be able to exfiltrate it out of the secure network soon. The weather has been pretty nice here. Anyone do anything fun this weekend? Oh, before I forget, the flag is: %s" % flag
message = base64.b64encode(message.encode())

packets = []

flags = ["C","E","U","A","P","R","S","F"]

for m in message:
    bits = bin(m)[2:].zfill(8)
    f = "".join([flags[i] for i in range(8) if bits[i]=="1"])
    packet = Ether() / IP(src="10.10.0.180",dst="10.10.0.99") / TCP(sport=random.randint(50000,60000),dport=1337,flags=f)
    packets.append(packet)

wrpcap('semaphore.pcap',packets)