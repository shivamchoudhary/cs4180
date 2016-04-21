"""
prob 2b
Program to send HTTP GET messages.
"""

__author__ = "Shivam Choudhary"
__uni__    = "sc3973"



from scapy.all import *
import binascii
import ConfigParser,os
config = ConfigParser.RawConfigParser()

class SendGet(object):
        """
            Send HTTP GET request to the server.
        """
	def __init__(self):
		config.read('inpartb.txt') #opens the inpartb.txt file
		self.saddress = config.get('ipaddress','src_address')
		self.daddress = config.get('ipaddress','dst_address') 
		self.payload = config.get('payload','getmessage')
		self.send_packet()
	def send_packet(self):
                """
                Send the packet based on inputs.
                """
		a = IP(src=self.saddress,dst=self.daddress) #Create IP packet
		b = TCP(dport=int(config.get('ipaddress','dst')),
                        sport=int(config.get('ipaddress','source')))
		#Attach the payload to the layered packet
                packet = a/b/Raw(load=binascii.unhexlify(self.payload))
		packet.show()
		print str(packet)
		send(packet)

def main():
	s = SendGet()
	



if __name__=="__main__":
	main()
