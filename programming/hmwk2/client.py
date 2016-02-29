import socket
import ssl
import argparse
import cmd
import os
import random
import Common
import signal
import pprint
import json
import binascii
import struct
"""References
    1) http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-
    with-self-signed-certificate (For setting up the SSL Socket Context)
    2) https://docs.python.org/2/library/ssl.html#client-side-operation
"""
class Client(object):

    def __init__(self,port,host=None):
        self.port = port

        if host:
            self.host= host
        else:
            self.host="127.0.0.1"
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(self.clientsocket,
                ca_certs="server.crt",
                cert_reqs=ssl.CERT_REQUIRED,
                certfile="client.crt",
                keyfile="client.key") # Reference: 1
        try:
            ssl_sock.connect((self.host,self.port))
        except socket.error as error:
            print ("Failed to Connect to Server,Is it running?",error)
            exit()
        self.run(ssl_sock)
    def run(self,ssl_sock):
        try:
            console = Cli(ssl_sock)
            console.cmdloop()
        finally:
            ssl_sock.close()
            exit()

class Cli(cmd.Cmd):

    """CLI for console Management!!
    """
    
    def __init__(self,clientsocket):
        cmd.Cmd.__init__(self)
        self.SUPPORTED_COMMANDS = ['get','put','stop']
        self.prompt     = ">"
        self.doc_header = "Secure TLS Shell"
        self.ruler      = "-"
        self.intro      = 'Welcome to 2 Way Secure TLS Shell !!'
        self.clientsocket = clientsocket 
        self.encflag = False
        signal.signal(signal.SIGINT, self.handler)# Signal Interrupt Handler. 
    
    def handler(self, signum, frame):
        """For handling ctrl-c events 
        """
        print ("Recieved Signal !! Cleaning Up Please Wait")
        self.clientsocket.close()
        exit()

    
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except Exception as e:
            print "Wrong Syntax use help <command> to find correct usage.",e
            self.cmdloop()

    def default(self, line):
        print "Command Not recognized,try help or press <tab>"
    
    def do_stop(self,line):
        print "Okay Got IT!!"
        return True

    def do_get(self,line):
        """ Tries to get the file from the server!!
        """
        try:
            filename, encflag, password = line.split(" ")
        except Exception as e:
            pass
        if self.get_sanitycheck(encflag,password):
            Common.send_msg(self.clientsocket,"get")
            Common.send_msg(self.clientsocket, filename)
            status = Common.recv_msg(self.clientsocket)
            if status=="OK":
                data = Common.recv_msg(self.clientsocket)
                fhash = Common.recv_msg(self.clientsocket)
                with open('tmp_client/'+filename+".enc","w") as f:
                    f.write(data)
                with open('tmp_client/'+filename+".sha256","w") as f:
                    f.write(fhash)
                filename = 'tmp_client/'+filename+".enc"
                Common.decrypt_file(password, filename)
                filehash = Common.gen_hash(filename)
                if fhash==filehash:
                    print "Hash MAtches"
                else:
                    print "hash failed:"
            else:
                print status
    def get_sanitycheck(self,encflag,password=None):
        if not (encflag=="E" or encflag=="N"):
            print "The encryption flag should be either E or N"
            return False
        if (encflag=="E"):
            if len(password)!=8:
                print ("Specify password <8 Characters> to decrypt the file")
                return False
        if (encflag=="N"):
            if password:
                print ("You specified not to decrypt but gave a password")
                return False
        return True
    def do_put(self,line):
        """Puts the file into the server
            filename        : The filename should be in same folder.
            encflag         : "E" or "N", whether encryption is required or not
            opt<password>   : Password<8 Characters> for encrypting the file.
        """
        try:
            filename,encflag,password = line.split(" ")
        except Exception as e:
            pass
        if self.sanity_check(filename,encflag,password):
            Common.encrypt_file(password,filename) 
            fhash = Common.gen_hash(filename)
            #File has been encrypted try to serialize and send it.
            with open(filename+".enc") as f:
                msg = f.read()
                
            Common.send_msg(self.clientsocket,"put") #Set mode to put
            Common.send_msg(self.clientsocket,msg)
            Common.send_msg(self.clientsocket,fhash)
            Common.send_msg(self.clientsocket,filename)
            #Wait for Error from Server
            print Common.recv_msg(self.clientsocket) 
            self.encflag = False
            
    def sanity_check(self,filename,encflag,password=None):
        """ Sanity Checks for the Inputs
        """
        if not os.path.isfile(filename):
            print "The file to be put should be in the same folder."
            return False
        if not (encflag=="E" or encflag=="N"):
            print "The encryption flag should be either E or N"
            return False
        if (encflag=="E"):
            if len(password)!=8:
                print ("Specify password <8 characters> to encrypt the file") 
                return False
            else:
                self.encflag=True
        return True

    

def main():
    parser = argparse.ArgumentParser(description="I am Client")
    parser.add_argument("port", type=int, help="Server's Port Number")
    parser.add_argument("host", type=str, help="Client's IP address")
    args = parser.parse_args()
    client = Client(args.port, args.host)

if __name__=="__main__":
    main()
