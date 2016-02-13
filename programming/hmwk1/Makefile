
server: server.o
	g++ -Wall server.cpp -o server
client: client.o Common.h encrypt.h
	g++ -Wall -I/usr/local/bin/openssl/ -o client -lcrypto -lssl Common.cpp encrypt.cpp client.cpp 
common.o: Common.c
	g++ -Wall Common.cpp -o common.o Common.c
testserver: 
	./server 4180 

testclient: 
	./client shivamchoudhary1 test.txt localhost 4180 RSA
encrypt:
	g++ -I/usr/local/bin/openssl/ -o encrypt -lcrypto encrypt.cpp 

