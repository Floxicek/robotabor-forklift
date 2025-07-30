# 🏆 EV3 Forklift Tournament 🏆

This repository contains the script for an **ev3dev Lego Mindstorms forklift robot** designed for a competitive camp game. In this tournament, two teams compete to move as many packages as possible using their lego forklifts.  

Each team has **three members**, and each member controls **one motor** on the robot — so it's all about teamwork and coordination.

The system now supports **peer-to-peer communication** between two computers, allowing synchronized gameplay with automatic invert commands every 30 seconds.

---

## 🚀 Setup

1. **Sync the code:**  
   Copy the `forklift` folder to your EV3dev device.  

2. **Connect ev3dev device with the computer using bluetooth**

    Tutorial in this [link ev3dev.org](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)

3. **Start the control script on your computer:**  

    **For Master (Team 1):**
    
    ```bash
    python computer.py 10.42.0.3 --master true
    ```

    **For Slave (Team 2):**
    
    ```bash
    python computer.py 10.42.0.3
    ```

   Or using UV:

   ```bash
   uv run -- python computer.py 10.42.0.3 --master true
   # or for slave
   uv run -- python computer.py 10.42.0.3
   ```

## 🎮 Controls

- **W/S**: Left motor forward/back
- **Up/Down**: Right motor forward/back  
- **I/K**: Lift up/down
- **Space**: Invert controls
- **G**: Start game (master only)
- **Esc**: Exit

## � P2P Communication

The system supports communication between two computers:

- **Master**: Sends game start signal and invert commands every 30 seconds
- **Slave**: Receives and responds to commands from master

### Testing P2P Communication

Use the test script to verify communication:

```bash
# On first computer (master)
python test_p2p.py master

# On second computer (slave)  
python test_p2p.py slave
```

### Network Configuration

Update the IP addresses in `p2pcomm.py`:

- `TARGET_IP`: IP address of the other computer
- `TARGET_PORT`: Port for slave (default: 12345)
- `MY_PORT`: Port for master (default: 25565)

## �💻 Python Requirements

- Python version: `3.11.9` (On the newer version i couldn't get pynput working)

- Packages: `pynput`
