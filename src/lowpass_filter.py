import numpy as np
from scipy.signal import butter, lfilter, freqz
from matplotlib import pyplot as plt


order = 6
fs = 30  # Frequncy 860 Hz
cutoff = 0.08  # Cut off frequncy 50 Hz

data = (
    1.805,
    1.805,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.806,
    1.807,
    1.807,
    1.805,
    1.806,
    1.806,
    1.806,
    1.806,
    1.805,
    1.808,
    1.806,
    1.806,
    1.806,
    1.805,
    1.806,
    1.806,
    1.806,
    1.807,
    1.807,
    1.807,
    1.807,
    1.806,
    1.806,
    1.806,
    1.807,
    1.807,
    1.807,
    1.807,
    1.806,
    1.806,
    1.805,
    1.806,
    1.807,
    1.807,
    1.807,
    1.806,
    1.807,
    1.806,
    1.806,
    1.807,
    1.807,
    1.807,
    1.807,
    1.807,
    1.806,
    1.807,
    1.807,
    1.807,
    1.807,
    1.807,
    1.807,
    1.807,
    1.806,
    1.807,
    1.807,
    1.807,
    1.807,
    1.808,
    1.807,
    1.808,
    1.808,
    1.807,
    1.807,
    1.808,
    1.806,
    1.807,
    1.806,
    1.807,
    1.807,
    1.808,
)


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
# order = 6
# fs = 30.0  # sample rate, Hz
# cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)
print(y)