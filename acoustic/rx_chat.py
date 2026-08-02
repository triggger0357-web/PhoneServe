#!/usr/bin/env python3
"""
PhoneServe Acoustic Data Transmission - Receiver & Listener (rx_chat.py)
Listens for the sync chirp, synchronizes, and decodes FSK audio payloads.
"""

import numpy as np
import wave
import sys
import time

try:
    import sounddevice as sd
except ImportError:
    print("[!] sounddevice not found. Install via: pip install sounddevice")
    sys.exit(1)

SAMPLE_RATE = 44100
CHIRP_DURATION = 0.5
F_START = 500
F_END = 2500
BAUD_RATE = 20
TONE_0 = 1200
TONE_1 = 2200

def generate_sync_chirp():
    t = np.linspace(0, CHIRP_DURATION, int(SAMPLE_RATE * CHIRP_DURATION), endpoint=False)
    phase = 2 * np.pi * (F_START * t + 0.5 * (F_END - F_START) * (t / CHIRP_DURATION))
    signal = np.sin(phase)
    window = np.hanning(len(signal))
    return signal * window

def decode_fsk(signal, sample_rate=SAMPLE_RATE, baud=BAUD_RATE):
    samples_per_symbol = int(sample_rate / baud)
    num_symbols = len(signal) // samples_per_symbol
    binary_chars = []
    
    for i in range(num_symbols):
        symbol_chunk = signal[i * samples_per_symbol : (i + 1) * samples_per_symbol]
        if len(symbol_chunk) < samples_per_symbol:
            break
        fft_res = np.abs(np.fft.rfft(symbol_chunk))
        freqs = np.fft.rfftfreq(len(symbol_chunk), 1/sample_rate)
        
        idx_0 = np.argmin(np.abs(freqs - TONE_0))
        idx_1 = np.argmin(np.abs(freqs - TONE_1))
        
        bit = '1' if fft_res[idx_1] > fft_res[idx_0] else '0'
        binary_chars.append(bit)
        
    binary_str = ''.join(binary_chars)
    chars = []
    for j in range(0, len(binary_str) - 7, 8):
        byte = binary_str[j:j+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def listen_loop():
    print("[*] Listening for PhoneServe acoustic sync chirp...")
    chirp_template = generate_sync_chirp()
    chunk_duration = 3.0  
    chunk_samples = int(SAMPLE_RATE * chunk_duration)
    
    while True:
        audio_chunk = sd.rec(chunk_samples, samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        audio_flat = audio_chunk.flatten()
        
        correlation = np.correlate(audio_flat, chirp_template, mode='valid')
        if len(correlation) > 0:
            max_idx = np.argmax(correlation)
            peak_val = correlation[max_idx]
            
            if peak_val > 10.0:  
                print(f"[+] Sync chirp detected! (Peak: {peak_val:.2f})")
                data_start = max_idx + len(chirp_template) + int(SAMPLE_RATE * 0.1)
                data_len = int(SAMPLE_RATE * (400 / BAUD_RATE))
                
                if data_start + data_len <= len(audio_flat):
                    data_segment = audio_flat[data_start:data_start + data_len]
                    decoded_text = decode_fsk(data_segment)
                    print(f"[+] Decoded Payload: {decoded_text}")
                    return decoded_text
                else:
                    print("[!] Chirp near frame boundary, re-listening...")

if __name__ == "__main__":
    listen_loop()
