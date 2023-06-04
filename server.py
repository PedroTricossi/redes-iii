import socket
import ssl
import json

host = "localhost"
port = 12345
certfile = "localhost.crt"  # Path to your server certificate file
keyfile = "localhost.key"  # Path to your server private key file

# SSL/TLS configuration for client authentication
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# Load the CA certificates for client certificate verification
context.load_verify_locations(certfile)

# Load the server's certificate and private key
context.load_cert_chain(certfile=certfile, keyfile=keyfile)

def handle_client(data):
    # Receive data from the client
    http, *params = data.split("/")
    print(f'REQUEST: {http}')

    if http == "POST" and len(params) == 2:
        key, value = params
        data_dict = {key: value}

        # Load existing data from the database file
        with open('database.json') as json_file:
            existing_data = json.load(json_file)

        # Update the existing data with the new data
        existing_data.update(data_dict)

        # Write the updated data back to the database file
        with open('database.json', 'w') as outfile:
            json.dump(existing_data, outfile)

        response = "Data received and stored successfully."
    elif http == "GET" and len(params) == 1:
        key = params[0]

        with open('database.json') as json_file:
            data = json.load(json_file)
        
        # data_dict = json.loads(data)
        response = data.get(key, "Key not found.")
    elif http == "PUT" and len(params) == 2:
        key, value = params
        with open('database.json') as json_file:
            data = json.load(json_file)
        
        data[key] = value

        with open('database.json', 'w') as outfile:
            json.dump(data, outfile)

        response = "Data updated successfully."
    elif http == "DELETE" and len(params) == 1:
        key = params[0]
        with open('database.json') as json_file:
            data = json.load(json_file)
        
        if key in data:
            del data[key]
            with open('database.json', 'w') as outfile:
                json.dump(data, outfile)
            
            response = "Data deleted successfully."
        else:
            response = "Key not found. No data deleted."
    else:
        response = "Invalid request."

    return response


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set socket options
    sock.bind((host, port))  # Bind the socket to the specified IP address and port

    print(f"Listening on port {port}...")
    sock.listen()  # Wait for incoming connections

    sock = context.wrap_socket(sock, server_side=True)
    conn, addr = sock.accept()  # Accept a connection from a client

    with conn:
        print(f"Server connected to client on socket {addr}")
        while True:
            data = conn.recv(1024)  # Receive data from the client (maximum of 1024 bytes)
            data = data.decode("utf-8")  # Decode the received data from bytes to string
            if not data:
                sock.close()  # Close the socket
                print("No connection received. Closing.")
                break

            print(f"Received request: {data}")
            response = handle_client(data)
            conn.sendall(response.encode("utf-8"))  # Send the response back to the client

if __name__ == "__main__":
    main()
