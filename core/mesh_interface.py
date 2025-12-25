import datetime
import logging
import time
import sys

try:
    import meshtastic
    import meshtastic.serial_interface
    from pubsub import pub
    HAS_MESHTASTIC = True
except ImportError:
    HAS_MESHTASTIC = False

class MeshInterface:
    """
    Meshtastic Taktiksel Ağ Arayüzü (Tactical Mesh Interface)
    
    Bu sınıf, Meshtastic cihazı ile iletişim kurmak için ana kontrol katmanını oluşturur.
    Gerçek donanım bağlantısı için 'meshtastic' kütüphanesini sarmalar.
    Eğer donanım yoksa veya kütüphane eksikse simülasyon moduna geçer.
    """

    def __init__(self, port=None):
        self.logger = self._setup_logger()
        self.port = port
        self.interface = None
        self.connected = False
        self.logger.info("Initializing Tactical Mesh Interface...")
        
        if not HAS_MESHTASTIC:
            self.logger.warning("Meshtastic library not found. Running in SIMULATION mode.")

    def _setup_logger(self):
        logger = logging.getLogger("MeshOps")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [TACTICAL] - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def connect(self):
        """Cihaza bağlantı kurar."""
        self.logger.info(f"Scanning for device on port: {self.port if self.port else 'AUTO'}")
        
        if HAS_MESHTASTIC:
            try:
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
                self.connected = True
                self.logger.info(f"CONNECTION ESTABLISHED with node: {self.interface.getMyNodeInfo()['user']['longName']}")
                
                # Event listener ekle
                pub.subscribe(self._on_receive, "meshtastic.receive")
                
                return True
            except Exception as e:
                self.logger.error(f"Hardware connection failed: {e}")
                self.logger.info("Falling back to SIMULATION mode.")
                self.connected = False
                # Fallthrough to simulation return True for testing purposes
                return True
        else:
            # Simulation
            time.sleep(1)
            self.connected = True
            self.logger.info("SIMULATION CONNECTION ESTABLISHED with node: TALON-1 (VIRTUAL)")
            return True

    def _on_receive(self, packet, interface):
        """Mesaj alındığında tetiklenir."""
        try:
            if 'decoded' in packet and 'text' in packet['decoded']:
                text = packet['decoded']['text']
                sender = packet['fromId']
                self.logger.info(f"INCOMING TRANSMISSION [{sender}]: {text}")
        except Exception as e:
            self.logger.error(f"Packet parsing error: {e}")

    def send_broadcast(self, message):
        """Ağa yayın mesajı gönderir (Broadcast)."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_msg = f"<{timestamp}> {message}"

        if self.connected and self.interface:
            self.interface.sendText(full_msg)
            self.logger.info(f"Broadcasting via RF >> {full_msg}")
            return True
        elif self.connected: # Simulation
            self.logger.info(f"[SIMULATION] Broadcasting >> {full_msg}")
            return True
        else:
            self.logger.error("No active connection. Cannot send message.")
            return False

    def get_peers(self):
        """Ağdaki diğer düğümleri listeler."""
        if self.connected and self.interface:
            nodes = []
            if self.interface.nodes:
                for node_id, node_info in self.interface.nodes.items():
                    # Parse interesting info
                    user = node_info.get('user', {})
                    metrics = node_info.get('deviceMetrics', {})
                    snr = node_info.get('snr', 0)
                    
                    nodes.append({
                        "id": node_id,
                        "name": user.get('longName', 'Unknown'),
                        "battery": metrics.get('batteryLevel', 0),
                        "snr": snr
                    })
            return nodes
        else:
            # Mock data return
            return [
                {"id": "!1234abcd", "name": "EAGLE-EYE (SIM)", "battery": 85, "snr": 10.5},
                {"id": "!5678efgh", "name": "GHOST-RECON (SIM)", "battery": 42, "snr": 8.2}
            ]

if __name__ == "__main__":
    mesh = MeshInterface()
    if mesh.connect():
        mesh.send_broadcast("CQ CQ CQ - This is Command Post testing RF link.")
        time.sleep(2)
        print("Known Peers:", mesh.get_peers())
        if mesh.interface:
            mesh.interface.close()
