TARFILES = Makefile client.py server.py Common.py Certificate\ Exchange.png\
	 client.crt client.csr client.key \
	client.orig.key README.txt  server.crt server.csr server.key \
	server.orig.key abc.txt x.dat
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
setup:
	mkdir tmp_client && mkdir server_files
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

sc3973_2.tar.gz:$(TARFILES)
	mkdir sc3973
	ln $(TARFILES) sc3973
	tar zcf sc3973_2.tar.gz sc3973
	rm -rf sc3973
