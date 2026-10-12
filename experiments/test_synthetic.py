
import numpy as np

from tuner.settings import sample_rate, buffer_size
from tuner.audio_signal import (
    calculate_fft,
    calculate_hps,
    find_peak,
    interpolate_peak,
)

# Generate a synthetic E2 tone
expected_frequency = 82.4069

t = np.arange(buffer_size) / sample_rate
audio_buffer = np.sin(2 * np.pi * expected_frequency * t)

# 1. Calculate the original FFT
magnitude, frequencies = calculate_fft(audio_buffer)

# Find the strongest original FFT peak between 75 and 90 Hz
mask = (frequencies >= 75) & (frequencies <= 90)
diagnostic_frequencies = frequencies[mask]
diagnostic_magnitude = magnitude[mask]

original_index = np.argmax(diagnostic_magnitude)
original_frequency = diagnostic_frequencies[original_index]

print(f"Expected frequency:  {expected_frequency:.4f} Hz")
print(f"Original FFT peak:   {original_frequency:.3f} Hz")
original_peak_index, original_magnitude, original_frequencies = find_peak(
    magnitude, frequencies
)

original_estimate = interpolate_peak(
    original_peak_index,
    original_magnitude,
    original_frequencies,
)

print(f"Interpolated FFT:    {original_estimate:.3f} Hz")
# 2. Calculate the harmonic product spectrum
hps = calculate_hps(magnitude, 2)
# Inspect HPS values around the expected E2 frequency
mask = (frequencies >= 75) & (frequencies <= 90)

for frequency, value in zip(frequencies[mask], hps[mask]):
    print(f"{frequency:8.3f} Hz  HPS: {value:.8e}")
# Find the strongest HPS peak
hps_index, hps_filtered, hps_frequencies = find_peak(
    hps, frequencies
)

print(f"Raw HPS peak:        {hps_frequencies[hps_index]:.3f} Hz")

# 3. Interpolate the HPS peak
estimated_frequency = interpolate_peak(
    hps_index,
    hps_filtered,
    hps_frequencies,
)
# Refine the frequency using the original FFT spectrum
estimated_frequency = original_estimate

print(f"Estimated frequency: {estimated_frequency:.3f} Hz")
print(f"Estimated frequency: {estimated_frequency:.3f} Hz")
