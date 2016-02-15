#!/usr/bin/env python

__author__  = "Shivam Choudhary"
__uni__     = "sc3973"

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
import os
import re

class Client(object):
    
    def __init__(self,password,filename,servername,port,fcprivate_key,
            fcpublic_key,fspublic_key):
        """
        Initializing the Client Socket for binding it on the port.
            password:
                    16 Character Password(Without any Special Characters)

            filename:
                    Filename which is to be encrypted. It should be in same 
                    folder.

            servername:
                    Name of the Server on which it has to connect. Usually 
                    localhost.

            port:
                    Port Number of which the Server is listening.

            fcprivate_key:
                    Private Key(.pem) of the client.

            fcpublic_key:
                    Public Key(.pem) corresponding to fcprivate_key.

            fspublic_key:
                    Public Key(.pem) of the Server.
        
        """
        self.password  = password
        self.filename = filename
        self.servername  = servername
        self.port = port
        self.fcprivate_key = fcprivate_key
        self.fcpublic_key = fcpublic_key
        self.fspublic_key = fspublic_key
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
        """
        Sends the Encrypted File to the server in 1024 chunks.
        """
        fenc = self.filename+".enc"
        with open(fenc) as infile:
            d = infile.read(1024)
            while d:
                self.s.sendall(d)
                d = infile.read(1024)
            print "File sending complete!! Sending AES Keys"
            self.s.close()
            self.sendsign()

    def sendsign(self):
        """
        Sends the RSA signed signature of the Hash contents of the file.
        """
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s1.connect((self.servername,self.port))
        key = self.encryptkey()
        self.s1.sendall(key)
        signature = self.sign()
        self.s1.sendall(signature)
        self.s1.close()

    def encryptkey(self):
        """
        Encrypts the AES_KEY with the Server's Public Key.
        """
        key = RSA.importKey(open(self.fspublic_key).read())
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
        key = RSA.importKey(open(self.fcprivate_key).read())
        h = SHA256.new()
        h.update(message)
        signer = PKCS1_PSS.new(key)
        signature = signer.sign(h)
        return signature


def sanity_check(password,filename,servername,port,fcprivate_key,fcpublic_key,
        fspublic_key):
    """
    Sanity Checks for Client.
    """
    if len(password)<16:
        print "Password is too small use 16 Characters"
        return False
    if not re.match("^[a-zA-Z0-9_]*$", password):
        print "Password contains special characters"
        return False
    if (port <1024 or port >65536):
        print "Port Number is not in the range <1024,65536>"
        return False
    if not (os.path.isfile(fcprivate_key) and os.path.isfile(fcpublic_key)
            and os.path.isfile(fspublic_key)):
        print "The .pem files should be in the same folder as this."
        return False
    if not(os.path.isfile('fakefile')):
        print "Fakefile does not exist in the folder."
        return False
    else:
        return True


def main():
    """
    Driver for running the client.
    Follows the same notation convention.
    """
    
    parser = argparse.ArgumentParser(description="I am Client")
    parser.add_argument("password", type=str, help="16 Character Password(AES_KEY)")
    parser.add_argument("filename",type=str, help="File name")
    parser.add_argument("servername",type=str,help="Name of Server(localhost)")
    parser.add_argument("port",type=int,help="Port Number for the Server")
    parser.add_argument("fcprivate_key",type=str,help="Private key of Client")
    parser.add_argument("fcpublic_key",type=str,help="Public Key of Client")
    parser.add_argument("fspublic_key",type=str,help="Public Key of Server")
    args = parser.parse_args()
    if sanity_check(args.password,args.filename,args.servername,args.port,
            args.fcprivate_key,args.fcpublic_key,args.fspublic_key):
        server = Client(args.password,args.filename,args.servername,args.port,
                args.fcprivate_key,args.fcpublic_key,args.fspublic_key)
    else:
        exit(0)

if __name__=="__main__":
    main()
