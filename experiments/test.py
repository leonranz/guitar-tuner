import numpy as np
import matplotlib.pyplot as plt

sample_rate = 48000
buffer_size = 16384
fft_size = 32768

def interpolate_peak(peak_index, magnitude_filtered, frequencies_filtered):
        if peak_index == 0 or peak_index == len(magnitude_filtered) - 1:
            return frequencies_filtered[peak_index]
        else:
            left = magnitude_filtered[peak_index - 1]
            center = magnitude_filtered[peak_index]
            right = magnitude_filtered[peak_index + 1]
            center_frequency = frequencies_filtered[peak_index]
            delta = 0.5 * (left - right)/(left - 2 * center + right)

            frequency_resolution = sample_rate / fft_size

            return center_frequency + delta * frequency_resolution



# Generate a 110 Hz test signal
t = np.arange(buffer_size) / sample_rate
audio_buffer = (
    np.sin(2 * np.pi * 110 * t)
    + 2 * np.sin(2 * np.pi * 220 * t)
)
# Apply window
window = np.hanning(len(audio_buffer))
audio_windowed = audio_buffer * window

# FFT
spectrum = np.fft.rfft(audio_windowed, n=fft_size)
magnitude = np.abs(spectrum)
magnitude = magnitude / np.max(magnitude)
# HPS
hps = magnitude.copy()

for factor in range(2,5):
    magnitude_compressed = magnitude[::factor]
    hps[:len(magnitude_compressed)] *= magnitude_compressed

# Frequencies
frequencies = np.fft.rfftfreq(fft_size, 1 / sample_rate)

# Only look at guitar range
mask = (frequencies >= 70) & (frequencies <= 400)

frequencies_filtered = frequencies[mask]
hps_filtered = hps[mask]
# Find peak
peak_index = np.argmax(hps_filtered)
interpolated_frequency = interpolate_peak(peak_index, hps_filtered, frequencies_filtered)
print("Peak index:", peak_index)
print("Raw frequency:", frequencies_filtered[peak_index])
print("interpolated:", interpolated_frequency)
