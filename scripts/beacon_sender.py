import time
import sys
import os

# Üst dizini path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.mesh_interface import MeshInterface

def start_beacon_loop(interval=10, message="BEACON_ALIVE"):
    """
    Belirli aralıklarla beacon sinyali gönderir.
    
    Args:
        interval (int): Saniye cinsinden döngü süresi.
        message (str): Gönderilecek mesaj içeriği.
    """
    interface = MeshInterface()
    if not interface.connect():
        print("CRITICAL: Bağlantı başarısız. Aborting.")
        return

    print("--- AUTOMATED BEACON SEQUENCE INITIATED ---")
    try:
        while True:
            interface.send_broadcast(f"AUTO-MSG: {message}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n--- SEQUENCE ABORTED BY USER ---")

if __name__ == "__main__":
    start_beacon_loop(interval=5, message="STATUS: GREEN | SECTOR: ALPHA")
