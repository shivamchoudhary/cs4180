import argparse
import sys
import Common
import socket
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
class Server(object):

    def __init__(self,port):
        """
        Initializing the Server Socket and binding it on the port.
            param:port The port number on which the server is listening.
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
        count=0
        while True:
            serversocket.listen(1)
            if count==0:
                count+=1
                Common.gen_rsa('server')
                (clientsocket,clientaddress) = serversocket.accept() 
                self.recv_data(clientsocket)
            elif count==1:
                self.normallisten(serversocket)
                break
    def normallisten(self,serversocket):
        print "Normal Listen"
        (clientsocket,clientaddress) = serversocket.accept()
        self.normal_recv(clientsocket)
        clientsocket.close()
    def normal_recv(self,clientsocket):
        """
        Designed to Recieve Key Used for Encryption and Signature Verification.
        Has 2 Socket.recv calls.
        """
        data = clientsocket.recv(1024)
        signature = clientsocket.recv(1024)
        key = RSA.importKey(open('server_private.pem').read())
        cipher = PKCS1_OAEP.new(key)
        AES_KEY = cipher.decrypt(data)
        self.decrypt(AES_KEY)
        print AES_KEY
        self.verify_signature(signature) 
    def recv_data(self,clientsocket):
        data=""
        length = 0
        while True:
            buffer = clientsocket.recv(1024)
            data+=buffer
            if not buffer:
                break
        with open('recv.enc','wb')as fname:
            fname.write(data)
        clientsocket.close()
    
    def verify_signature(self,signature):
        key = RSA.importKey(open('client_public.pem').read())
        h = SHA256.new()
        recvddata = open('recv').read()
        h.update(recvddata)
        verifier = PKCS1_PSS.new(key)
        
        if verifier.verify(h,signature):
            print "Authentic"
        else:
            print "Fake"

    
    def decrypt(self,AES_KEY):
        Common.decrypt_file(AES_KEY,'recv.enc')


def main():
    try:
        port = int(sys.argv[1])
    except IndexError:
        print ("Please Specify port number for binding")
        sys.exit()
    server = Server(port)

if __name__=="__main__":
    main()
