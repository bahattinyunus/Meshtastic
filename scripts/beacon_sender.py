import time
import sys
import os
import argparse

# Üst dizini path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.mesh_interface import MeshInterface

def start_beacon_loop(interval, message, port):
    """
    Belirli aralıklarla beacon sinyali gönderir.
    """
    interface = MeshInterface(port=port)
    if not interface.connect():
        print("CRITICAL: Bağlantı başarısız. Aborting.")
        return

    print("\n" + "="*45)
    print("   TACTICAL BEACON SEQUENCE INITIATED")
    print("="*45)
    print(f"Interval: {interval}s")
    print(f"Message : {message}")
    print(f"Port    : {port if port else 'AUTO'}")
    print("="*45 + "\n")

    seq = 0
    try:
        while True:
            seq += 1
            full_msg = f"SEQ:{seq:04d} | {message}"
            interface.send_broadcast(full_msg)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n--- SEQUENCE ABORTED BY USER ---")
        if interface.interface:
            interface.interface.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meshtastic Taktiksel Beacon Gönderici")
    parser.add_argument("--interval", type=int, default=15, help="Sinyal aralığı (saniye)")
    parser.add_argument("--msg", type=str, default="STATUS: GREEN", help="Gönderilecek mesaj")
    parser.add_argument("--port", type=str, default=None, help="Seri port (örn: COM3)")
    
    args = parser.parse_args()
    start_beacon_loop(args.interval, args.msg, args.port)
