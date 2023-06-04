import socket
import ssl
import json
import sys

host = "localhost"
port = 12345
certfile = "localhost.crt"  # Path to your server certificate file
keyfile = "localhost.key"  # Path to your server private key file

# SSL/TLS configuration for server authentication
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Load the CA certificates for client certificate verification
context.load_verify_locations(certfile)

# Load the server's certificate and private key
context.load_cert_chain(certfile=certfile, keyfile=keyfile)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock = context.wrap_socket(sock, server_hostname=host)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Tenta se conectar ao servidor
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            sock.close()
            print(f"Error: Could not connect to server")
            exit()

        print(f"Connected to server on port {port}...")

        # Loop principal do cliente
        while True:
            # Read user input from stdin
            user_input = input("Enter request (e.g., POST/nome/pedro): ")

            if user_input.lower() == "exit":
                break

            # Split the input into HTTP method and data
            http, data = user_input.split("/", 1)

            # Prepare the request message
            message = f'{http}/{data}'
            encoded_message = message.encode('UTF-8')

            # Send the request to the server
            sock.sendall(encoded_message)

            sock.settimeout(1.0)  # Timeout of 1 second

            # Wait for the server's response
            try:
                received_data = sock.recv(1024)  # Receive data from the server (buffer of 1024 bytes)
                received_data = received_data.decode("utf-8")  # Decode the received data
                print(f"Response: {received_data}")
            except socket.timeout:
                print("No data was received from server. Timeout occurred.")
            except:
                sock.close()

if __name__ == '__main__':
    main()