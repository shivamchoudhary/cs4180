from scapy.all import *
import ConfigParser,os
config = ConfigParser.RawConfigParser()

class SendGet(object):
	def __init__(self):
		config.read('inpartb.txt')
		self.saddress = config.get('ipaddress','src_address')
		self.daddress = config.get('ipaddress','dst_address') 
		self.payload = config.get('payload','getmessage')
		self.send_packet()
	def send_packet(self):
		a = IP(src=self.saddress,dst=self.daddress)
		b = TCP(dport=int(config.get('ipaddress','dst')),sport=int(config.get('ipaddress','source')))
		packet = a/b/Raw(load=(self.payload))
		packet.show()
		str(packet)
def main():
	s = SendGet()
	



if __name__=="__main__":
	main()
