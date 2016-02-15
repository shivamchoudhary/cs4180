"Programming Assignment 1"
==========================

*How to Run?
1)Use the Makefile,seriously its good in the below order.
2)make server
3)make client
If want to specify the parameters manually then follow the following format.
4)python server.py <Port> <Mode> <Server Private Key filename> 
        <Server Public Key filename> <Client Public Key filename>

5)python client.py <AES_KEY> <Filename> <Server Name> <Port Number> 
        <Client Private Key filename> <Client Public Key filename> 
        <Server Public Key filename>

*File Introduction:
client.py          : Contains Client Class which reads the data 
server.py          : Contains Server Class which stores the data received 
                     from the client.
Common.py          : Contains several utility functions used by both client 
                     and server.
client_private.pem : Client's 2048 bit RSA Private Key.
client_public.pem  : Client's 2048 bit RSA Public Key.
server_private.pem : Server's 2048 bit RSA Private Key.
server_public.pem  : Server's 2048 bit RSA Public Key.

*Messages
Error Messages     : Error Messages are Self Explanatory.
Verification Passed: When the Signed Hash matches.
Verification Failed: When the Signed Hash does not match.



