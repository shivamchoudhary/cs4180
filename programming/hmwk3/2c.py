import sys
import os
import logging
import random
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

class Packet(object):
	def __init__(self, sport,dport):
		"""
			
		"""
		self.sport = sport
		self.dport = dport
                self.loopback ="127.0.0.1"

	def sendTCP(self):
		""" Part (a) sending TCP packets
		"""
                for i in range(3000,3020):
                    send(IP(dst=self.loopback)/TCP(dport=i))
	def sendRandom(self):
		"""Part(c)  sending random TCP packets
		"""
		for i in range(5):
			randomstr = "".join(random.choice(string.letters) for i in range(10))
			send(IP(dst=self.loopback)/TCP(sport=int(self.sport),dport=int(self.dport))/Raw(load=randomstr)	



def main():
	try:
		sport = sys.argv[1]
		dport = sys.argv[2]	
	except IndexError:
		print "Error: Run as python <c1.py> <source_port> <dst_port> "	
		exit(0)
	p = Packet(sport,dport)
if __name__=="__main__":
	main()