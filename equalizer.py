import thinkdsp
import os
from scipy.io.wavfile import write
from audio2 import play_audio
import sounddevice as sd
import datetime
from datetime import datetime
import soundfile as sf
from pathlib import Path

def delete_files():
    
    print("deleting audio files")
    
    for x in range(0, 100):
        audio_path = Path("./recording{x}.wav")
        
        if audio_path.is_file():
            os.remove(f"recording{x}.wav")
            
        else:
            return

def record(freq, duration, x):
    
    print("recording")
    
    # start_time = datetime.now()
    
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1, dtype=float)
    sd.wait()
    
    # end_time = datetime.now()
    
    write(f"recording{x}.wav", freq, recording)

    # print('Duration: {}'.format(end_time - start_time))
    
    print("done recording")
    
    # return f"recording{x}.wav"

def record_audio(freq, duration, x):
    freq = 44100
    duration = 2
    
    record(freq, duration, x)
    # return record(freq, duration, x)
    
    # return recording

    # print(record(freq, duration))

def play_audio2(freq=44100, duration=1, x=0, filename="file.wav"):
    
    record_audio(freq, duration, x)
    print("playing recording")
    data, fs = sf.read(filename)
    sd.play(data, fs)
    sd.wait()

# delete_files()
play_audio2(44100, 2, 1, "recording0.wav")    

# sd.play(record_audio())

    

def equalizer():
    
    frequency = 1000
    
    start_time = datetime.now()
    
    while frequency <= 20000:

        signal = thinkdsp.SinSignal(frequency)
        wave = signal.make_wave(start=0, duration=1, framerate=44100)
        wave.apodize()
        
        x = 1
        wave.write(f"sine{x}.wav")
        # record_audio()
        play_audio(f"sine{x}.wav")
        x += 1
        
        print(f"The frequency played is {frequency}.")
        
        frequency += 1000
        
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
        
# equalizer()

from fix import fix
fix()


# duration = signal.period*100
# segment = signal.make_wave(duration, framerate=100000)
# # segment.plot()
# spectrum = segment.make_spectrum()
# spectrum.plot()
# decorate(xlabel='Frequency (s)')