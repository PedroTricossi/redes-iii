import socket
import ssl
import json

host = "localhost"
port = 12345
certfile = "localhost.crt"  # Path to your server certificate file
keyfile = "localhost.key"  # Path to your server private key file

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_verify_locations(certfile)
context.load_cert_chain(certfile = certfile, keyfile = keyfile)

context.check_hostname = False


def handle_client(data):
    # Receive data from the client
    http = data.split("/")[0]

    print(f'REQUEST:{http}')

    if (http == "POST"):
        data = data.split("/")[1]
        jsonData = json.dumps(data)


        with open('database.json', 'w') as outfile:
            json.dump(jsonData, outfile)

        response = "RECEBI ESSE CARALHO!!!"
    
    if (http == "GET"):
        with open('database.json') as json_file:
            data = json.load(json_file)    

        response = data
    
    return response


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Define as opções do socket
    sock.bind((host, port))  # Associa o socket ao endereço IP e porta especificados

    print(f"Listening on port {port}...")
    sock.listen()  # Aguarda por conexões de entrada


    sock = context.wrap_socket(sock, server_side = True)
    conn, addr = sock.accept()  # Aceita uma conexão de um cliente

    with conn:
            print(f"Server {port} connected to client on socket {addr}")
            while True:
                data = conn.recv(1024)  # Recebe dados do cliente (máximo de BUFFER_SIZE bytes)
                data = data.decode("utf-8")  # Decodifica os dados recebidos de bytes para string
                if not data:
                    sock.close()  # Fecha o socket
                    print("NO connection. Finishing...")
                    print("No connection received. Closing.") 
                    break

                print(f"Received request {data}")
                response = handle_client(data)
                conn.sendall(response.encode("utf-8"))  # Envia a resposta de volta para o cliente

if __name__ == "__main__":
    main()