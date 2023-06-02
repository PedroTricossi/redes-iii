import socket
import ssl
import time

dados = {
    'nome':'pedro'
}

host = "localhost"
port = 12346
certfile = "localhost.crt"  # Path to your server certificate file
keyfile = "localhost.key"  # Path to your server private key file

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(certfile)
context.load_cert_chain(certfile = certfile, keyfile = keyfile)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock = context.wrap_socket(sock, server_hostname = host)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Tenta se conectar ao servidor
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            sock.close()
            print(f"Error: Could not connect to server server")
            exit()
        
        print(f"Connected to server on port {port}...")

        # Loop principal do cliente
        while True:
            message = f'POST/{dados}'
            data = message.encode('UTF-8')  # Codifica os dados

            sock.sendall(data)  # Envia os dados codificados pelo socket

            sock.settimeout(1.0)  # Timeout de 1 segundo

            # Espera pela resposta do servidor
            try:
                data = sock.recv(1024)  # Recebe os dados do servidor (buffer de BUFFER_SIZE bytes)
                data = data.decode("utf-8")  # Decodifica os dados
                print(f"RESPOSTA: {data}")
            except socket.timeout:
                print("No data was received from server, timeout.")
                print("Server timeout.")
            except:
                sock.close()

if __name__ == '__main__':
    main()