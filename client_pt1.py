import socket
import ssl
import json

HOST = "127.0.0.1"
PORT = 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
context.minimum_version = ssl.TLSVersion.TLSv1_3 # enforce minimum tls version
context.load_cert_chain(certfile="./client.crt", keyfile="./client.key") # cert and key for mutual authentication
context.load_verify_locations("server.crt")

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:

        request = {"command": "GET_TIME"}
        ssock.sendall(json.dumps(request).encode())

        response = ssock.recv(4096)
        print("Server Response:", response.decode())



"""
[x] use TCP-based communication
[x] have server presents X.509 certificate
[x] include client verification of certificate
[] system logs the negotiated TLS version and cipher suite


Notes:

getpeercert() - retrieves the certificate of the other side of the connection
cipher() - retrieves the cipher being used for the secure connection
"""