import numpy as np
from .settings import fft_size, max_frequency, min_frequency, sample_rate

def calculate_fft(audio_buffer):
    # windowing to improve fft spectrum
    window = np.hanning(len(audio_buffer))
    audio_windowed = audio_buffer * window
    # fft with zero padding
    spectrum = np.fft.rfft(
        audio_windowed,
        n=fft_size
    )
    # calculate and normalize magnitude of the spectrum
    magnitude = np.abs(spectrum)
    max_magnitude = np.max(magnitude)

    if max_magnitude > 0:
        magnitude = magnitude / max_magnitude

    # calculate freqeuncies of the fft bins
    frequencies = np.fft.rfftfreq(fft_size, 1/sample_rate)

    return magnitude, frequencies

def calculate_hps(magnitude, factor):
    hps = magnitude.copy()

    for factors in range(2, factor + 1):
        magnitude_compressed = magnitude[::factors]
        hps[:len(magnitude_compressed)] *= magnitude_compressed
    return hps
# interpolate the peaks to improve accuracy
def interpolate_peak(peak_index, magnitude_filtered, frequencies_filtered):
        if peak_index == 0 or peak_index == len(magnitude_filtered) - 1:
            return frequencies_filtered[peak_index]
        else:
            left = magnitude_filtered[peak_index - 1]
            center = magnitude_filtered[peak_index]
            right = magnitude_filtered[peak_index + 1]
            center_frequency = frequencies_filtered[peak_index]
            delta = 0.5 * (left - right)/(left - 2 * center + right)

            # frequency_resolution = sample_rate / fft_size
            frequency_resolution = (
                frequencies_filtered[1] - frequencies_filtered[0]
            )
            return center_frequency + delta * frequency_resolution


def find_peak(hps, frequencies):
    # Only look at guitar range
    mask = (frequencies >= min_frequency) & (frequencies <= max_frequency)
    frequencies_filtered = frequencies[mask]
    hps_filtered = hps[mask]
    # Find peak
    return np.argmax(hps_filtered), hps_filtered, frequencies_filtered

def calculate_db(audio_buffer):
    rms = np.sqrt(np.mean(audio_buffer ** 2))
    db = 20 * np.log10(max(rms, 1e-10))
    return db
