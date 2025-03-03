import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.38"
PEER_PORT = 10001

MESSAGE = b"Salut!"
i = 0

idx = 0
MESSAGE_0 = b"GPIO4=0"
MESSAGE_1 = b"GPIO4=1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        if idx==0:
            TO_SEND = MESSAGE_0
            sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
            print("Am trimis mesajul: ", TO_SEND)
            idx=1
            time.sleep(1)
        else :
            if idx==1:
                TO_SEND = MESSAGE_1
                sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
                print("Am trimis mesajul: ", TO_SEND)
                idx=0
                time.sleep(1)
        # TO_SEND = MESSAGE + bytes(str(i),"ascii")
        # sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
        # print("Am trimis mesajul: ", TO_SEND)
        # i = i + 1
        # time.sleep(1)
    except KeyboardInterrupt:
        break