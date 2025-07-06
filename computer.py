#!/usr/bin/env python3
import argparse, socket, sys
from pynput import keyboard

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

last_key = None


def on_press(key):
    global last_key
    if key == last_key:
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
        cmd = "LIFT_UP"
    elif key == keyboard.KeyCode(char="k"):
        cmd = "LIFT_DOWN"
    elif key == keyboard.Key.space:
        cmd = "LIFT_STOP"
    else:
        return

    last_key = key
    s.sendall((cmd + "\n").encode())
    print(f"→ {cmd}")


def on_release(key):
    # TODO Handle release when multiple keys are pressed
    global last_key
    if key == last_key:
        last_key = None
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

    if key == keyboard.KeyCode(char="w") or key == keyboard.KeyCode(char="s"):
        cmd = "LEFT_OFF"
    elif key == keyboard.Key.up or key == keyboard.Key.down:
        cmd = "RIGHT_OFF"
    elif key == keyboard.KeyCode(char="i") or key == keyboard.KeyCode(char="k"):
        cmd = "LIFT_STOP"
    else:
        return
    s.sendall((cmd + "\n").encode())
    print(f"→ {cmd}")


# ---------- socket ----------
with socket.socket() as s:
    print("Connecting to EV3...", EV3_IP)
    s.connect((EV3_IP, PORT))
    print(f"✓ Connected to {EV3_IP}:{PORT}  –  press q to quit")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

print("Bye!")
