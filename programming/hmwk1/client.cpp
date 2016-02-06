#include <iostream>
#include <exception>
#include "Common.h"
#include <string>
using namespace std;
struct user_t{
        string password;
        string fname;
}client;
struct address{
        int port;
        string ip;
}socketname;



int main(int argc, char *argv[]){
        if (argc !=4){
                cerr <<"Wrong Initialization only 3 are required"<<endl;
                exit(0);
        }
        string password   = argv[1];
        string fname      = argv[2];
        int port          = stoi(argv[3]);
        string ip           = "localhost"; 
        socketname.port  = port;
        socketname.ip = ip;
        
        //Check if the password is less than 16 characters.
        if (password.length()<16){
                cerr <<"Password too short use 16 chars";
        }
        //Initialize client with password.
        client.password = password;
        client.fname = fname;
}



int 

