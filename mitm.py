import socket

host = "localhost"
portWoman = 12346
portServer = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de cliente
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Define as opções do socket
client.bind((host, portWoman))  # Liga o socket de cliente ao localhost e à porta 5051
client.listen()  # Aguarda conexões de entrada
client_conn, addr = client.accept()  # Aceita uma conexão de um cliente

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket de servidor
server.connect((host, portServer))  # Conecta ao servidor

def modify_bits(data, index):
    data_bytearray = bytearray(data)
    data_bytearray[index] ^= 1

    return bytes(data_bytearray)

def hexdump(package):
    n = 0
    while n < len(package):
        # String hexadecimal
        s1 = " ".join(f"{i:02x}" for i in package[n : n + 16])
        # Espaço extra entre grupos de 8 valores hexadecimais
        s1 = s1[0:23] + " " + s1[23:]
        # String ASCII, quando estiver fora do intervalo, exibe "."
        s2 = "".join(chr(i) if 32 <= i <= 127 else "." for i in package[n : n + 16])

        print(f"{n:08x}: {s1:<48}  {s2}")
        n += 16

def main():

    while True:

        package = client_conn.recv(1024)  # Recebe dados do cliente
        print("Cliente enviou:")
        hexdump(package)

        package = modify_bits(package, (len(package)-5))

        print("Modificado para:")
        hexdump(package)

        print("Enviando para o servidor...")
        server.sendall(package)  # Envia os dados modificados para o servidor

        package = server.recv(1024)  # Recebe dados do servidor
        print("Servidor enviou:")
        hexdump(package)

        print("Enviando para o cliente...")
        client_conn.sendall(package)  # Envia os dados recebidos para o cliente

if __name__ == "__main__":
    main()