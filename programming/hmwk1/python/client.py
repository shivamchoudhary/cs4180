import socket
import argparse
import sys
import os, random, struct
import Common
from Crypto.Signature import PKCS1_PSS
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import hashlib
from Crypto.Hash import SHA256
import json
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
        """
        Encryption Wrapper from Client class.
        Encrypts the input file and creates an output file <filename.enc>
        """
        Common.encrypt_file(self.password,self.filename)
    
    def send_data(self):
        with open('test.txt.enc') as infile:
            d = infile.read(1024)
            while d:
                self.s.sendall(d)
                d = infile.read(1024)
            print "File sending complete!! Sending AES Keys"
            self.s.close()
            self.sendsign()
    def sendsign(self):
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s1.connect((self.servername,self.port))
        
        # signature = self.sign()
        key = self.encryptkey()
        self.s1.sendall(key)
        signature = self.sign()
        self.s1.sendall(signature)
        self.s1.close()

    def encryptkey(self):
        key = RSA.importKey(open('server_public.pem').read())
        cipher =PKCS1_OAEP.new(key)
        ciphertext = cipher.encrypt(self.password)
        return ciphertext
    def rsa(self):
        """
        RSA wrapper. If the file <client_private.pem> or <client_public.pem>
        exists,does not creates them.
        """
        Common.gen_rsa('client')
    def sign(self):
        """
        Signs the SHA256 hash of the file contents with client's private key.
        """
        with open(self.filename) as file:
            message = file.read()
        key = RSA.importKey(open('client_private.pem').read())
        h = SHA256.new()
        h.update(message)
        signer = PKCS1_PSS.new(key)
        signature = signer.sign(h)
        return signature
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
