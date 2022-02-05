import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata[::downsample, mapping])
    #frequency = np.fft.fft(indata)
    #print(frequency)

def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


def main():
    global q, plotdata, lines, mapping, downsample, frequency, lines1

    channels = [1]
    device = None
    window = 200
    interval = 30
    samplerate = 10000
    downsample = 10

    mapping = [c - 1 for c in channels]  # Channel numbers start with 1
    q = queue.Queue()

    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        samplerate = device_info['default_samplerate']

    print(samplerate)

    length = int(window * samplerate / (1000 * downsample))
    plotdata = np.zeros((length, len(channels)))
    frequency = []

    fig, ax = plt.subplots(2)
    lines = ax[0].plot(plotdata)
    lines1 = ax[1].plot([], [], '-o')
    if len(channels) > 1:
        ax[0].legend(['channel {}'.format(c) for c in channels],
                  loc='lower left', ncol=len(channels))
    ax[0].axis((0, len(plotdata), -1, 1))
    ax[0].set_yticks([0])
    ax[0].yaxis.grid(True)
    ax[0].tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=device, channels=max(channels),
        samplerate=samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)

    with stream:
        plt.show()
        """
        while True:
            print(stream.read(400))
        """

main()