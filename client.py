import socket 
import cv2
import pickle
import struct
import sys
from datetime import datetime

def main(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set up IPv4 for streaming
    host_ip = socket.gethostbyname("haunter") # IP of device
    client_socket.connect((host_ip,int(port)))

    data = b""
    payload_size = struct.calcsize("Q")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.now()
    filename = "test.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    t = 0
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        out.write(frame)
        t += 1
        cv2.imshow("Receiving...",frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
    client_socket.close()
    out.release()

if __name__ == "__main__":
    main(sys.argv[1])