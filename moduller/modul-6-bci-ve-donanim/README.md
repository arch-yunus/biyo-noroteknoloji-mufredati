# Modül 6: Beyin-Bilgisayar Arayüzleri (BCI) ve Donanım Enstrümantasyonu

Biyolojik sinyallerin fiziksel dünyadan dijital dünyaya aktarılmasını sağlayan donanım katmanı ve BCI sistemlerinin çalışma prensipleri.

## ?? Öğrenme Hedefleri
* Biyopotansiyel yükselteç (InAmp) ve aktif filtre devreleri tasarlamak.
* Mikrodenetleyiciler (STM32, ESP32) ile yüksek hızda veri toplama sistemleri geliştirmek.
* P300 ve SSVEP gibi temel BCI paradigmalarını anlamak ve uygulamak.

## ?? Temel Konular

### 1. Analog Donanım Tasarımı (Frontend)
* **Enstrümantasyon Amplifikatörleri (InAmp):** Çok düşük genlikli (µV) beyin sinyallerini yükseltme ve yüksek CMRR sağlama.
* **Sağ Bacak Sürücüsü (Right Leg Drive - RLD):** Ortak mod gürültüsünü (şebeke gürültüsü) azaltmak için aktif geri besleme devresi.
* **Aktif Filtreler:** Butterworth ve Chebyshev tasarımları; anti-aliasing filtreleri.

### 2. Gömülü Sistemler ve Veri İletişimi
* **ADC (Analog-Dijital Dönüştürücü):** 24-bit çözünürlük (örn. ADS1299), örnekleme senkronizasyonu ve düşük gürültülü referans tasarımı.
* **Haberleşme Protokolleri:** SPI ve I2C üzerinden yüksek hızlı veri transferi; DMA (Direct Memory Access) kullanımı.
* **Gerçek Zamanlı Yazılım:** RTOS (FreeRTOS) kullanımı, kesme (interrupt) yönetimi ve buffer stratejileri.

### 3. BCI Paradigmaları ve Uygulama
* **P300 (Olayla İlişkili Potansiyeller):** "Oddball" paradigması ve dikkat tabanlı seçim sistemleri (BCI Speller).
* **SSVEP (Kararlı Durum Görsel Evoke Potansiyelleri):** Belirli frekanslarda yanıp sönen uyaranlara verilen tepkilerin analizi.
* **Motor İmgeleme (Motor Imagery):** Hareket hayal etme sırasında oluşan mu/beta ritimlerindeki değişimlerin (ERD/ERS) tespiti.

## ?? Geliştirme Araçları
* **KiCAD / Altium:** PCB tasarımı ve şema çizimi.
* **STM32 CubeIDE / ESP-IDF:** Gömülü yazılım geliştirme ortamları.
* **OpenBCI:** Açık kaynaklı BCI donanım ve yazılım platformu.

## ?? Önerilen Kaynaklar
* *Medical Instrumentation: Application and Design* - John G. Webster.
* *Brain-Computer Interfaces: Principles and Practice* - Wolpaw, Wolpaw.
* *Small Signal Audio Design* - Douglas Self (Analog tasarım temelleri için).

---
> [!NOTE]
> Bu modüldeki donanım tasarımları, `donanim-tasarimlari/` klasöründe yer alan projeler için temel oluşturur.
