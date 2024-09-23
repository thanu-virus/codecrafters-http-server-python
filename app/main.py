import socket
import threading
import os

# Function to handle client requests
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

    # Handle /files/{filename} to serve file content
    elif len(path_parts) > 2 and path_parts[1] == "files":
        file_path = "/".join(path_parts[2:])  # Get the file
