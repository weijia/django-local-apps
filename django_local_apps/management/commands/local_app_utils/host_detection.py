import netifaces as ni
from socket import *
from time import sleep

# from PyQt4.QtNetwork import QNetworkInterface
#
# all_Addresses = QNetworkInterface.allAddresses()    #list-of-QHostAddress
#
# for addr in all_Addresses:
#     print(addr.toString())


for i in ni.interfaces():
    interface = ni.ifaddresses(i)
    if 2 in interface:
        print interface
        print interface[2][0]["addr"]


cs = socket(AF_INET, SOCK_DGRAM)
cs.bind(("192.168.8.120", 0))
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# while True:
#     cs.sendto('This is a test', ('255.255.255.255', 988))
#     sleep(10)
