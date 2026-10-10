from queue import Queue

import numpy as np
import sounddevice as sd
from settings import hps_factors
from audio import create_stream
from audio_signal import calculate_fft, calculate_hps, interpolate_peak, find_peak
from notes import find_best_note, note_frequency, midi_to_note, cents_difference

buffer_size = 16384
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

    peak_index, frequencies_filtered = find_peak(hps, frequencies)

    peak_frequency = interpolate_peak(
        peak_index,
        hps,
        frequencies_filtered
    )
    best_note = find_best_note(peak_frequency)
    note = midi_to_note(best_note)
    cents = cents_difference(peak_frequency, note_frequency(best_note))

    result = (note, peak_frequency, cents)
    result_queue.put(result)
stream = create_stream(callback)

with stream:
    input("press enter to stop")
