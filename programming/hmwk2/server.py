#!/usr/bin/env python

__author__  = "Shivam Choudhary"
__uni__     = "sc3973"
import Common
import signal
import argparse
import socket
import signal
import ssl
import pprint
import json
import binascii
import struct
import os
class Server(object):
    """ Main Server Object listening on a port.
    """

    def __init__(self, fcca_cert, fsCert, fsKey, port, host=None):
        """
        Initializing the Server Socket and binding it to the port.
            fcca_cert:
                Certificate Authority for Client.
            fsCert:
                Server Certificate
            fsKey:
                Server Private Key
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
        self.start(fcca_cert, fsCert, fsKey)

    def start(self,fcca_cert,fsCert,fsKey):
        """Start listening and recieving. Create a context for Signal handling.
            For now it just captures ctrl-c events.
        """
        signal.signal(signal.SIGINT, self.handler)
        self.serversocket.listen(1)
        while True:
            (self.clientsocket, self.clientaddress) = self.serversocket.accept()
            connstream = ssl.wrap_socket(self.clientsocket,
                    server_side = True,
                    ca_certs = fcca_cert,
                    cert_reqs = ssl.CERT_REQUIRED,
                    certfile = fsCert,
                    keyfile = fsKey)
            try:
                self.deal_with_client(connstream)
            except Exception as e:
                print e
            finally:
                print ("Client has closed its socket!!")
                connstream.close()
                exit()
            
    def deal_with_client(self,connstream):
        while True:
            mode = Common.recv_msg(connstream)
            if mode=="put":
                data = Common.recv_msg(connstream)
                fhash = Common.recv_msg(connstream)
                fname = Common.recv_msg(connstream)
                with open ("server_files/"+fname,"w")as f:
                    f.write(data)
                with open("server_files/"+fname+".sha256","w") as f:
                    f.write(fhash)
                #send 200/OK to client
                Common.send_msg(connstream,"Transfer of %s Complete" %fname)
            if mode=="get":
                filename = Common.recv_msg(connstream)
                if os.path.exists("server_files/"+filename):
                    data = open("server_files/"+filename).read()
                    Common.send_msg(connstream,"OK")
                    Common.send_msg(connstream,data)
                    fhash = open("server_files/"+filename+".sha256").read()
                    Common.send_msg(connstream,fhash)
                else:
                    Common.send_msg(connstream,"Error: %s was not retrieved"
                            %filename)
            if not mode:
                break
        
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
    parser.add_argument("fcca_cert", type=str, help="Client's Ceritificate")
    parser.add_argument("fsCert",type=str, help="Server's certfile")
    parser.add_argument("fsKey", type=str, help= "Server's private key")
    parser.add_argument("port", type=int, help="<int> Port number for listening")
    parser.add_argument("host", type=str, help="IP/Host address of the server")
    args = parser.parse_args()
    server = Server(args.fcca_cert, args.fsCert, args.fsKey, 
            args.port, args.host)



if __name__=="__main__":
    main()
