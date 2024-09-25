import socket
import threading
import sys

def main():
    def handle_req(client, addr):
        try:
            data = client.recv(1024).decode()
            req = data.split("\r\n")
            path = req[0].split(" ")[1]
            pathb=req[0].split(" ")[0]
            if pathb=="POST":
                directory = sys.argv[2]
                filename = path[7:]
                content=req[-1]
                print(directory, filename)
                try:
                    with open(f"{directory}/{filename}", "w") as f:
                        body = f.write(contents)
                    response = f"HTTP/1.1 201 created\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                except Exception as e:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

            if path == "/":
                response = "HTTP/1.1 200 OK\r\n\r\n".encode()
            elif path.startswith("/echo"):
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()
            elif path.startswith("/user-agent"):
                user_agent = req[2].split(": ")[1]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
            elif path.startswith("/files"):
                directory = sys.argv[2]
                filename = path[7:]
                print(directory, filename)
                try:
                    with open(f"{directory}/{filename}", "r") as f:
                        body = f.read()
                    response = f"GET /files/{filename} HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                except Exception as e:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

            client.send(response)
        except Exception as e:
            print(f"Error handling request from {addr}: {e}")
        finally:
            client.close()

    try:
        # Manually create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
        server_socket.bind(("localhost", 4221))
        server_socket.listen(5)  # Allow 5 pending connections
        print("Server running on http://localhost:4221")
    except Exception as e:
        print(f"Error creating server: {e}")
        sys.exit(1)

    while True:
        try:
            client, addr = server_socket.accept()
            threading.Thread(target=handle_req, args=(client, addr)).start()
        except Exception as e:
            print(f"Error accepting client: {e}")

if __name__ == "__main__":
    main()
