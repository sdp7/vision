import socket
from telnetlib import KERMIT 
import cv2
import pickle
import struct
import sys

def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set up IPv4 for streaming
    host_name = socket.gethostname() #Name of device
    host_ip = socket.gethostbyname(host_name) # IP of device
    print(host_name, host_ip)
    socket_address = (host_ip, int(port))
    print("Socket Created")

    server_socket.bind(socket_address)
    print("Socket binding complete")

    server_socket.listen(5)
    server_status = True
    print("Socket now listening")
    
    while server_status:
        client_socket, addr = server_socket.accept()
        print("Connection from:",addr)
        if client_socket:
            vid = cv2.VideoCapture(2)
            while (vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a)) + a
                client_socket.sendall(message)


if __name__ == "__main__":
    main(sys.argv[1])