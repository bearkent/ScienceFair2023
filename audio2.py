#!/usr/bin/env python3
# Refs:
#   https://stackoverflow.com/questions/41293140/read-and-play-audio-in-python3
#   https://pypi.org/project/simpleaudio/
#   https://simpleaudio.readthedocs.io/en/latest/tutorial.html#

# import audioread
# import numpy as np
# # fin  = audioread.audio_open('test_justin.amr')
# fin  = audioread.audio_open('170255__dublie__trumpet.wav')
# dat  = [x for x in fin]          #Generate list of bytestrings
# dat  = b''.join(dat)             #Join bytestrings into a single urbytestring
# ndat = np.fromstring(dat, '<i2') #Convert from audioread format to numbers
#
# #Generate a wave file in memory
# import scipy.io.wavfile
# import io
# memory_file = io.BytesIO() #Buffer to write to
# scipy.io.wavfile.write(memory_file, fin.samplerate, ndat)

#Play the wave file
import simpleaudio
def play_audio(wav_file):
    # wave_obj = simpleaudio.WaveObject.from_wave_file(memory_file)
    wave_obj = simpleaudio.WaveObject.from_wave_file(wav_file)
    play_obj = wave_obj.play()
    # play_obj.wait_done()

    # while play_obj.is_playing():
    #     input("Press Enter to stop playback")
    #     break
    play_obj.stop()

