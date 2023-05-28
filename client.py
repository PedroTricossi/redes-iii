import socket
import ssl
import time

dados = {
    'nome':'pedro'
}

def start_tls_client(host, port):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL/TLS encryption
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False  # Disable hostname verification
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification
    client_socket = context.wrap_socket(client_socket, server_hostname=host)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server: {host}:{port}")

    # Send data to the server
    message = f'POST/{dados}'
    client_socket.sendall(message.encode("utf-8"))

    # Receive response from the server
    response = client_socket.recv(1024).decode("utf-8")
    print(f"Server response: {response}")

    # time.sleep(3)

    # message = f'GET/'
    # client_socket.sendall(message.encode("utf-8"))

    # # Receive response from the server
    # response = client_socket.recv(1024).decode("utf-8")
    # print(f"Server response: {response}")

    # Close the client socket
    client_socket.close()


# Example usage
if __name__ == "__main__":
    host = "localhost"
    port = 12345

    start_tls_client(host, port)
