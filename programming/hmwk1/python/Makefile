client:
	python client.py 1234567891011111 test.txt localhost 4180 client_private.pem client_public.pem server_public.pem

server:
	python server.py 4180 t server_private.pem server_public.pem client_public.pem
userver:
	python server.py 4180 u server_private.pem server_public.pem client_public.pem
clean:
	rm *.enc
