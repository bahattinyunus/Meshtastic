# 🛠️ Kurulum Rehberi (Installation Guide)

Bu rehber, Meshtastic donanımınızı ve yazılım geliştirme ortamınızı nasıl hazırlayacağınızı adım adım açıklar.

---

## 🔌 1. Donanım Hazırlığı ve Yazılım Yükleme (Flashing)

Cihazınıza en güncel firmware'i yüklemek için iki ana yöntem vardır:

### A. Web Flasher (En Kolay Yöntem)
1. Cihazınızı USB ile bilgisayara bağlayın.
2. [flasher.meshtastic.org](https://flasher.meshtastic.org/) adresine gidin.
3. Cihaz tipinizi seçin (örn: LILYGO T-Beam).
4. "Flash" butonuna basın ve işlemin tamamlanmasını bekleyin.

### B. CLI Üzerinden Flashing
Python yüklü ise terminalden şu komutla yükleme yapabilirsiniz:
```bash
meshtastic --flash <firmware_dosyasi>.bin
```

---

## 💻 2. Yazılım Geliştirme Ortamı

Bu depodaki scriptleri ve `MeshInterface` katmanını kullanmak için Python 3.8+ gereklidir.

### Adım 1: Depoyu Klonlayın
```bash
git clone https://github.com/bahattinyunus/Meshtastic.git
cd Meshtastic
```

### Adım 2: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

> [!IMPORTANT]
> Windows kullanıcıları için Serial port erişim izni gerekebilir. Cihazınız listede görünmüyorsa "CP210X" veya "CH340" sürücülerini kurduğunuzdan emin olun.

---

## ⚙️ 3. İlk Konfigürasyon

Cihazınız bağlandıktan sonra isimlendirme ve bölge ayarı yapılması kritiktir:

```bash
# Bölgeyi Türkiye (EU868) olarak ayarla
meshtastic --set region EU868

# Cihaz ismini tanımla
meshtastic --set-owner "OPERATOR-01" --set-owner-short "OP01"
```

---

## 📡 4. Bağlantı Testi

Kurulumun başarılı olduğunu doğrulamak için:
```bash
python scripts/scan_nodes.py
```
Eğer cihazınız bağlıysa ve sistem doğru çalışıyorsa, aktif düğümlerin listesini terminalde göreceksiniz.

---

> [!NOTE]
> Daha fazla detay için `docs/CONFIGURATION.md` dökümanına göz atın.
