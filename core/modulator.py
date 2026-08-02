import numpy as np
import wave
import struct

SAMPLE_RATE = 44100
BITS_PER_SYMBOL = 16
SYMBOL_DURATION = 0.08  
TONE_SPACING = 60       
FREQ_START = 18000  # Shifted to near-ultrasonic band

CHIRP_DURATION = 0.1
CHIRP_START_FREQ = 17000
CHIRP_END_FREQ = 17800

SAMPLES_PER_SYMBOL = int(SYMBOL_DURATION * SAMPLE_RATE)

FREQ_PAIRS = []
for i in range(BITS_PER_SYMBOL):
    f0 = FREQ_START + (2 * i) * TONE_SPACING
    f1 = FREQ_START + (2 * i + 1) * TONE_SPACING
    FREQ_PAIRS.append((f0, f1))

def generate_chirp():
    t = np.arange(0, CHIRP_DURATION, 1.0 / SAMPLE_RATE)
    k = (CHIRP_END_FREQ - CHIRP_START_FREQ) / CHIRP_DURATION
    phase = 2 * np.pi * (CHIRP_START_FREQ * t + 0.5 * k * t**2)
    return np.sin(phase).astype(np.float32)

def modulate_bits_to_bfsk(payload_bits):
    num_symbols = len(payload_bits) // BITS_PER_SYMBOL
    total_waveform = np.array([], dtype=np.float32)
    t_symbol = np.arange(0, SYMBOL_DURATION, 1.0 / SAMPLE_RATE)

    for i in range(num_symbols):
        symbol_wave = np.zeros(SAMPLES_PER_SYMBOL, dtype=np.float32)
        symbol_bits = payload_bits[i * BITS_PER_SYMBOL : (i + 1) * BITS_PER_SYMBOL]

        for b_idx, bit in enumerate(symbol_bits):
            target_freq = FREQ_PAIRS[b_idx][bit]
            symbol_wave += np.sin(2 * np.pi * target_freq * t_symbol)

        total_waveform = np.concatenate((total_waveform, symbol_wave))

    chirp_preamble = generate_chirp()
    complete_packet = np.concatenate((chirp_preamble, total_waveform))
    return complete_packet / np.max(np.abs(complete_packet))

def save_wav(waveform, filename="phoneserve_packet.wav"):
    scaled_wave = np.int16(waveform * 32767)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        for sample in scaled_wave:
            w.writeframes(struct.pack('h', sample))
