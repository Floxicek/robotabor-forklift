# Server (receive)
import socket, threading

# Modify based on the other PC
TARGET_IP = '192.168.8.137'
TARGET_PORT = 12345
MY_PORT = 25565

# True for sender, False for reciever
MASTER=True

def recv():
    s = socket.socket()
    s.bind(('0.0.0.0', MY_PORT))
    s.listen(1)
    conn, _ = s.accept()
    while True:
        data = conn.recv(1)
        if data:
            print("Received:", data)

if not MASTER:
    threading.Thread(target=recv, daemon=True).start()
    while True: pass

# Master (send)
s = socket.socket()
print(f'Connecting to {TARGET_IP}')
s.connect((TARGET_IP, TARGET_PORT))  # PC2’s receiver
print(f'Connected to {TARGET_IP}')
while True:
    msg = input("Send: ") + "\n"
    s.send(msg.encode())
