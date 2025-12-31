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
    
    Bu sınıf, Meshtastic donanımı ile üst seviye yazılım katmanları arasında bir köprü görevi görür.
    'meshtastic' kütüphanesini sarmalayarak veri gönderimi, düğüm taraması ve olay yönetimini sağlar.
    Donanım erişimi olmadığında sistem sürekliliği için otomatik Simülasyon Modu'na sahiptir.

    Attributes:
        port (str): Cihazın bağlı olduğu seri port (örn: 'COM3', '/dev/ttyUSB0').
        interface (SerialInterface): Meshtastic kütüphanesinin aktif arayüz nesnesi.
        connected (bool): Bağlantı durumunu gösteren bayrak.
    """

    def __init__(self, port=None):
        """
        MeshInterface sınıfını başlatır.
        
        Args:
            port (str, optional): Seri port yolu. Belirtilmezse sistem otomatik tarama yapar.
        """
        self.logger = self._setup_logger()
        self.port = port
        self.interface = None
        self.connected = False
        self.logger.info("Initializing Tactical Mesh Interface...")
        
        if not HAS_MESHTASTIC:
            self.logger.warning("Meshtastic library not found. Running in SIMULATION mode.")

    def _setup_logger(self):
        """
        Taktiksel operasyonlar için özelleştirilmiş loglama yapısını kurar.
        
        Returns:
            logging.Logger: Yapılandırılmış logger nesnesi.
        """
        logger = logging.getLogger("MeshOps")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [TACTICAL] - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def connect(self):
        """
        Belirtilen port üzerinden donanım bağlantısını kurar.
        
        Donanım bulunamazsa veya hata oluşursa güvenli bir şekilde Simülasyon Modu'na geçer.

        Returns:
            bool: Bağlantı başarılıysa True, aksi halde simülasyon olarak True döner.
        """
        self.logger.info(f"Scanning for device on port: {self.port if self.port else 'AUTO'}")
        
        if HAS_MESHTASTIC:
            try:
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
                self.connected = True
                
                # Get local node info safely
                node_info = self.interface.getMyNodeInfo()
                long_name = node_info.get('user', {}).get('longName', 'UNKNOWN')
                
                self.logger.info(f"CONNECTION ESTABLISHED | Node: {long_name}")
                
                # Olay dinleyicilerini (receivers) kaydet
                pub.subscribe(self._on_receive, "meshtastic.receive")
                
                return True
            except Exception as e:
                self.logger.error(f"Hardware initialization failed: {str(e)}")
                self.logger.info("CRITICAL: Falling back to SIMULATION mode to maintain service continuity.")
                self.connected = False
                return True # Test ve simülasyon için devam et
        else:
            # Otomatik Simülasyon Akışı
            time.sleep(1)
            self.connected = True
            self.logger.info("SIMULATION MODE ACTIVE | Node: TALON-VIRTUAL")
            return True

    def _on_receive(self, packet, interface):
        """
        Mesh ağından gelen yeni bir paket algılandığında tetiklenen callback fonksiyonu.

        Args:
            packet (dict): Alınan paketin ham verisi.
            interface (SerialInterface): Verinin geldiği arayüz nesnesi.
        """
        try:
            if 'decoded' in packet and 'text' in packet['decoded']:
                text = packet['decoded']['text']
                sender = packet.get('fromId', 'UNKNOWN')
                snr = packet.get('snr', 0)
                self.logger.info(f"INCOMING [ID:{sender}] [SNR:{snr}]: {text}")
        except Exception as e:
            self.logger.error(f"Failed to parse incoming packet: {e}")

    def send_broadcast(self, message):
        """
        Tüm ağa (RF üzerinden) şifreli bir yayın mesajı gönderir.

        Args:
            message (str): Gönderilecek metin içeriği.

        Returns:
            bool: Gönderim işlemi başlatıldıysa True.
        """
        if not message:
            return False

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"

        try:
            if self.connected and self.interface:
                self.interface.sendText(formatted_msg)
                self.logger.info(f"TRANSMITTING RF >> {formatted_msg}")
                return True
            elif self.connected: 
                # Simülasyon gönderimi
                self.logger.info(f"[SIM-RF] BROADCAST >> {formatted_msg}")
                return True
            else:
                self.logger.error("TRANSMISSION FAILED: Interface not connected.")
                return False
        except Exception as e:
            self.logger.error(f"RF Transmission Error: {e}")
            return False

    def get_peers(self):
        """
        Ağdaki keşfedilmiş tüm düğümlerin (peers) listesini ve güncel durumlarını döner.

        Returns:
            list: Düğüm bilgilerini içeren sözlük listesi (ID, İsim, Batarya, SNR).
        """
        if self.connected and self.interface and self.interface.nodes:
            nodes = []
            for node_id, node_info in self.interface.nodes.items():
                user = node_info.get('user', {})
                metrics = node_info.get('deviceMetrics', {})
                
                nodes.append({
                    "id": node_id,
                    "name": user.get('longName', user.get('shortName', 'UNKNOWN')),
                    "battery": metrics.get('batteryLevel', 0),
                    "snr": node_info.get('snr', 0)
                })
            return nodes
        else:
            # Gelişmiş simülasyon verisi
            return [
                {"id": "!a1b2c3d4", "name": "VIRTUAL-NODE-01", "battery": 92, "snr": 12.5},
                {"id": "!e5f6g7h8", "name": "VIRTUAL-NODE-02", "battery": 65, "snr": 8.0}
            ]

if __name__ == "__main__":
    mesh = MeshInterface()
    if mesh.connect():
        mesh.send_broadcast("CQ CQ CQ - This is Command Post testing RF link.")
        time.sleep(2)
        print("Known Peers:", mesh.get_peers())
        if mesh.interface:
            mesh.interface.close()
