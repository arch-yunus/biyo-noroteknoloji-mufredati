import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

class EEGProcessor:
    def __init__(self, sfreq):
        self.sfreq = sfreq

    def apply_bandpass_filter(self, data, lowcut, highcut, order=4):
        """Applies a Butterworth bandpass filter."""
        nyq = 0.5 * self.sfreq
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')
        filtered_data = signal.filtfilt(b, a, data)
        return filtered_data

    def apply_notch_filter(self, data, freq=50.0, q=30.0):
        """Applies a notch filter to remove line noise."""
        nyq = 0.5 * self.sfreq
        w0 = freq / nyq
        b, a = signal.iirnotch(w0, q)
        filtered_data = signal.filtfilt(b, a, data)
        return filtered_data

    def extract_alpha_rhythm(self, data):
        """Extracts Alpha rhythm (8-13 Hz)."""
        return self.apply_bandpass_filter(data, 8.0, 13.0)

    def calculate_psd(self, data):
        """Calculates Power Spectral Density using Welch's method."""
        f, psd = signal.welch(data, self.sfreq, nperseg=1024)
        return f, psd

# Mock Usage
if __name__ == "__main__":
    fs = 250  # 250 Hz sampling rate
    t = np.arange(0, 10, 1/fs)
    
    # Generate mock EEG: 10Hz Alpha + 50Hz Noise
    alpha_wave = 1.0 * np.sin(2 * np.pi * 10 * t)
    noise_50hz = 0.5 * np.sin(2 * np.pi * 50 * t)
    white_noise = 0.2 * np.random.randn(len(t))
    raw_eeg = alpha_wave + noise_50hz + white_noise

    processor = EEGProcessor(fs)
    
    # 1. Notch Filter
    clean_step1 = processor.apply_notch_filter(raw_eeg, 50.0)
    
    # 2. Extract Alpha
    alpha_only = processor.extract_alpha_rhythm(clean_step1)
    
    # 3. PSD Analysis
    freqs, psd = processor.calculate_psd(clean_step1)

    print("EEG Processing Complete.")
    print(f"Alpha Wave peak expected at 10Hz. Max PSD at: {freqs[np.argmax(psd)]:.2f} Hz")
