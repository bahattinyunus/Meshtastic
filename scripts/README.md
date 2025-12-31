# 🛠️ Yardımcı Araçlar (Utility Scripts)

Bu dizin, Meshtastic ağını yönetmek, test etmek ve izlemek için kullanılan Python tabanlı yardımcı araçları içerir. Tüm araçlar `core/mesh_interface.py` katmanını kullanır.

---

## 📡 1. Beacon Gönderici (`beacon_sender.py`)

Ağdaki diğer düğümlere belirli aralıklarla "Hayattayım" (Heartbeat) mesajı gönderir. Menzi testi yapmak için idealdir.

### Kullanım:
```bash
python scripts/beacon_sender.py --interval 30 --msg "REPEATER-01 ACTIVE" --port COM5
```

### Parametreler:
- `--interval`: Mesaj gönderim aralığı (Saniye).
- `--msg`: Yayınlanacak mesaj içeriği.
- `--port`: Cihazın bağlı olduğu seri port.

---

## 🔍 2. Ağ Tarayıcı (`scan_nodes.py`)

Mesh ağındaki aktif düğümleri tespit eder ve batarya, sinyal kalitesi (SNR) gibi verileri raporlar.

### Kullanım:
```bash
# Tek seferlik tarama
python scripts/scan_nodes.py --port COM3

# Sürekli izleme modu
python scripts/scan_nodes.py --loop --wait 10
```

### Parametreler:
- `--port`: Cihazın bağlı olduğu seri port.
- `--wait`: Düğüm bilgilerinin toplanması için beklenecek süre.
- `--loop`: Bu bayrak eklendiğinde tarama sürekli tekrarlanır.

---

## 🛠️ Geliştirme Notları

Yeni bir araç eklemek isterseniz, `core.mesh_interface.MeshInterface` sınıfını miras alarak veya doğrudan kullanarak donanım bağımlılığını minimize edebilirsiniz. Sistem, donanım yoksa otomatik olarak simülasyon verisi üretecektir.

---

> *Operasyonel Veritabanı ve İzleme Araçları.*
