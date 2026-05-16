# Modül 5: Nörobiyoloji ve Biyomedikal Sinyal İşleme

Sinir sisteminin elektriksel dinamikleri ve bu sinyallerin matematiksel yöntemlerle analiz edilmesi.

## ?? Öğrenme Hedefleri
* Nöronların elektriksel davranışlarını Hodgkin-Huxley ve basitleştirilmiş modellerle analiz etmek.
* EEG, EMG ve ECG sinyallerini toplamak için gerekli enstrümantasyon bilgisini edinmek.
* Gürültülü biyolojik sinyalleri temizlemek ve öznitelik çıkarımı (feature extraction) yapmak.

## ?? Temel Konular

### 1. Hesaplamalı Nörobilim Temelleri
* **Membran Potansiyeli:** Nernst ve Goldman-Hodgkin-Katz denklemleri.
* **Aksiyon Potansiyeli:** Hodgkin-Huxley modeli, iyon kanalları (Na+, K+) kinetiği ve FitzHugh-Nagumo basitleştirmesi.
* **Sinaptik İletim:** Kimyasal ve elektriksel sinapslar, nörotransmitter dinamikleri.

### 2. Sinyal Edinimi ve Ön İşleme
* **Sinyal Kaynakları:** EEG (Beyin), EMG (Kas), ECG (Kalp) ve EOG (Göz hareketleri).
* **Donanım Sınırlamaları:** Örnekleme hızı (Nyquist kriteri), ADC çözünürlüğü ve ortak mod reddetme oranı (CMRR).
* **Artefakt Temizleme:** Çentik filtre (50/60 Hz), bant geçiren filtreler ve Bağımsız Bileşen Analizi (ICA) ile göz kırpma/kas gürültüsü giderme.

### 3. Zaman ve Frekans Domeni Analizi
* **Spektral Analiz:** FFT (Hızlı Fourier Dönüşümü), PSD (Güç Spektral Yoğunluğu) ve beyin ritimleri (Delta, Theta, Alpha, Beta, Gamma).
* **Zaman-Frekans Analizi:** STFT (Kısa Zamanlı Fourier Dönüşümü) ve Sürekli/Ayrık Dalgacık Dönüşümü (Wavelet Transform).
* **Bağlantısallık (Connectivity):** Koherans, Faz Kilitleme Değeri (PLV) ve Granger Nedenselliği.

## ?? Yazılım ve Boru Hattı (Pipeline)
* **MNE-Python:** EEG/MEG verileri için kapsamlı analiz kütüphanesi.
* **EEGLAB:** MATLAB tabanlı görsel sinyal işleme aracı.
* **SciPy.signal:** Filtre tasarımı ve spektral analiz fonksiyonları.

## ?? Önerilen Kaynaklar
* *Theoretical Neuroscience* - Peter Dayan, L.F. Abbott.
* *Biomedical Signal Processing* - Metin Akay.
* *Analyzing Neural Time Series Data* - Mike X Cohen.

---
> [!IMPORTANT]
> **Modül Projesi:** `laboratuvar-projeleri/eeg-processing-core/` klasöründe, ham EEG verisini temizleyen ve alfa ritmini çıkaran bir Python boru hattı bulunmaktadır.
