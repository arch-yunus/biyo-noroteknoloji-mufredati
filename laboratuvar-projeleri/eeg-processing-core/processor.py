import sys
import numpy as np
import scipy.signal as signal

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class EEGProcessor:
    """
    Advanced Biomedical Signal Processing Core for Electroencephalography (EEG).
    Implements digital filter design, power spectral density estimation, and band extraction.
    """
    def __init__(self, sfreq):
        """
        Initializes the processor with a specific sampling frequency.
        :param sfreq: Sampling frequency in Hz.
        """
        self.sfreq = sfreq

    def apply_bandpass_filter(self, data, lowcut, highcut, order=4):
        """
        Applies a zero-phase Butterworth bandpass filter.
        :param data: Input 1D signal or 2D array (channels x samples).
        :param lowcut: Lower cutoff frequency (Hz).
        :param highcut: Upper cutoff frequency (Hz).
        :param order: Filter order.
        """
        nyq = 0.5 * self.sfreq
        low = lowcut / nyq
        high = highcut / nyq
        
        # Ensure values are within Nyquist limit
        low = max(0.001, min(low, 0.999))
        high = max(0.001, min(high, 0.999))
        
        b, a = signal.butter(order, [low, high], btype='band')
        
        # Check if data is multi-channel or single channel
        if len(data.shape) > 1:
            return np.array([signal.filtfilt(b, a, ch) for ch in data])
        return signal.filtfilt(b, a, data)

    def apply_notch_filter(self, data, notch_freq=50.0, q=30.0):
        """
        Applies a zero-phase IIR notch filter to remove narrow-band line noise.
        :param data: Input 1D or 2D array.
        :param notch_freq: Powerline noise frequency (typically 50.0 Hz or 60.0 Hz).
        :param q: Quality factor (controls bandwidth).
        """
        nyq = 0.5 * self.sfreq
        w0 = notch_freq / nyq
        b, a = signal.iirnotch(w0, q)
        
        if len(data.shape) > 1:
            return np.array([signal.filtfilt(b, a, ch) for ch in data])
        return signal.filtfilt(b, a, data)

    def calculate_psd(self, data, nperseg=None):
        """
        Calculates the Power Spectral Density (PSD) using Welch's method.
        :param data: 1D signal array.
        :param nperseg: Length of each segment. Default is 4 * sfreq (approx. 4 sec window).
        :return: Frequencies, PSD values.
        """
        if nperseg is None:
            nperseg = min(len(data), int(4 * self.sfreq))
        f, psd = signal.welch(data, self.sfreq, nperseg=nperseg)
        return f, psd

    def extract_band_powers(self, data):
        """
        Extracts absolute and relative powers for standard physiological EEG bands:
        - Delta (0.5 - 4 Hz)
        - Theta (4 - 8 Hz)
        - Alpha (8 - 13 Hz)
        - Beta (13 - 30 Hz)
        - Gamma (30 - 45 Hz)
        """
        freqs, psd = self.calculate_psd(data)
        
        bands = {
            'Delta': (0.5, 4.0),
            'Theta': (4.0, 8.0),
            'Alpha': (8.0, 13.0),
            'Beta': (13.0, 30.0),
            'Gamma': (30.0, 45.0)
        }
        
        abs_powers = {}
        for band_name, (low, high) in bands.items():
            # Find indices corresponding to the frequency range
            idx_band = np.logical_and(freqs >= low, freqs <= high)
            # Integrate the PSD over the range using trapezoidal rule
            trapz_func = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
            band_power = trapz_func(psd[idx_band], freqs[idx_band])
            abs_powers[band_name] = band_power
            
        total_power = sum(abs_powers.values())
        
        relative_powers = {}
        for band_name, abs_pow in abs_powers.items():
            relative_powers[band_name] = (abs_pow / total_power) if total_power > 0 else 0
            
        return abs_powers, relative_powers

