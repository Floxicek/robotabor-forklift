#!/usr/bin/env python3
import argparse, socket, sys
import threading
from pynput import keyboard
from time import sleep

# ---------- command-line args ----------
p = argparse.ArgumentParser(description="Control EV3 over TCP")
p.add_argument("ip", nargs="?", help="EV3 IP address")
p.add_argument("--ip", dest="ip_kw")
p.add_argument("--port", type=int, default=9999, help="TCP port (default 9999)")
args = p.parse_args()
EV3_IP = args.ip_kw or args.ip
PORT = args.port
if not EV3_IP:
    sys.exit("❌  Specify the EV3 IP with positional arg or --ip")

pressed_keys = set()

last_cmd = None

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
        sleep(0.1)  # Check every 100ms
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
with socket.socket() as s:
    print("Connecting to EV3...", EV3_IP)
    s.settimeout(5)
    s.connect((EV3_IP, PORT))
    print(f"✓ Connected to {EV3_IP}:{PORT}")

    watchdog_thread.start()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
print("Bye!")
