"COMS 4180 Network Security Programming Assignment 2"
=====================================================

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
 
Supported Commands and Formats:
        1) put <filename> <enc-flag> <opt-password>
                The command would encrypt the file and put the file to the 
                server.
