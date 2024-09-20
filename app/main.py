import socket
def main():
    server_socket: socket.socket = socket.create_server(
        ("localhost", 4221), reuse_port=True
    )
    client: socket.socket
    client, addr = server_socket.accept()
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")
    response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    if request_data[0].split(" ")[1] != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    client.send(response)
    client.close()
    server_socket.close()
if __name__ == "__main__":
    main()