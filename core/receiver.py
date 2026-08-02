import numpy as np
import wave

SAMPLE_RATE = 44100
BITS_PER_SYMBOL = 16
SYMBOL_DURATION = 0.08  
TONE_SPACING = 60       
FREQ_START = 18000  # Must match transmitter precisely

CHIRP_DURATION = 0.1
CHIRP_START_FREQ = 17000
CHIRP_END_FREQ = 17800

SAMPLES_PER_SYMBOL = int(SYMBOL_DURATION * SAMPLE_RATE)

FREQ_PAIRS = []
for i in range(BITS_PER_SYMBOL):
    f0 = FREQ_START + (2 * i) * TONE_SPACING
    f1 = FREQ_START + (2 * i + 1) * TONE_SPACING
    FREQ_PAIRS.append((f0, f1))

def load_wav(filename):
    with wave.open(filename, 'rb') as w:
        n_samples = w.getnframes()
        data = w.readframes(n_samples)
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
        return audio

def generate_chirp():
    t = np.arange(0, CHIRP_DURATION, 1.0 / SAMPLE_RATE)
    k = (CHIRP_END_FREQ - CHIRP_START_FREQ) / CHIRP_DURATION
    phase = 2 * np.pi * (CHIRP_START_FREQ * t + 0.5 * k * t**2)
    return np.sin(phase).astype(np.float32)

def demodulate_audio_to_bits(audio_data):
    chirp = generate_chirp()
    corr = np.correlate(audio_data, chirp, mode='valid')
    if len(corr) == 0:
        return np.array([], dtype=np.int16)
        
    sync_idx = np.argmax(np.abs(corr)) + len(chirp)
    bits = []
    t_symbol = np.arange(0, SYMBOL_DURATION, 1.0 / SAMPLE_RATE)
    
    f0_vectors = [np.exp(-2j * np.pi * f0 * t_symbol) for f0, f1 in FREQ_PAIRS]
    f1_vectors = [np.exp(-2j * np.pi * f1 * t_symbol) for f0, f1 in FREQ_PAIRS]
    
    idx = sync_idx
    while idx + SAMPLES_PER_SYMBOL <= len(audio_data):
        symbol_samples = audio_data[idx : idx + SAMPLES_PER_SYMBOL]
        if len(symbol_samples) < SAMPLES_PER_SYMBOL:
            break
            
        for b_idx in range(BITS_PER_SYMBOL):
            mag_f0 = np.abs(np.dot(symbol_samples, f0_vectors[b_idx]))
            mag_f1 = np.abs(np.dot(symbol_samples, f1_vectors[b_idx]))
            bits.append(1 if mag_f1 > mag_f0 else 0)
                
        idx += SAMPLES_PER_SYMBOL
        if len(bits) >= 2048:
            break
            
    return np.array(bits, dtype=np.int16)
