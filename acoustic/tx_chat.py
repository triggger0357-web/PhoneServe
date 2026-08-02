#!/usr/bin/env python3
"""
PhoneServe Acoustic Data Transmission - Transmitter & Player (tx_chat.py)
Modulates text payloads into an audio stream and plays them directly through the device speaker.
"""

import numpy as np
import wave
import sys
import subprocess
import os

# Audio & Modulation Parameters
SAMPLE_RATE = 44100
CHIRP_DURATION = 0.5  # seconds for sync preamble
F_START = 500         # Hz start frequency for chirp
F_END = 2500          # Hz end frequency for chirp
BAUD_RATE = 20        # Symbols per second for data transmission
TONE_0 = 1200         # Frequency for binary 0
TONE_1 = 2200         # Frequency for binary 1

def generate_sync_chirp(sample_rate=SAMPLE_RATE, duration=CHIRP_DURATION, f_start=F_START, f_end=F_END):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    phase = 2 * np.pi * (f_start * t + 0.5 * (f_end - f_start) * (t / duration))
    signal = np.sin(phase)
    window = np.hanning(len(signal))
    return (signal * window * 32767).astype(np.int16)

def modulate_text_to_tones(text, sample_rate=SAMPLE_RATE, baud=BAUD_RATE):
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    samples_per_symbol = int(sample_rate / baud)
    
    t = np.linspace(0, 1.0 / baud, samples_per_symbol, endpoint=False)
    signal = np.array([], dtype=np.float32)
    
    for bit in binary_data:
        freq = TONE_1 if bit == '1' else TONE_0
        tone = np.sin(2 * np.pi * freq * t)
        signal = np.concatenate((signal, tone))
        
    return (signal * 32767).astype(np.int16)

def play_audio(filename):
    """Plays the generated WAV file through the device speaker using Termux tools."""
    print(f"[*] Emitting acoustic chirp and payload from speaker...")
    try:
        subprocess.run(["mpv", "--no-video", "--really-quiet", filename], check=True)
    except (FileNotFoundError, subprocess.SubprocessError):
        try:
            subprocess.run(["termux-media-player", "play", filename], check=True)
        except (FileNotFoundError, subprocess.SubprocessError):
            print(f"[!] Error: No audio player found. Install mpv via: pkg install mpv")

def create_and_transmit(payload_text, filename="phoneserve_packet.wav"):
    print(f"[*] Encoding payload: '{payload_text}'")
    
    chirp = generate_sync_chirp()
    data_tones = modulate_text_to_tones(payload_text)
    silence = np.zeros(int(SAMPLE_RATE * 0.1), dtype=np.int16)
    full_transmission = np.concatenate((chirp, silence, data_tones, silence))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(full_transmission.tobytes())
        
    print(f"[+] Packet saved to {filename}")
    play_audio(filename)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else "PHONESERVE_NODE_BOOTSTRAP_0357"
    create_and_transmit(payload)
