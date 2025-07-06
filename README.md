# 🏆 EV3 Forklift Tournament 🏆

This repository contains the script for an **ev3dev Lego Mindstorms forklift robot** designed for a competitive camp game. In this tournament, two teams compete to move as many packages as possible using their lego forklifts.  

Each team has **three members**, and each member controls **one motor** on the robot — so it's all about teamwork and coordination  

---

## 🚀 Setup

1. **Sync the code:**  
   Copy the `forklift` folder to your EV3dev device.  

2. Connect ev3dev device with the computer using bluetooth

    Tutorial in this [link ev3dev.org](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)

3. **Start the control script on your computer:**  

    **Use corresponding ip** (it is displayed on the ev3dev device)

   ```bash
   python computer.py 10.42.0.3
   ```

   Or using UV

   ```bash
   uv run -- python computer.py 10.42.0.3
   ```

## 💻 Python Requirements

- Python version: `3.11.9` (On the newer version i couldn't get pyinput working)

- Packages: `pyinput`
