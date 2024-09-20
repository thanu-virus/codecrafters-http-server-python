import socket

def main():
    print("Logs from your program will appear here!")
    
    # Create the server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    print("Server is listening on port 4221...")
    
    while True:
        try:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            
            # Send a simple HTTP response
            data=client_socket.recv(1024)
            if data:
                client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            client_socket.close()  # Close the client connection
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
