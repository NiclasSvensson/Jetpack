import numpy as np
import sounddevice as sd

class Input:
    def __init__(self):
        self.channels = [1]
        self.device = None
        self.samplerate = None
        self.downsample = 10
        self.mapping = [c - 1 for c in self.channels]
        self.samples = 2000
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, 'input')
            self.samplerate = device_info['default_samplerate']
        self.coefficients = np.fft.fftfreq(self.samples//self.downsample, 1/(self.samplerate/self.downsample))
        self.stream = sd.InputStream(device=self.device, channels=max(self.channels), samplerate=self.samplerate)

    def get_frequency(self):
        self.stream.start()
        signal = 100*self.stream.read(self.samples)[0][::self.downsample]
        fourier = np.fft.fft(signal, axis=0)
        i = np.abs(np.max(fourier[1:]))
        f = np.abs(self.coefficients[np.argmax(fourier[1:])])
        if i > 40:
            return f
        else:
            return 0