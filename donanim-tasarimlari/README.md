# Donanım Tasarımları ve Enstrümantasyon

Bu klasör, biyolojik sinyallerin toplanması için gerekli olan analog ve dijital donanım projelerini içerir.

## ?? Mevcut Projeler

### 1. [EMG Amplifikatör (KiCAD)](./emg-amplifier-kicad/)
* **Açıklama:** Kas sinyallerini toplamak için tasarlanmış tek kanallı enstrümantasyon amplifikatörü.
* **Bileşenler:** INA128 (InAmp), OPA2134 (Filtreler), Sağ Bacak Sürücüsü devresi.

### 2. [EEG Shield](./eeg-shield/)
* **Açıklama:** Arduino/ESP32 uyumlu, 8 kanallı EEG toplama kartı.
* **Ana Entegre:** ADS1299 (24-bit ADC).

## ?? Tasarım İlkeleri
* **Düşük Gürültü:** Analog sinyal yollarının dijital hatlardan izole edilmesi.
* **Güvenlik:** Kullanıcı izolasyonu için optik izolatörler veya batarya ile besleme.
* **Modülerlik:** Farklı mikrodenetleyicilerle SPI üzerinden kolay entegrasyon.

---
> [!WARNING]
> Bu donanımlar eğitim amaçlıdır. İnsan üzerinde test yapmadan önce mutlaka tıbbi güvenlik standartlarına (IEC 60601) uygunluğunu kontrol edin.
