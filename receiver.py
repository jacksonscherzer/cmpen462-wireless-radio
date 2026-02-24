import math, numpy as np

def downconvert(input_file, carrier_freq, sample_rate):
    """
    Downconvert the input signal to baseband

    Parameters:
    input_file: The path to the input file containing signal samples
    carrier_freq: The frequency of the carrier signal in Hz
    sample_rate: sampling rate of the input signal (Hz)

    Returns:
    I and Q components of the downconverted signal as a list of complex numbers
    """
    i = []
    q = []
    input = []
    with open(input_file, 'r') as f:
        for line in f:
            input.append(int(line.strip()))
    for n, sample in enumerate(input):
        i[n] = sample * math.cos(2 * math.pi * carrier_freq * n / sample_rate)
        q[n] = sample * math.sin(2 * math.pi * carrier_freq * n / sample_rate)
    
    return i, q

def lowpass_filter(i, q, cutoff_freq, sample_rate):
    """
    Compute 3000-point FFT and eliminate frequencies outside +-5.1 Hz

    Uses numpy FFT functions to perform FFT and IFFT

    Parameters:
    i and q: components of our downconverted signal
    cutoff_freq: limit frequency at which we set signals to 0 (+-5.1 Hz in this case)
    sample rate: sampling rate of the input signal (Hz)

    Returns:
    i_f and q_f: components of filtered signal
    """
    # get length
    N = len(i)

    # calculate frequency for filtering

    # filter i
    freqs = np.fft.fftfreq(N, 1/sample_rate)

    X = np.fft.fft(i)
    X[np.abs(freqs) > cutoff_freq] = 0
    i_f = np.real(np.fft.ifft(X))       #use real to remove imaginary parts and eliminate noise

    #filter q
    Y = np.fft.fft(q)
    Y[np.abs(freqs) > cutoff_freq] = 0
    q_f = np.real(np.fft.ifft(Y))       #same as above to elimintate noise

    return i_f, q_f

def downsample(i, q):
    """
    Combine i and  q, then downsample to collect every 10th frequency

    Parameters:
    i, q: components of filtered signal

    Returns:
    r_ds: downsampled signal r that combines i and q, and contains every 10th sample
    """

    # combine signals

    r = i + 1j * q

    # downsample

    r_ds = r[::10]      #takes every 10th sample

    return r_ds


