import socket
import ssl
import json
import datetime
import logging

# logging configuration so that things properly log
logging.basicConfig(level=logging.INFO)
HOST = "127.0.0.1"
PORT = 8443

# Initiate SSL and certifications
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# enforce minimum tls version
context.minimum_version = ssl.TLSVersion.TLSv1_3 
context.load_cert_chain(certfile="./server.crt", keyfile="./server.key")
# authenticate client
context.load_verify_locations("client.crt") 

# Bind TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Secure server listening on {PORT}")

    # Wrapping socket with SSL
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        # TLS detail logging
        logging.info(f"TLS Version: {conn.version()}") 
        logging.info(f"Cipher Suite: {conn.cipher()}")
        logging.info(f"Session Id: {conn.session.id.hex()}")
        data = conn.recv(4096)
        request = json.loads(data.decode())

        if request.get("command") == "GET_TIME":
            response = {"time": datetime.datetime.now(
                datetime.timezone.utc).isoformat()}
        else:
            response = {"error": "Unknown command"}

        conn.sendall(json.dumps(response).encode())
