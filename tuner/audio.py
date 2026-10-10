import sounddevice as sd
from .settings import sample_rate, block_size
# Audio stream
def find_audio_device(name):
    devices = sd.query_devices()

    for index, device in enumerate(devices):
        if name in device["name"] and device["max_input_channels"] > 0:
            return index

    raise RuntimeError(f"Audio device '{name}' not found")
device_index = find_audio_device("TunerSink")
def create_stream(callback):
    stream = sd.InputStream(
        device=device_index,
        samplerate=sample_rate,
        blocksize=block_size,
        channels=1,
        callback=callback
    )
    return stream
