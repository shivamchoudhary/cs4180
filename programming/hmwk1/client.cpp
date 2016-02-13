//Shivam Choudhary (sc3973)
//
#include <iostream>
#include <exception>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "encrypt.h"
using namespace std;
void error(const char *msg){
        perror(msg);
        exit(0);
}
int main(int argc, char *argv[]){
        int sockfd, portno, n;
        struct sockaddr_in serv_addr;
        struct hostent *server;
        char buffer[256];
        //TODO: Adding more parameters for command line
        if (argc !=6) {
                cerr<<"usage "<<argv[0]<< " <password> <file> <server-ip>"
                        " <portno> <RSA KEY>"<<endl;
                exit(0);
        }
        server = gethostbyname(argv[3]);
        portno = atoi(argv[4]);
        string password  = argv[1];
        char userpassword[16];
        for (int i=0;i<password.length();i++){
                userpassword[i] = password[i];
        }
        
        unsigned char *inputkey = (unsigned char *)userpassword;
        start(inputkey);
        //Check Password Length
        if (password.length()<16){
                cerr<<"Password Length should be greater than 16 Characters";
                exit(0);
        }

        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) 
                error("ERROR opening socket");
        if (server == NULL) {
                fprintf(stderr,"ERROR, no such host\n");
                exit(0);
        }
        bzero((char *) &serv_addr, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        bcopy((char *)server->h_addr, 
                 (char *)&serv_addr.sin_addr.s_addr,
                server->h_length);
        serv_addr.sin_port = htons(portno);
        if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
                error("ERROR connecting");
        while (1){

                bzero(buffer,256);
                fgets(buffer,255,stdin);
                n = write(sockfd,buffer,strlen(buffer));
                if (n < 0) 
                        cout<<"ERROR writing to socket";
                bzero(buffer,256);
                n = read(sockfd,buffer,255);
                if (n < 0) 
                        cout<<"ERROR reading from socket";
                cout<<"Server: "<<buffer<<endl;
        }
    close(sockfd);
    return 0;
}


