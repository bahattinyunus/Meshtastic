# 📟 Donanım Rehberi (Hardware Selection & Theory)

Meshtastic ağınızın performansı, seçtiğiniz donanım ve anten kombinasyonuna doğrudan bağlıdır.

---

## 🎯 1. Popüler Cihaz Karşılaştırması

| Cihaz | Güç Tüketimi | Özellikler | En İyi Kullanım |
| :--- | :--- | :--- | :--- |
| **LILYGO T-Beam** | Orta | GPS, Ekran opsiyonel, 18650 Pil yuvası. | Saha birimleri, takip sistemleri. |
| **LILYGO T-Echo** | Çok Düşük | E-Ink ekran, NRF52 işlemci, şık kasa. | Günlük taşıma (EDC), uzun pil ömrü. |
| **RAK4631 (WizBlock)** | Minimal | Modüler yapı, IP67 kasa seçeneği. | Güneş enerjili uzak mesafe röleleri. |
| **Heltec V3** | Yüksek | Wi-Fi/BT, OLED ekran. | Ev/Ofis baz istasyonları. |

---

## 📡 2. Anten Teorisi

Anten, Meshtastic cihazının "sesidir". 

- **Omni-Directional (Çok Yönlü):** Sinyali her yöne eşit dağıtır. Saha operasyonları için idealdir. (3-5 dBi önerilir).
- **Directional (Yönlü/Yagi):** Sinyali belirli bir yöne odaklar. Çok uzak mesafedeki (noktadan noktaya) düğümler için kullanılır.
- **Dipol Antenler:** En temel anten tipidir, genellikle cihazlarla birlikte gelir ancak kapsama alanı sınırlıdır.

> [!CAUTION]
> **SWR Uyarısı:** Anteniniz seçtiğiniz frekans (868 MHz) ile uyumlu olmalıdır. Uygun olmayan antenler cihaza zarar verebilir veya mesafeyi ciddi oranda düşürür.

---

## 🔋 3. Güç Yönetimi ve Solar Sistemi

Uzak mesafe rölesi (Repeater) kurarken dikkate alınması gerekenler:
1. **Güneş Paneli:** En az 5V 10W panel önerilir.
2. **Şarj Kontrolcü:** TP4056 veya RAK'ın solar girişleri.
3. **Batarya:** Li-ion veya soğuk iklimler için LiFePO4.

---

## 🗺️ 4. Türkiye Uygulamaları

Türkiye'de Meshtastic topluluğu genellikle **EU868** bandını kullanır.
- **Optimal Frekans:** 868.0 MHz
- **Kanal Ayarı:** `LongFast` modu en güvenilir menzili sağlar.

---

> *Teknoloji ile Taktiksel Fark Yaratın.*
