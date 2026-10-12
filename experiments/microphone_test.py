import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np



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

t = np.arange(48000)/48000
test_signal = np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 220 * t)




device = 0
sample_rate = 48000
duration = 1
audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    device=device
)
sd.wait()
audio = audio[:, 0]
window = np.hanning(len(audio))
audio_windowed = audio * window
time = np.arange(len(audio)) / sample_rate
spectrum = np.fft.rfft(audio_windowed)
frequencies = np.fft.rfftfreq(len(audio),1/sample_rate)
mask = (frequencies >= 70) & (frequencies <= 400)
magnitude = np.abs(spectrum)

frequencies_filtered = frequencies[mask]
magnitude_filtered = magnitude[mask]

peak_index = np.argmax(magnitude_filtered)
peak_frequency = frequencies_filtered[peak_index]
# plt.plot(time,audio)
plt.plot(frequencies,magnitude)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.xlim(0, 400)
midi_notes = range(40, 65)
best_note = min(midi_notes, key=lambda n: abs(peak_frequency - note_frequency(n)))
print("cents difference:",cents_difference(peak_frequency, note_frequency(best_note)))
print("Peak:", peak_frequency)
print("MIDI:", best_note)
print("Frequency:", note_frequency(best_note))
print("Note:",midi_to_note(best_note))
plt.show()
