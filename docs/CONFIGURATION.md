# ⚙️ Konfigürasyon Derin Bakış (Advanced Configuration)

Bu döküman, Meshtastic cihazlarınızın ve bu yazılımın performansını optimize etmek için gereken kritik parametreleri detaylandırır.

---

## 📡 1. LoRa Parametreleri ve Performans Etkisi

Meshtastic ağında menzil ve bant genişliği arasındaki dengeyi şu ayarlar belirler:

### Modem Presets (Önayarlar)
- **`LONG_FAST` (Varsayılan):** En iyi menzil/hız dengesi. %90 senaryolar için idealdir.
- **`LONG_SLOW`:** Maksimum menzil, ancak çok düşük hız. Sadece kritik mesajlar için.
- **`SHORT_FAST`:** Yüksek hız, kısa mesafe. Bina içi kullanımlar için.

### Kritik Değişkenler
- **Spreading Factor (SF):** Artarsa menzil artar, veri hızı düşer.
- **Coding Rate (CR):** Hata düzeltme oranı. Sinyal kirliliğinde artırılmalıdır.
- **Bandwidth (BW):** Genişlik artarsa hız artar, ancak hassasiyet (sensitivity) düşer.

---

## 🔐 2. Kanal Güvenliği (Encryption)

Ağınızın güvenliği için `psk` (Pre-Shared Key) yönetimi hayati önem taşır.

- **Primary Channel:** Tüm düğümler aynı PSK'ya sahip olmalıdır.
- **AES-256:** Meshtastic varsayılan olarak bu şifrelemeyi kullanır.
- **Base64 Key:** Kendi anahtarınızı üretmek için:
  ```bash
  meshtastic --set-channel-name "PRIVATE" --set-channel-psk "random_secure_key"
  ```

---

## 📲 3. Telemetri ve Güç Ayarları

Pilinizi optimize etmek için:
- **`position_broadcast_secs`:** Konum paylaşım sıklığı. Standart kullanıcılar için 900-1800 sn (15-30 dk) önerilir.
- **`device_metrics_interval`:** Pil ve voltaj bilgisinin gönderilme sıklığı.

---

## 🛠️ 4. Yazılım Tarafı (`example_config.yaml`)

Depodaki `configs/example_config.yaml` dosyası şu yapıyı takip eder:

```yaml
lora:
  hop_limit: 3 # Bir paketin ağda en fazla kaç kez "sekebileceği"
  tx_power: 30 # Sinyal çıkış gücü (30 dBm = 1 Watt)
```

> [!WARNING]
> `hop_limit` değerini 7'den fazla yapmayın. Bu, ağda "broadcast storm" (paket fırtınası) oluşmasına ve iletişimin kilitlenmesine neden olabilir.

---

> [!TIP]
> **Pro Tip:** Ağınızdaki düğüm sayısı 30'u geçerse, `hop_limit` değerini 2'ye düşürerek ağ kalabalığını azaltabilirsiniz.
