import sys
import os
import time
import argparse

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.mesh_interface import MeshInterface

def scan_network(port, wait_time, continuous):
    print("\n" + "*"*45)
    print("      TACTICAL NETWORK SCANNER v2.0")
    print("*"*45)
    
    mesh = MeshInterface(port=port)
    if not mesh.connect():
        print("Failed to initialize interface.")
        return

    try:
        while True:
            print(f"Scanning for peers ({wait_time}s)...")
            time.sleep(wait_time) 
            
            nodes = mesh.get_peers()
            
            print(f"\n--- SCAN RESULTS: {len(nodes)} NODES FOUND ---")
            print(f"{'ID':<12} | {'CALLSIGN':<15} | {'BATT':<5} | {'SNR':<5}")
            print("-" * 45)
            
            for node in nodes:
                node_id = node.get('id', '???')
                name = node.get('name', 'UNKNOWN')
                batt = node.get('battery', 0)
                snr = node.get('snr', 0)
                
                print(f"{node_id:<12} | {name:<15} | {batt}%   | {snr} dB")
                
            print("-" * 45)
            
            if not continuous:
                break
                
            print("Waiting for next cycle... (Ctrl+C to stop)\n")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nScan terminated by operator.")
    finally:
        print("Closing interface.")
        if mesh.interface:
            mesh.interface.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meshtastic Taktiksel Ağ Tarayıcı")
    parser.add_argument("--port", type=str, default=None, help="Seri port")
    parser.add_argument("--wait", type=int, default=5, help="Tarama öncesi bekleme süresi")
    parser.add_argument("--loop", action="store_true", help="Sürekli tarama modu")
    
    args = parser.parse_args()
    scan_network(args.port, args.wait, args.loop)
