import sys
import os
from scapy.all import *

def send_data(ip):
	try:
		p = sr1(IP(dst=sys.argv[1])/ICMP()/Raw(load="TEST"))
	except socket.error:
		print "Can't open socket maybe you are not root?"
		exit(0)
	if p:
		p.show()
def main():
	try:
		ip = sys.argv[1]
	except IndexError:
		print "Error: Provide IP address"
		exit(0)
	send_data(ip)
		

if __name__=="__main__":
	main()

