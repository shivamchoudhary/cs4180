#!/usr/bin/env python

__author__  = "Shivam Choudhary"
__uni__     = "sc3973"

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
import os

class Server(object):
    """ Generic Server Class with Recieve and Send """

    def __init__(self,port,mode,fsprivate_key,fspublic_key,fcpublic_key):
        """
        Initializing the Server Socket and binding it on the port.
            param:port The port number on which the server is listening.
            param:mode The mode(Trusted/Untrusted) of Server.
        """
        self.host ="localhost"
        self.port = port
        self.mode = mode
        self.fsprivate_key = fsprivate_key
        self.fspublic_key = fspublic_key
        self.fcpublic_key = fcpublic_key
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
                Common.gen_rsa('server') #Generate the RSA Keys(if not exists)
                (clientsocket,clientaddress) = serversocket.accept() 
                self.recv_data(clientsocket)
            elif count==1:
                self.normallisten(serversocket)
                break
    
    def normallisten(self,serversocket):
        """
        Recieve other Keys AES and Signed Hash.
        """
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
        key = RSA.importKey(open(self.fsprivate_key).read())
        cipher = PKCS1_OAEP.new(key)
        AES_KEY = cipher.decrypt(data) #AES_KEY using Server's Private Key.
        self.decrypt(AES_KEY)
        self.verify_signature(signature) 
    
    def recv_data(self,clientsocket):
        """
        Recieves AES_CBC mode encrypted file from the Socket and writes in file
        decrypted.enc

        clientsocket:
            The socket from which it has to recieve the data.
        """
        data=""
        while True:
            buffer = clientsocket.recv(1024)
            data+=buffer
            if not buffer:
                break
        with open('decrypted.enc','wb')as fname:
            fname.write(data)
        clientsocket.close()
    
    def verify_signature(self,signature):
        """
        Verify the Hashed Signature.

        signature:
            The SHA256 signed hash recieved from the Client of the file.
        """
        key = RSA.importKey(open(self.fcpublic_key).read())
        h = SHA256.new()
        if self.mode=='t':
            recvddata = open('decrypted').read()
        elif self.mode=="u":
            recvddata = open('fakefile').read()
        h.update(recvddata)
        verifier = PKCS1_PSS.new(key)
        
        if verifier.verify(h,signature):
            print "Verification Passed"
        else:
            print "Verification Failed"

    
    def decrypt(self,AES_KEY):
        """
        Wrapper to Decrypt file.
        """
        Common.decrypt_file(AES_KEY,'decrypted.enc')

def sanity_check(port, mode, fsprivate_key, fspublic_key, fcpublic_key):
    """
    Sanity checks to make sure <port> <mode> <fsprivate_key> <fspublic_key>
    <fcpublic_key>
    exists. 
    For PrivateKey and PublicKey pairs if the file is not specified it takes 
    precomputed files or generates new key pair. See Common.py for gen_rsa(mode)
    method.
    """

    if (port <1024 or port >65536):
        print "Port Number is not in the range <1024,65536>"
        return False
    if not(mode!='t'or mode!='u'):
        print "Invalid Mode. It should be either untrusted(u) or trusted(t)"
        return False
    if not (os.path.isfile(fspublic_key) and os.path.isfile(fsprivate_key)):
        print "Both Public and Private Key files should be in the same folder"
        return False
    if (fspublic_key==fsprivate_key):
        print "Public Keys and Private Keys should have different names"
        return False
    if not(os.path.isfile(fcpublic_key)):
        print "Public Key of Client should be in the same folder"
    else:
        return True

def main():
    """
    Driver Code for running the server.
    Some Notation Convention:
    f is appended for file.
    s is for server.
    c is for client.
    so fspublic_key becomes Public Key of Server and so on.
    """
    parser = argparse.ArgumentParser(description="I am Server")
    parser.add_argument("port", type=int, help="Socket to bind on")
    parser.add_argument("mode", type=str, help="Trusted/Untrusted")
    parser.add_argument("fsprivate_key",type=str,help="Server Private Key in,"
            ".pem format,Also it should be in the same folder")
    parser.add_argument("fspublic_key",type=str,help="Server Public Key in .pem" 
            "format ,Also it should be in the same folder")
    parser.add_argument("fcpublic_key",type=str,help="Client's Public Key in, "
            ".pem format")
    args = parser.parse_args()
    if sanity_check(args.port,args.mode,args.fsprivate_key,args.fspublic_key,
            args.fcpublic_key):
        server = Server(args.port,args.mode,args.fsprivate_key,
                args.fspublic_key,args.fcpublic_key)
    else:
        exit()
if __name__=="__main__":
    main()
