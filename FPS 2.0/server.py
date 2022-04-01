import socket
import time

c = None

def start_socket():
    global c

    host = '192.168.105.223'
    port = 35000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('', port))
    s.listen(1)
    print("Server started...")
    
    c, addr = s.accept()
    print("CONNECTION FROM:", str(addr))

def send_message(message):
    c.send(message.encode())
    print("Sent message: " + message)
  
def close_socket():
    c.send("".encode())
    c.close()
    print("Server closed.")

if __name__ == "__main__":
    start_socket()
    print("Socket started!!!")
    send_message("Hiiiii")
    time.sleep(10)
    send_message("Workssssss")
    close_socket()
