import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection , address = server_socket.accept(1024) # wait for client
    if address:
        print(f"connection succeded with {address}")
    data = 200
    conection.sendall(data)

if __name__ == "__main__":
    main()
