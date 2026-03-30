import socket
import ssl
import json

HOST = "127.0.0.1"
PORT = 8443

# Initiating SSL with server.crt
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# enforce minimum tls version
context.minimum_version = ssl.TLSVersion.TLSv1_3 
# cert and key for mutual authentication
context.load_cert_chain(certfile="./client.crt", keyfile="./client.key") 
context.load_verify_locations("server.crt")

with socket.create_connection((HOST, PORT)) as sock:

    # Wrapping socket with SSL
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:

        request = {"command": "GET_TIME"}
        ssock.sendall(json.dumps(request).encode())

        response = ssock.recv(4096)
        print("Server Response:", response.decode())