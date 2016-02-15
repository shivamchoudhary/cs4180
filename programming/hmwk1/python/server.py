import argparse
import sys
import Common
import socket
class Server(object):
    def __init__(self,port):
        """
        Initializing the Server Socket and binding it on the port.
        """
        self.host ="localhost"
        self.port = port
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            serversocket.bind((self.host,self.port))
        except socket.error as error:
            print ("Socket binding failed with %s",error)
        # Allowing only one(1) Client to connect.
        serversocket.listen(1)
        (clientsocket,clientaddress) = serversocket.accept()
    
        self.recv_data(clientsocket)
    def recv_data(self,clientsocket):
        data = clientsocket.recv(1024)
        with open('recv.enc','wb')as fname:
            fname.write(data)
        self.decrypt()
        clientsocket.close()
    def decrypt(self):
        Common.decrypt_file('shivamchoudhary1','recv.enc')


def main():
    try:
        port = int(sys.argv[1])
    except IndexError:
        print ("Please Specify port number for binding")
        sys.exit()
    server = Server(port)

if __name__=="__main__":
    main()
