import RealSound as rs

sound = rs.record(10, 44100)
sound.play()
sound.write('guitarrecording.wav')