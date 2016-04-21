from socket import *
from time import sleep

cs = socket(AF_INET, SOCK_DGRAM)
cs.bind(("192.168.8.238",0))
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    cs.sendto('Detection', ('255.255.255.255', 988))
    sleep(10)
