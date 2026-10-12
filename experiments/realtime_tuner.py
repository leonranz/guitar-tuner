import sounddevice as sd
import numpy as np

def find_best_note(peak_frequency):
    midi_notes = range(40, 65)
    return min(midi_notes, key=lambda n: abs(peak_frequency - note_frequency(n)))

def note_frequency(n):
    return 440 * 2 ** ((n - 69) / 12)

def cents_difference(measured, target):
    return 1200 * np.log2(measured/target)

def midi_to_note(midi_note):
    note_names = ["C", "C#", "D", "D#", "E", "F",
                      "F#", "G", "G#", "A", "A#", "B"]
    note = note_names[midi_note % 12]
    octave = midi_note // 12 - 1
    return f"{note}{octave}"
def interpolate_peak(peak_index, magnitude_filtered, frequencies_filtered):
        if peak_index == 0 or peak_index == len(magnitude_filtered) - 1:
            return magnitude_filtered[peak_index]
        else:
            left = magnitude_filtered[peak_index - 1]
            center = magnitude_filtered[peak_index]
            right = magnitude_filtered[peak_index + 1]
            center_frequency = frequencies_filtered[peak_index]
            delta = 0.5 * (left - right)/(left - 2 * center + right)

            frequency_resolution = sample_rate / fft_size

            return center_frequency + delta * frequency_resolution
def calculate_hps(magnitude,num_harmonics):

buffer_size = 16384
audio_buffer = np.zeros(buffer_size)
fft_size = 32768
sample_rate = 48000
block_size = 2048



# Generate a 110 Hz test signal
t = np.arange(buffer_size) / sample_rate
audio_buffer = np.sin(2 * np.pi * 110 * t)

def callback(indata, frames, time, status):
    global audio_buffer
    global buffer_size
    audio = indata[:, 0]
    audio_buffer = np.concatenate((audio_buffer, audio))
    audio_buffer = audio_buffer[-buffer_size:]
    window = np.hanning(len(audio_buffer))
    audio_windowed = audio_buffer * window
    spectrum = np.fft.rfft(audio_windowed, n=fft_size)
    magnitude = np.abs(spectrum)
    frequencies = np.fft.rfftfreq(fft_size, 1 / sample_rate)
    mask = (frequencies >= 70) & (frequencies <= 400)

    frequencies_filtered = frequencies[mask]
    magnitude_filtered = magnitude[mask]

    peak_index = np.argmax(magnitude_filtered)
    peak_frequency = interpolate_peak(
        peak_index,
        magnitude_filtered,
        frequencies_filtered
    )
    best_note = find_best_note(peak_frequency)
    print("Frequency:", peak_frequency)
    print("Note:",midi_to_note(best_note))
    print("cents:",cents_difference(peak_frequency, note_frequency(best_note)))
    print("Peak index:", peak_index)
    print("Peak magnitude:", magnitude_filtered[peak_index])
    print("Left:", magnitude_filtered[peak_index - 1])
    print("Right:", magnitude_filtered[peak_index + 1])


stream = sd.InputStream(
    samplerate=sample_rate,
    blocksize=block_size,
    channels=1,
    callback=callback
)

with stream:
    input("Press Enter to stop...\n")
