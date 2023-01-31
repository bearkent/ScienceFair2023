import os
import thinkdsp
# import wget
# import thinkdsp.py

# if not os.path.exists('thinkdsp.py'):
#     wget.download(https://github.com/AllenDowney/ThinkDSP/raw/master/code/thinkdsp.py)
    
from thinkdsp import CosSignal, SinSignal

cos_sig = CosSignal(freq=440, amp=1.0, offset=0)
sin_sig = SinSignal(freq=880, amp=0.5, offset=0)

from thinkdsp import decorate

# p1 = sin_sig.plot()
decorate(xlabel='Time (s)')

# p2 = cos_sig.plot()
decorate(xlabel='Time (s)')

mix = cos_sig+sin_sig
period = mix.period

wave = mix.make_wave(duration=0.5, start=0, framerate=11025)
# wave.make_audio()
# segment = wave.segment(start=0, duration=period*3)
# mix.plot()

# wave.write('temp.wav')
# thinkdsp.play_wave(filename='temp.wav', player='play')
# wave.play('temp.wav')

spectrum = wave.make_spectrum()
# spectrum.low_pass(500, 0.5)
spectrum.plot()
decorate(xlabel='Frequency (Hz)')

import matplotlib
matplotlib.pyplot.show(block=True)