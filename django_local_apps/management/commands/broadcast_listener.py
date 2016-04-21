#!/usr/bin/python
from socket import *
from django.core.management import BaseCommand


class BroadcastListener(BaseCommand):
    def handle(self, *args, **options):
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.bind(('192.168.8.120', 988))
        while True:
            data, address = cs.recvfrom(1024)
            print ':received:', data, "from ", address
            if data == "HLK":
                cs.sendto("HLK-RM(V1.78(Jul 23))", address)


Command = BroadcastListener
