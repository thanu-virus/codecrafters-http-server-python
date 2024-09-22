# Uncomment this to pass the first stage
# import socket
import socket
import threading
def drecv(conn, buffersize):
    data = conn.recv(buffersize)
    try:
        data = data.decode()
    except:
        return -1
    finally:
        return data
def dsend(conn, data, buffersize=4096):
    conn.send(data.encode())
def status(index, raw=""):
    ok = "HTTP/1.1 200 OK\r\n"
    notok = "HTTP/1.1 404 Not Found\r\n\r\n"
    context = "Content-Type: text/plain\r\nContent-Length: "
    # context="HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\nContent-Length: "
    if index == "/":
        content = "Default page"
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    elif index == "/echo/abc/":
        content = "abc"
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
        # return context+str(len("abc"))+"\r\n"*2+"abc"+"\r\n"*2
    elif index[0:6] == "/echo/":
        content = index[6:]
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    elif index == "/user-agent":
        content = raw.split("\r\n")[2].split(" ", 1)[1]
        mes = ok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    else:
        # return "HTTP/1.1 404 Not Found\r\n\r\n"
        content = "Page was not found"
        mes = notok + context + str(len(content)) + "\r\n" * 2 + content + "\r\n" * 2
    return mes
def c_handler(conn, addr, buffersize=4096):
    def message(data):
        print("sending message: " + str(data))
        return dsend(conn, data)
    data = drecv(conn, buffersize)
    if data != 0 or data != -1:
        print(data)
        # dsend(conn, message)
        print("data: \n")
        print(data)
        p1 = data.split("\r\n")[0].split()[1]
        message(status(p1, data))
        """
        if p1 == "/":
            message("HTTP/1.1 200 OK\r\n\r\n")
        elif p1 == "/echo/abc":
            #message("abc
            mes="HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "
            content="abc"
            mes+=str(len(abc))+ "r\n"*2
            mes+=content+"\r\n"*2
            message(mes)
        else:
            message("HTTP/1.1 404 Not Found \r\n\r\n")
        """
    else:
        message(status())
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    # Uncomment this to pass the first stage
    #
    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_address = ("localhost", 4221)
    s.bind(server_address)
    s.listen()
    while True:
        conn, addr = s.accept()
        # c_handler(conn, addr)
        threading.Thread(target=c_handler, args=(conn, addr)).start()
if __name__ == "__main__":
    main()