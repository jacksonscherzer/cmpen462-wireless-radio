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

    #read preamble file 
    with open(input_file, 'r') as f:
        for line in f:
            input.append(float(line.strip()))

    # downconversion
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

    freqs = np.fft.fftfreq(N, 1/sample_rate)

    # filter i
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

def correlate(r, preamble_file):
    """
    Use the given preamble to correlate our signal with the preamble to find peak coorelation

    Parameters:
    r: downsampled signal
    preamble_file: path to file containing preamble data

    Returns:
    symbols: all matching symbols after removing preamble
    """

    #read preamble file
    preamble = []
    with open(preamble_file, 'r') as f:
        for line in f:
            preamble.append(complex(line.strip()))

    # make preamble numpy array
    preamble = np.array(preamble)
    
    # correlate
    corr = np.correlate(r, preamble, mode='valid')

    # find start index
    index = np.argmax(np.abs(corr))

    #set where data starts
    start = index + len(preamble)
    symbols = r[start:]

    #test to check peak mag
    print("Peak corr mag: ", np.max(np.abs(corr)))

    return symbols

def demodulate(symbols):
    """
    Match each symbol value to closest of -3, -1, 1 and 3

    Parameters:
    symbols: correlated values of our signal

    Returns:
    binary: binary string created from mapping signal to grid
    """

    #define levels
    levels = np.array([-3, -1, 1, 3])

    #create mapping based on diagram
    mapping = {
        -3: "10",
        -1: "11",
        1: "01",
        3: "00"
    }

    #process
    binary = ""

    for s in symbols:

        #get real and imaginary
        I = np.real(s)
        Q = np.imag(s)

        #map each I and Q to nearest level
        I_m = levels[np.argmin(np.abs(levels - I))]
        Q_m = levels[np.argmin(np.abs(levels - Q))]

        #add to binary
        binary += mapping[Q_m] + mapping[I_m]

    return binary

def ascii(binary):
    """
    Convert binary string to ascii values

    Parameters:
    binary: string of bits created from demodulation

    Return:
    ascii: string of ascii characters
    """

    ascii = ""

    #create integer and convert to char
    for i in range(0, len(binary), 8):
        #create byte
        byte = binary[i:i+8]

        #ignore incomplete bytes (if binary is not length 0 mod 8)
        if len(byte) < 8:
            break
            
        #create char
        ascii += chr(int(byte, 2))      #base 2 --> integer

    return ascii

input_file = 'input.txt'
preamble_file = 'preamble.txt'
carrier_freq = 20
sampling_rate = 100
cutoff_freq = 5.1

i, q = downconvert(input_file, carrier_freq, sampling_rate)

i_f, q_f = lowpass_filter(i, q, cutoff_freq, sampling_rate)

r = downsample(i_f, q_f)

symbols = correlate(r, preamble_file)

binary = demodulate(symbols)

text = ascii(binary)

print(text)