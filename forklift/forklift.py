#!/usr/bin/env python3
import socket, subprocess, re

# from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_C, OUTPUT_D, StopAction, SpeedDPS
from ev3dev2.motor import *
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from time import sleep


# ---------- utility ----------------------------------------------------------
def get_ip() -> str:
    """
    Return the first non-loopback IPv4 found.
    Works over Wi-Fi, USB-ethernet or Bluetooth PAN.
    """
    try:  # 1) fast path: hostname -I
        ips = subprocess.check_output(["hostname", "-I"]).decode().split()
        for ip in ips:
            if re.match(r"^\d+\.\d+\.\d+\.\d+$") and not ip.startswith("127."):
                return ip
    except Exception:
        pass  # 2) fall-back: UDP trick
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # no packets actually leave the brick
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "unknown"


# ----- variables ----
inversed = False
default_speed = -400


speed = -300
lift_speed = 700
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_D)
# right_motor.ramp_up_sp = 13
# left_motor.ramp_up_sp = 13


lift_motor = MediumMotor(OUTPUT_C)

speaker = Sound()

while True:  # Loop to keep the script running
    # ---------- show IP on LCD ---------------------------------------------------
    ip = get_ip()
    print("IP address: ", ip)

    # ---------- normal socket server --------------------------------------------
    srv = socket.socket()
    srv.bind(("0.0.0.0", 9999))
    srv.listen(1)
    print("Waiting for PC client")
    conn, addr = srv.accept()
    print("Connected from", addr)


    try:
        while True:
            data = conn.recv(16)
            if not data:
                break
            cmd = data.decode().strip().upper()
            if cmd == "LEFT_ON":
                left_motor.run_forever(speed_sp=speed if not inversed else -speed)
            elif cmd == "LEFT_OFF":
                left_motor.stop()
            elif cmd == "LEFT_BACK":
                left_motor.run_forever(speed_sp=-speed if not inversed else speed)
            elif cmd == "RIGHT_ON":
                right_motor.run_forever(speed_sp=speed if not inversed else -speed)
            elif cmd == "RIGHT_OFF":
                right_motor.stop()
            elif cmd == "RIGHT_BACK":
                right_motor.run_forever(speed_sp=-speed if not inversed else speed)
            elif cmd == "LIFT_ON":
                lift_motor.run_forever(
                    speed_sp=lift_speed if not inversed else -lift_speed
                )
            elif cmd == "LIFT_BACK":
                lift_motor.run_forever(
                    speed_sp=-lift_speed if not inversed else lift_speed
                )
            elif cmd == "LIFT_OFF":
                lift_motor.stop()
            elif cmd == "INVERT":
                speaker.play_tone(
                    frequency=440,
                    duration=0.5,
                    volume=80,
                    play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE,
                )
                inversed = not inversed

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
        srv.close()
        left_motor.stop()
        right_motor.stop()
        lift_motor.stop()