def simulate_raw_eeg(duration=10.0, sfreq=250.0):
    """
    Simulates a highly realistic multi-channel raw EEG dataset with:
    - 6 channels representing different brain regions (F3, F4, C3, C4, O1, O2).
    - Alpha rhythm (10 Hz) dominant on occipital channels (O1, O2) representing eye closure.
    - Mu rhythm (11 Hz) and Beta rhythm (22 Hz) on motor cortex channels (C3, C4).
    - Heavy slow-wave eye blink artifacts (1.5 Hz delta spikes) on frontal channels (F3, F4).
    - 50 Hz powerline interference and high-frequency sensor noise on all channels.
    """
    n_samples = int(duration * sfreq)
    t = np.arange(0, duration, 1/sfreq)
    channels = ['F3', 'F4', 'C3', 'C4', 'O1', 'O2']
    data = np.zeros((len(channels), n_samples))
    
    # Common background brain activity (pink noise approximation)
    background = np.convolve(np.random.randn(n_samples), np.ones(10)/10, mode='same') * 0.5
    
    # Powerline interference (50 Hz)
    powerline = 0.8 * np.sin(2 * np.pi * 50 * t)
    
    # Add noise & background to all channels
    for ch_idx in range(len(channels)):
        data[ch_idx] = background + powerline + 0.15 * np.random.randn(n_samples)
        
    # Frontal channels: Add high-amplitude eye blinks (delta spikes at 1.5 Hz)
    blinks = np.zeros(n_samples)
    blink_times = [1.5, 4.0, 7.2]  # Blink event seconds
    for bt in blink_times:
        blink_idx = int(bt * sfreq)
        # Create a half-sine wave pulse for blink
        blink_width = int(0.3 * sfreq)
        pulse = signal.windows.hann(blink_width) * 5.0
        blinks[blink_idx : blink_idx + blink_width] += pulse
    
    data[0] += blinks        # F3
    data[1] += blinks * 0.9  # F4
    
    # Occipital channels: Add Alpha rhythm (10 Hz)
    alpha = 1.8 * np.sin(2 * np.pi * 10 * t)
    data[4] += alpha         # O1
    data[5] += alpha * 0.95  # O2
    
    # Motor channels: Add Mu (11 Hz) and Beta (20 Hz)
    mu = 1.0 * np.sin(2 * np.pi * 11 * t)
    beta = 0.6 * np.sin(2 * np.pi * 22 * t)
    data[2] += mu + beta     # C3
    data[3] += mu * 0.9 + beta * 0.8  # C4
    
    return data, channels, t

def execute_eeg_processing_pipeline():
    """Runs a complete test and verification suite of the EEG processing pipeline."""
    print("==================================================")
    print("⚡ BIOMEDICAL SIGNAL PROCESSING & FILTER PIPELINE")
    print("==================================================")
    
    # 1. Simulating Raw EEG Data
    sfreq = 250.0
    duration = 10.0
    print(f"\n[+] Simulating 6-channel EEG Signal (Sampling Rate: {sfreq} Hz, Duration: {duration}s)")
    raw_data, channels, t = simulate_raw_eeg(duration, sfreq)
    
    # 2. Applying Filters
    processor = EEGProcessor(sfreq)
    print("\n[+] Applying Multi-Stage Digital Filtering:")
    print("    - Notch Filter (50 Hz) for Powerline Interference...")
    notch_filtered = processor.apply_notch_filter(raw_data, notch_freq=50.0)
    
    print("    - Bandpass Filter (0.5 - 45 Hz) for Physiological Signals...")
    clean_data = processor.apply_bandpass_filter(notch_filtered, lowcut=0.5, highcut=45.0)
    
    # 3. Validation on Occipital Channel O1 (Channel 4)
    print("\n[+] Performing Quantitative Power Band Analysis on Occipital (O1) Channel:")
    raw_o1 = raw_data[4]
    clean_o1 = clean_data[4]
    
    abs_raw, rel_raw = processor.extract_band_powers(raw_o1)
    abs_clean, rel_clean = processor.extract_band_powers(clean_o1)
    
    print("\n    --> Spectral Band Relative Power Distribution:")
    print("        Band       | Raw EEG Relative | Clean EEG Relative | Status")
    print("        -------------------------------------------------------------")
    for band in abs_raw.keys():
        status = "Active" if band == "Alpha" else "Attenuated"
        print(f"        {band:<10} | {rel_raw[band]*100:>15.1f}% | {rel_clean[band]*100:>17.1f}% | {status}")
        
    # Calculate attenuation of 50 Hz powerline noise
    freqs_raw, psd_raw = processor.calculate_psd(raw_o1)
    freqs_clean, psd_clean = processor.calculate_psd(clean_o1)
    
    idx_50hz = np.argmin(np.abs(freqs_raw - 50.0))
    psd_50_raw = psd_raw[idx_50hz]
    psd_50_clean = psd_clean[idx_50hz]
    attenuation_db = 10 * np.log10(psd_50_raw / psd_50_clean)
    
    print(f"\n    --> 50Hz Powerline Interference Attenuation: {attenuation_db:.2f} dB")
    print("==================================================\n")

if __name__ == "__main__":
    execute_eeg_processing_pipeline()
