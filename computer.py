#!/usr/bin/env python3
import argparse, socket, sys
import threading, time
from pynput import keyboard
import p2pcomm

start_time = None

# ---------- command-line args ----------
p = argparse.ArgumentParser(description="Control EV3 over TCP")
p.add_argument("ip", nargs="?", help="EV3 IP address")
p.add_argument("--ip", dest="ip_kw")
p.add_argument("--port", type=int, default=9999, help="TCP port (default 9999)")
p.add_argument(
    "--master", type=bool, default=False, help="Run as master (default False)"
)
args = p.parse_args()
EV3_IP = args.ip_kw or args.ip
PORT = args.port
if not EV3_IP:
    sys.exit("❌  Specify the EV3 IP with positional arg or --ip")

pressed_keys = set()

last_cmd = None


def start_game():
    global start_time
    if not args.master:
        print("⚠️ Only master can start the game!")
        return
    start_time = time.time()
    print(f"🎮 Starting game at {start_time}")
    p2pcomm.send("game_start", {"start_time": start_time})
    
def send_invert():
    p2pcomm.send("invert")

def handle_invert_message(data):
    """Handle invert message received from master"""
    print("🔄 Processing invert command from master")
    # Send invert command to EV3
    send_cmd("INVERT")


def send_cmd(cmd):
    """Send a command to the EV3 and print it."""
    global last_cmd
    try:
        s.sendall((cmd + "\n").encode())
        print(f"→ {cmd}")
        last_cmd = cmd
    except Exception as e:
        print(f"⚠️ Failed to send: {e}")


def watchdog():
    while True:
        # print("Checking for pressed keys...")
        time.sleep(0.1)  # Check every 100ms
        if not pressed_keys:
            if last_cmd != "OFF":
                print("No keys pressed -> Sending OFF command")
                send_cmd("OFF")


def on_press(key):
    if key in pressed_keys:
        return
    if key == keyboard.KeyCode(char="w"):
        cmd = "LEFT_ON"
    elif key == keyboard.KeyCode(char="s"):
        cmd = "LEFT_BACK"
    elif key == keyboard.Key.up:
        cmd = "RIGHT_ON"
    elif key == keyboard.Key.down:
        cmd = "RIGHT_BACK"
    elif key == keyboard.KeyCode(char="i"):
        cmd = "LIFT_ON"
    elif key == keyboard.KeyCode(char="k"):
        cmd = "LIFT_BACK"
    elif key == keyboard.Key.space:
        cmd = "INVERT"
    elif key == keyboard.KeyCode(char="g"):  # G key to start game
        start_game()
        return
    else:
        return

    pressed_keys.add(key)
    send_cmd(cmd)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    if key in pressed_keys:
        if key == keyboard.KeyCode(char="w"):
            if keyboard.KeyCode(char="s") in pressed_keys:
                cmd = "LEFT_BACK"
            else:
                cmd = "LEFT_OFF"
        elif key == keyboard.KeyCode(char="s"):
            if keyboard.KeyCode(char="w") in pressed_keys:
                cmd = "LEFT_ON"
            else:
                cmd = "LEFT_OFF"
        elif key == keyboard.Key.up:
            if keyboard.Key.down in pressed_keys:
                cmd = "RIGHT_BACK"
            else:
                cmd = "RIGHT_OFF"
        elif key == keyboard.Key.down:
            if keyboard.Key.up in pressed_keys:
                cmd = "RIGHT_ON"
            else:
                cmd = "RIGHT_OFF"

        elif key == keyboard.KeyCode(char="i"):
            if keyboard.KeyCode(char="k") in pressed_keys:
                cmd = "LIFT_BACK"
            else:
                cmd = "LIFT_OFF"
        elif key == keyboard.KeyCode(char="k"):
            if keyboard.KeyCode(char="i") in pressed_keys:
                cmd = "LIFT_ON"
            else:
                cmd = "LIFT_OFF"
        else:
            return
        pressed_keys.remove(key)
        send_cmd(cmd)
    else:
        if not pressed_keys:
            send_cmd("OFF")
        return


watchdog_thread = threading.Thread(target=watchdog, daemon=True)

# Initialize P2P communication
print(f"🔗 Initializing P2P communication (Master: {args.master})")
p2pcomm.comm_init(is_master=args.master)

# Register invert handler for slave
if not args.master:
    p2pcomm.register_handler("invert", handle_invert_message)

time.sleep(1)  # Give time for connection to establish

with socket.socket() as s:
    print("Connecting to EV3...", EV3_IP)
    s.settimeout(5)
    s.connect((EV3_IP, PORT))
    print(f"✓ Connected to {EV3_IP}:{PORT}")

    watchdog_thread.start()
    
    print("🎮 Controls:")
    print("  W/S: Left motor forward/back")
    print("  Up/Down: Right motor forward/back") 
    print("  I/K: Lift up/down")
    print("  Space: Invert")
    print("  G: Start game (master only)")
    print("  Esc: Exit")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Clean up P2P connection
p2pcomm.close_connection()
print("Bye!")
