import socket
import ssl
import json

def start_tls_server(host, port, certfile, keyfile):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable reuse address/port to avoid "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the specified host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    print(f"Server started on {host}:{port}")

    while True:
        try:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")

            # Wrap the socket with SSL/TLS encryption
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile, keyfile)
            client_socket = context.wrap_socket(client_socket, server_side=True)

            # Handle client requests
            handle_client(client_socket)

            # Close the client connection
            client_socket.close()

        except KeyboardInterrupt:
            break

    # Close the server socket
    server_socket.close()
    print("Server stopped")


def handle_client(client_socket):
    # Receive data from the client
    data = client_socket.recv(1024).decode("utf-8")
    http = data.split("/")[0]

    print(f'REQUEST:{http}')

    if (http == "POST"):
        data = data.split("/")[1]
        jsonData = json.dumps(data)


        with open('database.json', 'w') as outfile:
            json.dump(jsonData, outfile)

        response = "Data save with success"
        client_socket.sendall(response.encode("utf-8"))
    
    if (http == "GET"):
        with open('database.json') as json_file:
            data = json.load(json_file)    

        response = data
        client_socket.sendall(response.encode("utf-8"))



# Example usage
if __name__ == "__main__":
    host = "localhost"
    port = 12345
    certfile = "localhost.crt"  # Path to your server certificate file
    keyfile = "localhost.key"  # Path to your server private key file

    start_tls_server(host, port, certfile, keyfile)