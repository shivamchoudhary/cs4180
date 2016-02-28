#!/usr/bin/env python

__author__  = "Shivam Choudhary"
__uni__     = "sc3973"

import signal
import argparse
import socket
import signal

class Server(object):
    """ Main Server Object listening on a port.
    """

    def __init__(self, port,host=None):
        """
        Initializing the Server Socket and binding it to the port.
            host:
                IPV4 address on which the server is listening.
            port:
                Port Number on which the Server is listening.

        """
        if host:
            self.host = host # If ip address is specified use that.
        else:
            """ip not specified use the Fully Qualified Domain.
            >>> socket.getfqdn()
            'dyn-**-**-**-**.dyn.columbia.edu' 
            So as we can see this is a problem here.
            """
            self.host = socket.getfqdn()
            print ("You didn't specify host so using FQDN %s" %self.host)
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.serversocket.bind((self.host, self.port))
        except socket.error as error:
            print ("Socket Binding Failed %s" %error)
            exit()
        self.start()


    def start(self):
        """Start listening and recieving. Create a context for Signal handling.
            For now it just captures ctrl-c events.
        """
        signal.signal(signal.SIGINT, self.handler)
        self.serversocket.listen(1)
        (self.clientsocket, self.clientaddress) = self.serversocket.accept()

        while True:
            data = self.clientsocket.recv(1024)
            if not data:
                print "Client Side has been closed!!"
                exit()
    


    def handler(self,signum, frame):
        """
        For handling ctrl-c events.
        """
        print ("Recieved Signal!! Cleaning Up Please Wait")
        try:
            self.clientsocket.close()
            print ("Cleaned Client Connection")
        except AttributeError:
            # When connection closed without accepting the connection from client.
            pass
        print ("Closing!!")
        exit()


def main():
    """Some Notation
            a) f is appended for file.
            b) s is for server.
            c) c is for client.
            d) Cert is for certificate.
        eg: fsCert/fcCert is server's/client's certificate.
    """
    parser = argparse.ArgumentParser(description="I am Server")
    parser.add_argument("port", type=int, help="<int> Port number for listening")
    parser.add_argument("host", type=str, help="IP/Host address of the server")
    args = parser.parse_args()
    server = Server(args.port , args.host)

if __name__=="__main__":
    main()
