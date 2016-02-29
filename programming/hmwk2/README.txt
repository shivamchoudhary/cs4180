"COMS 4180 Network Security Programming Assignment 2"
=====================================================

File Certificate Exchange.png is wireshark screenshot of Certificate Exchange. 

*Warning:
        All Certificates must be in the same folder. Names can be changed but 
        don't put CA into Private Key and expect it work,it just won't.

*How to Run?

Method 1:- 
        Type make server and make client. This supplies the Server and Client 
        with default values of port number. The only caveat is that it runs 
        on localhost. If you want to test on different IP's look into Method 2 
        in this section.
        As is common, run the server first.

Method 2:-
        server: python server.py <fcca_cert> <fsCert> <fsKey> <port> <host>
        client: python client.py <fsca_cert> <fcCert> <fcKey> <port> <host>
        where:-
        <fcca_cert>     : File Client Certificate Authority
        <fsCert>        : File Server Certificate
        <fsKey>         : File Server Key (Private)
        <port>          : Port Number on which server is listening/client will
                                connect.
        <host>          : IP Address/FQDN of the server on which the Server is 
                                hosted/Client will connect
        <fsca_cert>     : File Server Certificate Authority
        <fcCert>        : File Client Certificate
        <fcKey>         : File Client Private Key
        
        Eg:
        Server          : python server.py server.crt client.crt client.key \
                                4180 127.0.0.1
        Client          : python client.py client.crt server.crt server.key \
                                4180 127.0.0.1:
        
        As usual run the server first else you will get an error "Is the Server\
                running?"
 
*Supported Commands and Formats:
        1) put <filename> <enc-flag> <opt-password>
                The command would encrypt the file and put the file to the 
                server.
        2) get <filename> <enc-flag> <opt-password>
                Tries to get the file from the server and puts it in /tmp_client
                directory
        3) stop 
                Closes the socket and exits.
        4) The server stores the file and its SHA256 hash in server_files folder.


* Generating Certificates:
        I used openssl cert generation tool to generate the certificates.
        a) For server:-
        openssl genrsa -des3 -out server.orig.key 2048
	openssl rsa -in server.orig.key -out server.key
	openssl req -new -key server.key -out server.csr
	openssl x509 -req -days 365 -in server.csr -signkey \
	server.key -out server.crt
        
        b) For client:-
        openssl genrsa -des3 -out client.orig.key 2048
	openssl rsa -in client.orig.key -out client.key
	openssl req -new -key client.key -out client.csr
	openssl x509 -req -days 365 -in client.csr -signkey \
	client.key -out client.crt

