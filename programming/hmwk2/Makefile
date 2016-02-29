TARFILES = Makefile client.py server.py Common.py 
port 		= 4119
host 		= 127.0.0.1
#Client Certificate Setup
fsca_cert 	= server.crt
fcCert 		= client.crt
fcKey		= client.key
#Server Certificate Setup
fcca_cert	= client.crt
fsCert		= server.crt
fsKey		= server.key
#Setup Folders for temp files
server_folder 	= server_files
client_folder 	= tmp_client


#Directives
client:
	python client.py $(fsca_cert) $(fcCert) $(fcKey) $(port) $(host) 
server:
	python server.py $(fcca_cert) $(fsCert) $(fsKey) $(port) $(host)
clean:
	rm *.pyc *.enc *.pem  
clean_files:
	cd server_files && rm * && cd ../tmp_client && rm *
gen_server:
	openssl genrsa -des3 -out server.orig.key 2048
	openssl rsa -in server.orig.key -out server.key
	openssl req -new -key server.key -out server.csr
	openssl x509 -req -days 365 -in server.csr -signkey \
	server.key -out server.crt
gen_client:
	openssl genrsa -des3 -out client.orig.key 2048
	openssl rsa -in client.orig.key -out client.key
	openssl req -new -key client.key -out client.csr
	openssl x509 -req -days 365 -in client.csr -signkey \
	client.key -out client.crt
