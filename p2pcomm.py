# Server (receive)
import socket, threading

TARGET_IP = '192.168.1.101'
TARGET_PORT = 12346
MY_PORT = 12345

def recv():
    s = socket.socket()
    s.bind(('0.0.0.0', MY_PORT))
    s.listen(1)
    conn, _ = s.accept()
    while True:
        data = conn.recv(1)
        if data:
            print("Received from PC2:", data)
threading.Thread(target=recv, daemon=True).start()

# Client (send)
s = socket.socket()
s.connect((TARGET_IP, TARGET_PORT))  # PC2’s receiver
while True:
    msg = input("Send to PC2: ")
    s.send(msg.encode())
