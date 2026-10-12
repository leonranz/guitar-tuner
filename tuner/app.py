
from queue import Queue
import tkinter as tk

import numpy as np

from .settings import (
    hps_factors,
    buffer_size,
    max_frequency,
    min_frequency,
    fft_search_width,
)
from .audio import create_stream
from .audio_signal import (
    calculate_db,
    calculate_fft,
    calculate_hps,
    interpolate_peak,
    find_peak,
)
from .notes import (
    find_best_note,
    note_frequency,
    midi_to_note,
    cents_difference,
)
from .gui import TunerGUI


audio_buffer = np.zeros(buffer_size)
result_queue = Queue()


def callback(indata, frames, time, status):
    global audio_buffer

    # Update the rolling audio buffer
    audio = indata[:, 0]
    audio_buffer = np.concatenate((audio_buffer, audio))
    audio_buffer = audio_buffer[-buffer_size:]

    # 1. Calculate the original FFT
    magnitude, frequencies = calculate_fft(audio_buffer)

    # 2. Calculate HPS and find its strongest peak
    hps = calculate_hps(magnitude, hps_factors)

    hps_peak_index, hps_filtered, hps_frequencies = find_peak(
        hps, frequencies
    )

    hps_candidate_frequency = hps_frequencies[hps_peak_index]

    # 3. Find the corresponding bin in the original FFT
    candidate_index = np.argmin(
        np.abs(frequencies - hps_candidate_frequency)
    )

    # 4. Search the original FFT around the HPS candidate
    search_start = max(0, candidate_index - fft_search_width)
    search_end = min(
        len(magnitude),
        candidate_index + fft_search_width + 1,
    )

    local_magnitude = magnitude[search_start:search_end]
    local_frequencies = frequencies[search_start:search_end]

    # Find the strongest original FFT peak in this local range
    local_peak_index = np.argmax(local_magnitude)
    fft_peak_index = search_start + local_peak_index

    # 5. Interpolate around the local FFT peak
    peak_frequency = interpolate_peak(
        local_peak_index,
        local_magnitude,
        local_frequencies,
    )

    # Convert the frequency into a note and cents deviation
    best_note = find_best_note(peak_frequency)
    note = midi_to_note(best_note)
    cents = cents_difference(
        peak_frequency,
        note_frequency(best_note),
    )

    # Calculate input level and peak magnitude for the GUI
    db = calculate_db(audio_buffer)
    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-10))
    peak_magnitude_db = magnitude_db[fft_peak_index]

    # Only send results close to a note to the GUI
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
