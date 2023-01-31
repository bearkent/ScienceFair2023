import sounddevice as sd
import soundfile as sf
import thinkdsp
from thinkdsp import CosSignal


def record(freq, duration):
    
    print("recording")
    
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=float)
    sd.wait()
    
    return recording
    
recording = record(44100, 1)

recording_wave = thinkdsp.Wave(recording, None, 44100)

cos_sig = CosSignal(freq=440, amp=1.0, offset=0)
cos_wave = cos_sig.make_wave(1, 0, 44100)

# print(cos_wave)

# print(type(recording))
# print(type(cos_wave.ys))

spectrum = recording_wave.make_spectrum()

spectrum.plot(high=22050)
thinkdsp.decorate(xlabel='Frequency (Hz)')

import matplotlib
matplotlib.pyplot.show(block=True)


