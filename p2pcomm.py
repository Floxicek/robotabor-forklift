# P2P Communication Module
import socket, threading, json, time

# slave ip: 192.168.8.137
# slave port: 12345
# master ip:  192.168.8.217
# master port: 25565

# Modify based on the other PC
TARGET_IP = "192.168.8.131"
TARGET_PORT = 25565
MY_PORT = 25565

# Global variables
_is_master = False
_connection = None
_socket = None
_game_started = False
_start_time = None
_custom_handlers = {}

def comm_init(is_master: bool):
    global _is_master
    _is_master = is_master
    if is_master:
        threading.Thread(target=_master, daemon=True).start()
    else:
        threading.Thread(target=_slave, daemon=True).start()
    
    # Give some time for initial connection attempt
    time.sleep(0.5)

def send(message_type, data=None):
    """Send a message to the other computer"""
    global _connection, _game_started, _start_time
    if not _connection:
        print("⚠️ No connection established")
        return
    
    message = {
        "type": message_type,
        "data": data,
        "timestamp": time.time()
    }
    
    # If master is sending game_start, update local state too
    if message_type == "game_start" and _is_master:
        _game_started = True
        _start_time = data.get("start_time") if data else None
        print(f"🎮 Master: Game started locally! Start time: {_start_time}")
    
    try:
        message_str = json.dumps(message) + "\n"
        _connection.sendall(message_str.encode())
        print(f"📤 Sent: {message_type}")
    except Exception as e:
        print(f"⚠️ Failed to send message: {e}")

def register_handler(message_type, handler_func):
    """Register a custom handler for a specific message type"""
    global _custom_handlers
    _custom_handlers[message_type] = handler_func

def _slave():
    global _connection, _socket
    _socket = socket.socket()
    print(f"🔌 Slave listening on port {MY_PORT}...")
    _socket.bind(("0.0.0.0", MY_PORT))
    _socket.listen(1)
    _connection, addr = _socket.accept()
    print(f"✓ Connected to master at {addr[0]}")
    
    buffer = ""
    while True:
        try:
            data = _connection.recv(1024).decode()
            if not data:
                break
            
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    try:
                        message = json.loads(line)
                        print(f"📥 Received: {message.get('type')}")
                        _handle_message(message)
                    except json.JSONDecodeError:
                        print(f"⚠️ Invalid message received: {line}")
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
            break

def _master():
    global _connection, _socket, _game_started, _start_time
    _socket = socket.socket()
    print(f"🔌 Master connecting to {TARGET_IP}:{TARGET_PORT}...")
    try:
        _socket.connect((TARGET_IP, TARGET_PORT))
        _connection = _socket
        print(f"✓ Connected to slave at {TARGET_IP}")
        
        # Start the invert timer thread
        threading.Thread(target=_invert_timer, daemon=True).start()
        
    except Exception as e:
        print(f"❌ Failed to connect to slave: {e}")

def _handle_message(message):
    """Handle incoming messages on slave"""
    global _game_started, _start_time, _custom_handlers
    
    message_type = message.get("type")
    data = message.get("data")
    
    if message_type == "game_start":
        _game_started = True
        _start_time = data.get("start_time") if data else None
        print(f"🎮 Game started! Start time: {_start_time}")
        
    elif message_type == "invert":
        print("🔄 Received invert command")
        # Check for custom handler
        if "invert" in _custom_handlers:
            _custom_handlers["invert"](data)
        
    elif message_type in _custom_handlers:
        # Use custom handler if available
        _custom_handlers[message_type](data)
        
    else:
        print(f"📥 Received unknown message type: {message_type}")

def _invert_timer():
    """Send invert message every 30 seconds (only for master)"""
    global _game_started
    print("🔄 Invert timer thread started, waiting for game to start...")
    
    # Wait for the game to start
    while not _game_started:
        time.sleep(0.5)
    
    print("🎮 Game started! Invert timer now active - sending invert every 30 seconds")
    
    while _game_started and _connection:
        time.sleep(30)  # Wait 30 seconds
        if _game_started and _connection:
            print("⏰ 30 seconds elapsed - sending invert command")
            send("invert")

def is_game_started():
    """Check if the game has started"""
    return _game_started

def get_start_time():
    """Get the game start time"""
    return _start_time

def close_connection():
    """Close the connection"""
    global _connection, _socket
    if _connection:
        _connection.close()
    if _socket:
        _socket.close()
