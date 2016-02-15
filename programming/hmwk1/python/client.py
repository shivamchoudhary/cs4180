import socket
import argparse
import sys
import os, random, struct
import Common
import json
from Crypto.Signature import PKCS1_PSS
from Crypto.PublicKey import RSA
import hashlib
from Crypto.Hash import SHA256
class Client(object):
    
    def __init__(self,password,filename,servername,port):
        """
        Initializing the Client Socket for binding it on the port.
        """
        self.password  = password
        self.filename = filename
        self.servername  = servername
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveraddress = (self.servername,self.port)
        try:
            self.s.connect(serveraddress)
        except socket.error as error:
            print ("Failed to connect to server %s",error)
        self.encrypt_file()
        self.send_data()
        self.rsa()
        self.sign()

    def encrypt_file(self):
        Common.encrypt_file('shivamchoudhary1','test.txt')
    def read_file(self):
        with open('test.txt.enc','rb') as fname:
            data = fname.read()
        return data
    def send_data(self):
        data  = self.read_file()
        self.s.sendall(str(data))
    
    def rsa(self):
        Common.gen_rsa('client')

    def sign(self):
        with open(self.filename) as file:
            message = file.read()
        key = RSA.importKey(open('client_private.pem').read())
        h = SHA256.new()
        h.update(message)
        signer = PKCS1_PSS.new(key)
        signature = signer.sign(h)
        
def sanity_check(password,filename,servername,port):
    """
    Sanity Check for the System.
    TODO Add more checks.
    """
    if len(password)<16:
        print ("Password %s is too small use 16 Characters",password)


def main():
    try:
        password = sys.argv[1]
        filename = sys.argv[2]
        servername = sys.argv[3]
        port=int(sys.argv[4])
    except IndexError:
        print ("Missing some important things Port Number/Hostname ")
        sys.exit()

    server = Client(password,filename,servername,port)


if __name__=="__main__":
    main()
