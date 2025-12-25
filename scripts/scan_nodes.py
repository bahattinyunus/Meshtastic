import sys
import os
import time

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.mesh_interface import MeshInterface

def scan_network():
    print("Initializing TACTICAL SCANNER based on core/mesh_interface...")
    mesh = MeshInterface()
    
    if not mesh.connect():
        print("Failed to initialize interface.")
        return

    print("Scanning for peers (5 seconds)...")
    time.sleep(5) # Wait for mesh to populate if real
    
    nodes = mesh.get_peers()
    
    print(f"\n--- SCAN RESULTS: {len(nodes)} NODES FOUND ---")
    print(f"{'ID':<15} | {'CALLSIGN':<20} | {'BATT':<5} | {'SNR':<5}")
    print("-" * 55)
    
    for node in nodes:
        node_id = node.get('id', '???')
        name = node.get('name', 'UNKNOWN')
        batt = node.get('battery', 0)
        snr = node.get('snr', 0)
        
        print(f"{node_id:<15} | {name:<20} | {batt}%   | {snr} dB")
        
    print("-" * 55)
    print("END OF SCAN")

    if mesh.interface:
        mesh.interface.close()

if __name__ == "__main__":
    scan_network()
