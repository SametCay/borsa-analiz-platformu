# MarketPulse - Borsa Analiz Platformu 📈

Bu proje, 30 günlük yazılım stajım kapsamında geliştirilmiş; Borsa İstanbul (BIST) verilerini ve haberlerini otomatik olarak çekerek görselleştiren, aynı zamanda portföy takibi yapabilen yerel bir web uygulamasıdır.

## 🚀 Özellikler
* **Otomatik Veri Çekme:** `yfinance` kütüphanesi ile BIST hisselerinin güncel fiyat, hacim ve teknik analiz verilerini indirir.
* **Haber Akışı:** Google News RSS üzerinden hisselerle ilgili son piyasa haberlerini anlık olarak listeler.
* **Portföy Yönetimi:** Alım-satım işlemlerini JSON formatında kaydeder, kar/zarar (P&L) durumunu gösterir ve ATR bazlı dinamik stop-loss seviyeleri hesaplar.
* **Görselleştirme:** Çekilen veriler `Chart.js` kullanılarak dinamik grafiklere dökülür ve piyasa ısı haritası oluşturulur.
* **Yapay Zeka Analizi:** Claude API entegrasyonu ile seçilen hisse üzerinde teknik ve temel verilere dayalı otomatik analist raporu üretir.

## 🛠️ Kullanılan Teknolojiler
* **Backend / Veri İşleme:** Python, yerel HTTP Sunucusu (`http.server`)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
* **Kütüphaneler:** yfinance, requests, Chart.js

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Projeyi bilgisayarınıza indirin (ZIP olarak veya klonlayarak).
2. Terminal veya Komut İstemcisi'ni (cmd) açarak proje klasörünün içine girin.
3. Gerekli Python kütüphanelerini kurun:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. Klasör içindeki **`GUNCELLE_VE_AC_2.bat`** dosyasına çift tıklayın.

Bu işlem sırasıyla; güncel piyasa verilerini çekecek, haberleri güncelleyecek, yerel sunucuyu başlatacak ve arayüzü tarayıcınızda otomatik olarak açacaktır.
