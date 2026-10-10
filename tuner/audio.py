import sounddevice as sd
from settings import sample_rate, block_size
# Audio stream
def create_stream(callback):
    stream = sd.InputStream(
        samplerate=sample_rate,
        blocksize=block_size,
        channels=1,
        callback=callback
    )
    return stream
