from queue import Queue
import tkinter as tk
import numpy as np
import sounddevice as sd
from .settings import fft_size, hps_factors, buffer_size, max_frequency, min_frequency
from .audio import create_stream
from .audio_signal import calculate_db, calculate_fft, calculate_hps, interpolate_peak, find_peak
from .notes import find_best_note, note_frequency, midi_to_note, cents_difference
from .gui import TunerGUI

audio_buffer = np.zeros(buffer_size)
result_queue = Queue()
# Callback function
def callback(indata, frames, time, status):
    global audio_buffer

    audio = indata[:, 0]
    audio_buffer = np.concatenate((audio_buffer, audio))
    audio_buffer = audio_buffer[-buffer_size:]

    magnitude, frequencies = calculate_fft(audio_buffer)

    hps = calculate_hps(magnitude,hps_factors)

    hps_peak_index, hps_filtered, hps_frequencies = find_peak(hps, frequencies)

    peak_frequency = interpolate_peak(
       hps_peak_index,
       hps_filtered,
       hps_frequencies
    )
    best_note = find_best_note(peak_frequency)
    note = midi_to_note(best_note)
    cents = cents_difference(peak_frequency, note_frequency(best_note))
    db = calculate_db(audio_buffer)

    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-10))
    fft_peak_index = np.argmin(np.abs(frequencies - peak_frequency))
    peak_magnitude_db = magnitude_db[fft_peak_index]

    # temporary
    mask = (frequencies >= 75) & (frequencies <= 90)

    frequencies_filtered = frequencies[mask]
    magnitude_filtered = magnitude[mask]

    original_peak_index = np.argmax(magnitude_filtered)
    original_peak_frequency = frequencies_filtered[original_peak_index]

    print(f"Original FFT peak: {original_peak_frequency:.3f} Hz")
    print(f"HPS estimate:      {peak_frequency:.3f} Hz")
    print(f"Raw HPS peak: {hps_frequencies[hps_peak_index]:.3f} Hz")
    # temporary
    if abs(cents) < 40:
        result = (
            note,
            peak_frequency,
            cents,
            db,
            frequencies,
            magnitude_db,
            peak_frequency,
            peak_magnitude_db,
        )
        result_queue.put(result)
stream = create_stream(callback)

with stream:
    root = tk.Tk()
    gui = TunerGUI(root, result_queue)
    root.mainloop()
