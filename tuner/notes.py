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
