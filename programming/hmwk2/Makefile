TARFILES = Makefile client.py server.py 
port = 4119
host = 127.0.0.1
client:
	python client.py $(port) $(host) 


server:
	python server.py $(port) $(host)


clean:
	rm *.pyc *.enc *.pem
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
