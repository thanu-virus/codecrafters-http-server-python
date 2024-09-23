import socket
import threading

def handle_client(client_socket: socket.socket):
    data: str = client_socket.recv(1024).decode()
    
    if not data:
        client_socket.close()
        return

    request_data: list[str] = data.split("\r\n")
    path_parts: list[str] = request_data[0].split(" ")[1].split("/")
    
    # Handle /echo/{something}
    if len(path_parts) > 2 and path_parts[1] == "echo":
        string_to_echo = path_parts[2]  # The part after /echo/
        response_body = string_to_echo
        response: bytes = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(response_body)}\r\n\r\n"
            f"{response_body}\r\n"
        ).encode()

    # Handle /user-agent and extract the User-Agent header
    elif len(path_parts) > 1 and path_parts[1] == "user-agent":
        user_agent_header = next(
            (header for header in request_data if header.startswith("User-Agent:")), 
            None
        )
        if user_agent_header:
            response_body = user_agent_header.split(": ", 1)[1]
            response: bytes = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body)}\r\n\r\n"
                f"{response_body}\r\n"
            ).encode()
    elif len(path_parts) > 1 and path_parts[1] == "files":
        string_to_echo = path_parts[2]  # The part after /echo/
        response_body = string_to_echo
        response: bytes = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(response_body)}\r\n\r\n"
                f"{response_body}\r\n"
            ).encode()

    # Handle any other request path
    elif path_parts[1] != "":
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    # Default response (for root path `/`)
    else:
        response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()

    client_socket.send(response)
    client_socket.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print("Server is running and waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
