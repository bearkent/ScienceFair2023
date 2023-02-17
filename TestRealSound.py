
import unittest
import os
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt

import RealSound as rs

class TestSound(unittest.TestCase):
    def test_constructor(self):
        samplingfreq = 10
        xs = np.linspace(0,11,num=110)
        ys = np.cos(3*xs)
        s = rs.Sound(samplingfreq, ys)
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertIsNone(npt.assert_array_equal(ys, s.ys))
        self.assertIsNone(npt.assert_array_equal(xs, s.xs))
        self.assertEqual(110, len(s))

    def test_sine(self):
        duration = 2
        samplingfreq = 10
        frequency = 5
        amplitude = 4.5
        ts = np.linspace(0,duration,num=samplingfreq*duration)
        ys = amplitude*np.sin(2*np.pi*frequency*ts)
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        self.assertEqual(duration*samplingfreq, len(s))
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertIsNone(npt.assert_allclose(ts, s.xs))
        self.assertIsNone(npt.assert_allclose(ys, s.ys))
        self.assertEqual(int(samplingfreq*duration), len(s.xs))
        self.assertEqual(int(samplingfreq*duration), len(s.ys))

        duration = 3.5
        samplingfreq = 11
        frequency = 7.2
        amplitude = 0.6
        ts = np.linspace(0,duration,num=int(samplingfreq*duration))
        ys = amplitude*np.sin(2*np.pi*frequency*ts)
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        self.assertEqual(int(duration*samplingfreq), len(s))
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertIsNone(npt.assert_allclose(ts, s.xs))
        self.assertIsNone(npt.assert_allclose(ys, s.ys))
        self.assertEqual(int(samplingfreq*duration), len(s.xs))
        self.assertEqual(int(samplingfreq*duration), len(s.ys))

    def test_play(self):
        duration = 0.5
        samplingfreq = 44100
        frequency = 10000
        amplitude = 1
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        s.play()

    def test_record(self):
        duration = 0.5
        samplingfreq = 44100
        s = rs.record(duration,samplingfreq)
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertEqual(int(duration*samplingfreq), len(s))
        self.assertEqual(int(duration*samplingfreq), len(s.xs))
        self.assertEqual(int(duration*samplingfreq), len(s.ys))

    def test_read_write(self):
        file = "test.wav"

        if os.path.exists(file):
            os.remove(file)

        duration = 0.5
        samplingfreq = 44100
        frequency = 10000
        amplitude = 1
        s1 = rs.sine(duration, frequency, samplingfreq, amplitude)
        #TODO write
        s2 = rs.newread(file)
        self.assertEqual(samplingfreq, s2.samplingfreq)
        self.assertIsNone(npt.assert_allclose(s1.xs, s2.xs))
        self.assertIsNone(npt.assert_allclose(s1.ys, s2.ys))

        os.remove(file)

    def test_fft(self):
        self.fail()





class TestFFT(unittest.TestCase):

    def test_fail(self):
        self.fail()

class TestPowerSpectrum(unittest.TestCase):
    def test_fail(self):
        self.fail()

class TestUtilityFuncs(unittest.TestCase):
    def test_recordamps(self):
        self.fail()

    def test_meaninverse(self):
        self.fail()

    def test_cubicspline(self):
        self.fail()

    def test_plotspline(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()