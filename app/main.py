import socket
def main():
    server_socket: socket.socket = socket.create_server(
        ("localhost", 4221), reuse_port=True
    )
    client: socket.socket
    client, addr = server_socket.accept()
    data: str = client.recv(1024).decode()
    request_data: list[str] = data.split("\r\n")
    path_parts: list[str] = request_data[0].split(" ")[1].split("/")
    if len(path_parts) > 2 and path_parts[1] == "echo":  # Check if the path is like /echo/{something}
        string_to_echo = path_parts[2]  # The part after /echo/
        response_body = string_to_echo
        response: bytes = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n\r\n"
        f"{response_body}\r\n"
        ).encode()
    elif request_data[2] != "" and path_parts[1]=="user-agent":
        string_to_echo = request_data[2].split(" ")[1]# The part after /echo/
        response_body = string_to_echo
        response: bytes = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n\r\n"
        f"{response_body}\r\n"
        ).encode()
    elif request_data[0].split(" ")[1] != "/":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    else:
        response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    client.send(response)
    client.close()
    server_socket.close()
if __name__ == "__main__":
    main()