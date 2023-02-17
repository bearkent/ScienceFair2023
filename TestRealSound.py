
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
        amplitude = 4
        n = int(samplingfreq*duration) + 1
        ts = np.arange(0, n) / samplingfreq
        ys = amplitude*np.sin(2*np.pi*frequency*ts)
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        self.assertEqual(n, len(s))
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertEqual(n, len(s.xs))
        self.assertEqual(n, len(s.ys))
        print(f"x-ts: {ts}")
        print(f"x-s: {s.xs}")
        self.assertIsNone(npt.assert_allclose(ts, s.xs))
        print(f"y-ys: {ys}")
        print(f"y-s: {s.ys}")
        self.assertIsNone(npt.assert_allclose(ys, s.ys, atol=1e-7, rtol=1))

        #TODO: amplitude looks too small...

        duration = 3.5
        samplingfreq = 11
        frequency = 7.2
        amplitude = 0.6
        n = int(samplingfreq*duration) + 1
        ts = np.arange(0, n) / samplingfreq
        ys = amplitude*np.sin(2*np.pi*frequency*ts)
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        self.assertEqual(n, len(s))
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertEqual(n, len(s.xs))
        self.assertEqual(n, len(s.ys))
        print(f"x-ts: {ts}")
        print(f"x-s: {s.xs}")
        self.assertIsNone(npt.assert_allclose(ts, s.xs))
        print(f"y-ys: {ys}")
        print(f"y-s: {s.ys}")
        self.assertIsNone(npt.assert_allclose(ys, s.ys, atol=1e-7, rtol=1))

        #TODO: amplitude looks too small...

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
        s1.write(file)
        s2 = rs.soundread(file)
        self.assertEqual(samplingfreq, s2.samplingfreq)
        self.assertIsNone(npt.assert_allclose(s1.xs, s2.xs))
        self.assertIsNone(npt.assert_allclose(s1.ys, s2.ys))

        os.remove(file)

class TestFFT(unittest.TestCase):

    def test_roundtrip(self):
        duration = 0.5
        samplingfreq = 44100
        frequency1 = 5000
        frequency2 = 15000
        amplitude = 1
        s1 = rs.sine(duration, frequency1, samplingfreq, amplitude)
        s2 = rs.sine(duration, frequency2, samplingfreq, amplitude)
        s_in = rs.Sound(samplingfreq, s1.ys + s2.ys)

        fft = s_in.fft()

        self.assertEqual(samplingfreq, fft.samplingfreq)
        #TODO: assert expected contents of fft
        # self.assertEqual(len(s_in), len(fft))
        # self.assertEqual(len(s_in), len(fft.xs))
        # self.assertEqual(len(s_in), len(fft.ys))
        #TODO: assert xs values are exactly what is expected

        s_out = fft.ifft()

        self.assertEqual(samplingfreq, s_out.samplingfreq)
        self.assertEqual(len(s_in), len(s_out))
        self.assertEqual(len(s_in), len(s_out.xs))
        self.assertEqual(len(s_in), len(s_out.ys))
        self.assertIsNone(npt.assert_allclose(s_in.xs, s_out.xs))
        self.assertIsNone(npt.assert_allclose(s_in.ys, s_out.ys, atol=1e-7, rtol=1))

    def test_multiply(self):
        self.fail()

class TestPowerSpectrum(unittest.TestCase):
    def test_frequencies(self):
        duration = 0.5
        samplingfreq = 44100
        frequency1 = 5000
        frequency2 = 15000
        amplitude = 1
        s1 = rs.sine(duration, frequency1, samplingfreq, amplitude)
        s2 = rs.sine(duration, frequency2, samplingfreq, amplitude)
        s_in = rs.Sound(samplingfreq, s1.ys + s2.ys)

        fft = s_in.fft()
        #TODO: determine if the power spectrum has major peaks at frequency1 and frequency2
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