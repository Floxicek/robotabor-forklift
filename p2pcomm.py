# Server (receive)
import socket, threading, random, time

# slave ip: 192.168.8.137
# slave port: 12345
# master ip:  192.168.8.217
# master port: 25565


# Modify based on the other PC
TARGET_IP = '192.168.8.137'
TARGET_PORT = 12345
MY_PORT = 25565

# command char
CHAR_SWITCH = 's'


def comm_init(is_master: bool):
    if is_master:
        threading.Thread(target=_master, daemon=True).start()
        while True: pass
    else:
        threading.Thread(target=_slave, daemon=True).start()
        while True: pass

def _slave():
    s = socket.socket()
    print(f'Connecting to {TARGET_IP}...')
    s.bind(('0.0.0.0', MY_PORT))
    s.listen(1)
    conn, _ = s.accept()
    print(f'Connected to {TARGET_IP}')
    while True:
        data = conn.recv(1)
        if data == CHAR_SWITCH:
            print("Changing!:", data)

def _master():
    # Master (send)
    s = socket.socket()
    print(f'Connecting to {TARGET_IP}...')
    s.connect((TARGET_IP, TARGET_PORT))  # PC2’s receiver
    print(f'Connected to {TARGET_IP}')
    while True:
        t0 = time.time()
        t1 = t0 + random.randint(10, 60)
        print(f'Waiting for: {t1-t0} s')
        while time.time() < t1: pass
        s.send(CHAR_SWITCH.encode())

def test_main():
    comm_init(True)


test_main()