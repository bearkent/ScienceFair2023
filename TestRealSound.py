
import unittest
import os
import numpy as np
import numpy.testing as npt
import matplotlib.pyplot as plt
from fix import fix
import RealSound as rs

class TestSound(unittest.TestCase):
    def test_constructor(self):
        samplingfreq = 10
        duration = 11
        n = int(samplingfreq*duration) + 1
        xs = np.arange(0, n) / samplingfreq
        ys = np.cos(3*xs)
        s = rs.Sound(samplingfreq, ys)
        remainder = len(s) % 2
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertEqual(0, remainder)
        self.assertIsNone(npt.assert_array_equal(ys[:-1], s.ys))
        self.assertIsNone(npt.assert_array_equal(xs[:-1], s.xs))

    def test_sine(self):
        duration = 2
        samplingfreq = 10
        frequency = 2
        amplitude = 4
        n = int(samplingfreq*duration)
        ts = np.arange(0, n) / samplingfreq
        ys = amplitude*np.sin(2*np.pi*frequency*ts)
        s = rs.sine(duration, frequency, samplingfreq, amplitude)
        remainder = len(s.ys) % 2
        self.assertEqual(0, remainder)
        self.assertEqual(samplingfreq, s.samplingfreq)
        self.assertEqual(n, len(s.xs))
        self.assertEqual(n, len(s.ys))
        print(f"x-ts: {ts}")
        print(f"x-s: {s.xs}")
        self.assertIsNone(npt.assert_allclose(ts, s.xs))
        print(f"y-ys: {ys}")
        print(f"y-s: {s.ys}")
        self.assertIsNone(npt.assert_allclose(ys, s.ys, atol=1e-7, rtol=1))

        duration = 3.5
        samplingfreq = 11
        frequency = 7.2
        amplitude = 0.6
        n = int(samplingfreq*duration)
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
        duration = 2
        samplingfreq = 44100
        frequency1 = 5000
        frequency2 = 15000
        amplitude = 1
        s1 = rs.sine(duration, frequency1, samplingfreq, amplitude)
        s2 = rs.sine(duration, frequency2, samplingfreq, amplitude)
        s_in = rs.Sound(samplingfreq, s1.ys + s2.ys)

        #TODO: Debug hack
        # s_in.xs = s_in.xs[:-1]
        # s_in.ys = s_in.ys[:-1]

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

        def func(x):

            return x*2

        sinewave = rs.sine(1, 100, 44100, 1)
        fft = sinewave.fft()

        fft.multiply(func)
        ifft = fft.ifft()

        self.assertAlmostEqual(sinewave.ys[0], ifft.ys[0]/2, delta=1e-5)

        def func2(x):

            return x**2

        ys = np.array([1,3,4,64,2,3,234,6534])

        fft2 = rs.FFT(10, ys)

        fft2.multiply(func2)

        self.assertAlmostEqual(ys[0], fft2.ys[0]**0.5, delta=1e-2)


class TestPowerSpectrum(unittest.TestCase):

    def test_shapes(self):

        sinewave = rs.sine(1, 1000, 44100, 1)
        fft = sinewave.fft()

        self.assertEqual(len(fft.xs), len(fft.ys))

    def test_frequencies(self):
        duration = 0.5
        samplingfreq = 44100

        frequency = 100
        amplitude = 10
        s1 = rs.sine(duration, frequency, samplingfreq, amplitude)
        s_in = rs.Sound(samplingfreq, s1.ys)

        fft = s_in.fft()
        ps = rs.PowerSpectrum(fft)
        # ps.plot()
        # fix()

        xmax,ymax,amp = ps.max()
        self.assertAlmostEqual(frequency, xmax, delta=1e-2)
        self.assertAlmostEqual(amplitude*amplitude, ymax, delta=1e-1)
        self.assertAlmostEqual(amplitude, ymax**0.5, delta=1e-2)

        #TODO: repeat with another frequency and amplitude

        duration2 = 1
        samplingfreq2 = 88200

        frequency2 = 1000
        amplitude2 = 7
        s2 = rs.sine(duration2, frequency2, samplingfreq2, amplitude2)
        s_in2 = rs.Sound(samplingfreq2, s2.ys)

        fft2 = s_in2.fft()
        ps2 = rs.PowerSpectrum(fft2)
        # ps.plot()
        # fix()

        xmax2, ymax2, amp2 = ps2.max()
        self.assertAlmostEqual(frequency2, xmax2, delta=1e-2)
        self.assertAlmostEqual(amplitude2 * amplitude2, ymax2, delta=1e-1)
        self.assertAlmostEqual(amplitude2, ymax2 ** 0.5, delta=1e-2)

class TestUtilityFuncs(unittest.TestCase):

    # def test_recordamps(self):
    #
    #     testfreq = 20
    #     step = 1000
    #     endfreq = 20000
    #     freqs = np.arange(20, 20000, 1000)
    #
    #     samplingfreq = 44100
    #     samplingtime = 1
    #
    #     vals = rs.recordamps(testfreq, step, endfreq, samplingfreq, samplingtime)
    #
    #     self.fail()

    def test_meaninverse(self):

        ys = np.array([1, 2, 3])
        inverseys = rs.meaninverse(ys)

        self.assertIsNone(npt.assert_allclose(np.array([2, 1, 2/3]), inverseys))

    def test_cubicspline(self):

        f = rs.cubicspline(np.array([0, 1, 2]), np.array([2, 2, 2]))
        y = f(0.5)

        self.assertEqual(2, y)

if __name__ == '__main__':
    unittest.main()