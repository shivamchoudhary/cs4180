import socket
import argparse
import cmd
import os
import random
import Common
class Client(object):

    def __init__(self,port,host=None):
        self.port = port

        if host:
            self.host= host
        else:
            self.host="127.0.0.1"
       
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientsocket.connect((self.host,self.port))
        except socket.error as error:
            print ("Failed to Connect to Server,Is it running?",error)
            exit()
        self.run()
    def run(self):
        console = Cli(self.clientsocket)
        console.cmdloop()

class Cli(cmd.Cmd):
    """CLI for console Management!!
    """
    
    
    def __init__(self,clientsocket):
        cmd.Cmd.__init__(self)
        self.SUPPORTED_COMMANDS = ['get','put']
        self.prompt     = ">"
        self.doc_header = "Secure TLS Shell"
        self.ruler      = "-"
        self.intro      = 'Welcome to Secure TLS Shell. Type help <TAB>'
        self.clientsocket = clientsocket 
        self.encflag = False
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except Exception as e:
            print "Wrong Syntax use help <command> to find correct usage.",e
            self.cmdloop()

    def default(self, line):
        print "Command Not recognized,try help or press <tab>"
    
    def do_put(self,line):
        """
        Puts the file into the server
            filename        : The filename should be in same folder.
            encflag         : "E" or "N", whether encryption is required or not
            opt<password>   : Password<8 Characters> for encrypting the file.
        """
        try:
            filename,encflag,password = line.split(" ")
        except Exception as e:
            pass
        if self.sanity_check(filename,encflag,password):
            Common.encrypt_file("1234567890111213",filename) 
            

    def sanity_check(self,filename,encflag,password=None):
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
