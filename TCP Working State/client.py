import socket

s = None

def start_socket():
    global s

    host = '129.215.3.209'
    port = 35000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

def receive_message():
    msg = s.recv(1024).decode()
    print("Received: " + msg)

def close_socket():
    # disconnect the client
    s.close()
    print("Socket closed.")

if __name__ == "__main__":
    start_socket()
    while True:
        message = receive_message()
        if message == "":
            break
    close_socket()