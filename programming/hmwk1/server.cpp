//Shivam Choudhary(sc3973)
//
#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <csignal>
using namespace std;

void signalHandler( int signum ){
        cout << "Interrupt signal (" << signum << ") received.\n";
        exit(signum);  
}


void error(const char *msg){

    perror(msg);
    exit(1);
}
int main(int argc, char *argv[]){

        int sockfd, newsockfd, portno;
        socklen_t clilen;
        char buffer[256];
        struct sockaddr_in serv_addr, cli_addr;
        int n;
        if (argc < 2) {
                cerr<<"Usage, no port provided\n"<<endl;
                exit(1);
     }
     // TCP Socket
        sockfd =  socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) 
                error("ERROR opening socket");

        int reuse = 1;
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (const char*)&reuse, 
                            sizeof(reuse)) < 0)
                perror("setsockopt(SO_REUSEADDR) failed");

        #ifdef SO_REUSEPORT
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, (const char*)&reuse, 
                            sizeof(reuse)) < 0) 
                perror("setsockopt(SO_REUSEPORT) failed");
        #endif 

        bzero((char *) &serv_addr, sizeof(serv_addr));
        portno = atoi(argv[1]);
        serv_addr.sin_family = AF_INET;  
        serv_addr.sin_addr.s_addr = INADDR_ANY;  
        serv_addr.sin_port = htons(portno);
        if (bind(sockfd, (struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
        listen(sockfd,5);
        clilen = sizeof(cli_addr);

        newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0) 
                error("ERROR on accept");

        cout <<"Request from "<<inet_ntoa(cli_addr.sin_addr)<<"Port "<<
             ntohs(cli_addr.sin_port);
        bzero(buffer,256);
        signal(SIGINT, signalHandler);  
        while (1){
                bzero(buffer,256);
                n = read(newsockfd,buffer,255);
                if (n < 0) 
                          error("ERROR reading from socket");
                cout<<"Client"<<buffer<<endl;
                n = write(newsockfd,buffer,255);
                if (n<0) 
                     error("Error");
     }
        close(newsockfd);
        close(sockfd);
     return 0; 
}
