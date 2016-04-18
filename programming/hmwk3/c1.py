import sys
import os
import logging
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




def main():
	try:
		sport = sys.argv[1]
		dport = sys.argv[2]	
	except IndexError:
		print "Error: Run as python <c1.py> <source_port> <dst_port> "	
		exit(0)
if __name__=="__main__":
	main()
