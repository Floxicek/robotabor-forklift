#!/usr/bin/env python3
"""
Test script for P2P communication
Run this on one computer as master and another as slave to test the communication.
"""

import p2pcomm
import time

def test_invert_handler(data):
    print("🔄 Test: Received invert command!")

def main():
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['master', 'slave']:
        print("Usage: python test_p2p.py [master|slave]")
        sys.exit(1)
    
    is_master = sys.argv[1] == 'master'
    
    print(f"🔗 Starting as {'master' if is_master else 'slave'}")
    
    # Initialize communication
    p2pcomm.comm_init(is_master=is_master)
    
    if not is_master:
        # Register test handler for invert messages
        p2pcomm.register_handler("invert", test_invert_handler)
        print("📥 Slave ready to receive messages...")
        
        # Keep slave running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Slave shutting down...")
    else:
        print("📤 Master ready to send messages...")
        time.sleep(2)  # Give slave time to connect
        
        # Send game start message
        print("🎮 Sending game start...")
        p2pcomm.send("game_start", {"start_time": time.time()})
        
        # Send some test invert messages
        for i in range(3):
            time.sleep(5)
            print(f"🔄 Sending invert message {i+1}")
            p2pcomm.send("invert")
        
        print("✅ Test completed")
    
    # Cleanup
    p2pcomm.close_connection()

if __name__ == "__main__":
    main()
