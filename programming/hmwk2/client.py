import socket
import ssl
import argparse
import cmd
import os
import random
import Common
import signal
import sys

"""References
    1) http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-
    with-self-signed-certificate (For setting up the SSL Socket Context)
    2) https://docs.python.org/2/library/ssl.html#client-side-operation
"""
class Client(object):
    def __init__(self,fsca_cert,fcCert,fcKey, port, host=None):
        """ Client Class for setting up the TLS/SSL socket and keys
            fsca_cert:
                file server CERTIFICATE AUTHORITY
            fcCert:
                file client Certificate
            fckey:
                file client Private RSA KEY
            port:
                port number on which server is listening.
            host:
                Host IP address
                
        """
        self.port = port
        if host:
            self.host= host
        else:
            self.host="127.0.0.1"
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(self.clientsocket,
                ca_certs=fsca_cert,
                cert_reqs=ssl.CERT_REQUIRED,
                certfile=fcCert,
                keyfile=fcKey) # Reference: 1
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
            sys.exit(0)


class Cli(cmd.Cmd):

    """CLI for console Management!!
    """
    
    def __init__(self,clientsocket):
        cmd.Cmd.__init__(self)
        self.prompt     = ">"
        self.doc_header = "Secure TLS Shell"
        self.ruler      = "-"
        self.intro      = 'Welcome to 2 Way Secure TLS Shell !!'
        self.clientsocket = clientsocket 
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
        print "Error: Invalid commands, options are 'get' 'put' 'stop'"
    
    def do_stop(self,line):
        print "Closing Socket!! Please wait"
        return True

    def do_get(self,line):
        """ Gets the file from the server!!
            line:
                filename        : The filename to be retrieved.
                <encflag>       : "E" or "N", whether the file was encrypted.
                <opt password>  : Password<8 Characters> for decrypting the file.
        """
        args = line.split(" ")
        if len(args)==2:
            #case get <filename> <encflag = N>
            filename, encflag = line.split(" ")
            if encflag!='N':
                print "Error: Wrong Flag"
                self.cmdloop()
        elif len(args)==3:
            #case get <filename> <encflag = E> <password>
            filename, encflag, password = line.split(" ")
            if len(password)!=8:
                print "Password is short <8 Characters>"
                self.cmdloop()
            if encflag!='E':
                print "Wrong Flag"
                self.cmdloop()
        else:
            print "Wrong Number of Arguments"
            self.cmdloop()
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
            fname = 'tmp_client/'+filename+".enc"
            if encflag=='E':
                #Client assumes the file was encrypted.
                if not Common.decrypt_file(password, fname):
                    #File was not encrypted to begin with!!
                    print ("Error: decryption of %s failed, was file encrypted?"
                            %filename)
                    os.remove('tmp_client/'+filename+".sha256") # sha of file
                    os.remove('tmp_client/'+filename+".enc") #enc file
                else:
                    #File decrypted check hash
                    filehash = Common.gen_hash('tmp_client/'+filename)
                    if fhash==filehash:
                        print "retrieval of %s complete" %filename
                    else:
                        print ("Error: Computed hash of %s does not match "
                        "retrieved hash" %filename)
                        os.remove('tmp_client/'+filename)
                    #Irrespecive of Match or not delete the hashed file.
                    os.remove('tmp_client/'+filename+".sha256")
                    os.remove('tmp_client/'+filename+".enc")
            else:
                #Client assumes no encryption was applied
                filehash = Common.gen_hash('tmp_client/'+filename+".enc")
                if fhash==filehash:
                    print "retrieval of %s complete "%filename
                else:
                    print ("Error: Computed hash of %s does not match "
                        "retrieved hash" %filename)
                with open('tmp_client/'+filename,"w") as f:
                    f.write(data)
                os.remove('tmp_client/'+filename+".sha256")

                os.remove('tmp_client/'+filename+".enc")
        else:
            #Server Error Occured.
            print status

    def do_put(self,line):
        """Puts the file into the server
            filename        : The filename should be in same folder.
            encflag         : "E" or "N", whether encryption is required or not
            opt<password>   : Password<8 Characters> for encrypting the file.
        """
        args = line.split(" ")
        if len(args)==2:
            #case put <filename> <encflag>
            filename, encflag = line.split(" ")
            if not os.path.isfile(filename):
                print ("Error: %s cannot be transferred" %filename)
                self.cmdloop()
            if encflag!='N':
                print "Wrong parameter"
                self.cmdloop()
        elif len(args)==3:
            #case put <filename> <encflag> <password>
            filename ,encflag, password = line.split(" ")
            if not os.path.isfile(filename):
                print "Error: File not found. Should be in same folder!"
                self.cmdloop()
            if encflag!="E" or len(password)!=8:
                print "Error: Wrong Flag/password"
                self.cmdloop()
        else:
            print "Error: Wrong Number of Arguments!!"
            self.cmdloop()
        fhash = Common.gen_hash(filename)
        # Hash generated send it now!
        if encflag=="E":
            Common.encrypt_file(password,filename) 
            with open(filename+".enc") as f:
                msg = f.read()
            os.remove(filename+".enc")
        else:
            with open(filename) as f:
                msg = f.read()
        Common.send_msg(self.clientsocket,"put") #Set mode to put
        Common.send_msg(self.clientsocket,msg)
        Common.send_msg(self.clientsocket,fhash)
        Common.send_msg(self.clientsocket,filename)
        #Wait for Response from Server
        print Common.recv_msg(self.clientsocket) 
        

def main():
    if not os.path.exists('tmp_client'):
        os.makedirs('tmp_client')
    if not os.path.exists('server_files'):
        os.makedirs('server_files')
    parser = argparse.ArgumentParser(description="I am Client")
    parser.add_argument("fsca_cert",type=str, help= "Root CA for server")
    parser.add_argument("fcCert",type=str, help="Client Certificate")
    parser.add_argument("fcKey",type=str, help="Client's Private RSA Key")
    parser.add_argument("port", type=int, help="Server's Port Number")
    parser.add_argument("host", type=str, help="Client's IP address")
    args = parser.parse_args()
    client = Client(args.fsca_cert, args.fcCert, args.fcKey, 
            args.port, args.host)

if __name__=="__main__":
    main()
