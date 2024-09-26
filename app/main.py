import socket
import threading
import sys
import gzip
import io

def main():
    def handle_req(client, addr):
        try:
            data = client.recv(1024).decode()
            req = data.split("\r\n")
            path = req[0].split(" ")[1]
            method = req[0].split(" ")[0]  # GET or POST

            # Handle POST request (File Upload)
            if method == "POST" and path.startswith("/files"):
                directory = sys.argv[2]
                filename = path[7:]  # Extract filename from URL
                content = req[-1]    # The content of the POST request is typically in the last part of the request

                print(f"Writing to {directory}/{filename}")
                try:
                    # Open the file in write mode and write the content
                    with open(f"{directory}/{filename}", "w") as f:
                        f.write(content)
                    
                    response_body = f"File '{filename}' created successfully."
                    response = f"HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode()
                except Exception as e:
                    response = f"HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()

            # Handle GET request (Homepage or file access)
            elif method == "GET":
                if path == "/":
                    response = "HTTP/1.1 200 OK\r\n\r\nWelcome to the server!".encode()

                # Handle the /echo endpoint with Gzip compression
                elif path.startswith("/echo"):
                    content = path[6:]  # Echo content after "/echo"

                    # Check for Accept-Encoding header and Gzip support
                    accept_encoding_header = next((h for h in req if h.startswith("Accept-Encoding:")), "")
                    if "gzip" in accept_encoding_header:
                        # Compress the content using Gzip
                        buf = io.BytesIO()
                        with gzip.GzipFile(fileobj=buf, mode='wb') as gz:
                            gz.write(content.encode())

                        gzipped_content = buf.getvalue()
                        response = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(gzipped_content)}\r\n\r\n".encode() + gzipped_content
                    else:
                        # No Gzip compression
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()

                elif path.startswith("/user-agent"):
                    user_agent = req[2].split(": ")[1]
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()

                elif path.startswith("/files"):
                    directory = sys.argv[2]
                    filename = path[7:]  # Extract filename from URL

                    print(f"Reading from {directory}/{filename}")
                    try:
                        with open(f"{directory}/{filename}", "r") as f:
                            body = f.read()
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
                    except Exception as e:
                        response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

            # Handle unknown methods or invalid paths
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

            # Send the response back to the client
            client.send(response)
        except Exception as e:
            print(f"Error handling request from {addr}: {e}")
        finally:
            client.close()

    try:
        # Create and bind the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
        server_socket.bind(("localhost", 4221))
        server_socket.listen(5)  # Allow 5 pending connections
        print("Server running on http://localhost:4221")
    except Exception as e:
        print(f"Error creating server: {e}")
        sys.exit(1)

    # Listen for incoming connections
    while True:
        try:
            client, addr = server_socket.accept()
            threading.Thread(target=handle_req, args=(client, addr)).start()
        except Exception as e:
            print(f"Error accepting client: {e}")

if __name__ == "__main__":
    main()
