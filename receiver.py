import math

def downconvert(input_file, carrier_freq, sample_rate):
    """
    Downconvert the input signal to baseband.

    Parameters:
    input_file (str): The path to the input file containing signal samples.
    carrier_freq (float): The frequency of the carrier signal in Hz.
    sample_rate (float): The sampling rate of the input signal in Hz.

    Returns:
    I and Q components of the downconverted signal as a list of complex numbers.
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
