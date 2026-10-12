# Guitar Tuner

A real-time guitar tuner written in Python. It analyzes an audio signal to estimate its fundamental frequency, identifies the closest musical note, and displays the tuning deviation in cents.

## How It Works

1. **Audio Input:** Continuously captures audio and maintains a rolling buffer of recent samples.
2. **Fast Fourier Transform (FFT):** Converts the audio signal from the time domain to the frequency domain. A Hann window is applied to reduce spectral leakage.
3. **Harmonic Product Spectrum (HPS):** Combines the original spectrum with downsampled versions to help identify the fundamental frequency instead of a stronger harmonic.
4. **Frequency Refinement:** Searches the original FFT spectrum around the HPS candidate and uses parabolic interpolation to improve frequency accuracy.
5. **Note Detection:** Maps the estimated frequency to the nearest musical note and calculates the deviation from its target frequency in cents.
6. **Graphical Interface:** Displays the detected note, tuning deviation, and audio signal information in real time.

## Requirements

* Python 3.14 or compatible version
* NumPy
* SoundDevice
* Tkinter

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/leonranz/guitar-tuner
cd guitar-tuner
```

Create and activate a virtual environment:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install numpy sounddevice
```

Tkinter may need to be installed separately through your operating system's package manager.

## Running the Tuner

From the project root, run:

```bash
python -m tuner.app
```

## Project Structure

```text
guitar-tuner/
├── tuner/
│   ├── app.py
│   ├── gui.py
│   ├── audio.py
│   ├── audio_signal.py
│   ├── notes.py
│   └── settings.py
└── README.md
```

* `app.py` — Connects audio processing and the GUI.
* `gui.py` — Implements the graphical interface.
* `audio.py` — Handles audio input.
* `audio_signal.py` — Implements FFT analysis, HPS, and frequency estimation.
* `notes.py` — Handles musical note and tuning calculations.
* `settings.py` — Stores audio and signal-processing parameters.

## Technologies

* **Python** — Application logic
* **NumPy** — Numerical calculations and signal processing
* **SoundDevice** — Audio input
* **Tkinter** — Graphical user interface
