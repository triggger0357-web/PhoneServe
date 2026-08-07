import numpy as np
import struct
import wave
import sys
from scipy.io import wavfile

class AcousticTxEncoder:
    """
    Encodes binary payloads into 0xAC01 acoustic frames and modulates
    them into phase-continuous BFSK audio waveforms.
    """
    MAGIC_HEADER = b'\xac\x01'
    
    # Audio Parameters
    SAMPLE_RATE = 44100       # Hz
    FREQ_MARK = 2400.0        # Hz (Bit 1)
    FREQ_SPACE = 1800.0       # Hz (Bit 0)
    FREQ_PREAMBLE = 3000.0    # Hz (Sync tone)
    SYMBOL_DURATION = 0.010   # 10ms per bit (100 baud rate)

    @staticmethod
    def calculate_crc16(data: bytes) -> int:
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc & 0xFFFF

    @classmethod
    def build_frame(cls, payload: bytes) -> bytes:
        if len(payload) > 255:
            raise ValueError("Payload exceeds maximum acoustic frame capacity (255 bytes)")
        
        header_and_len = cls.MAGIC_HEADER + bytes([len(payload)])
        raw_content = header_and_len + payload
        checksum = cls.calculate_crc16(raw_content)
        return raw_content + struct.pack('<H', checksum)

    @classmethod
    def bytes_to_bits(cls, data: bytes) -> list:
        bits = []
        for byte in data:
            for i in range(7, -1, -1): # MSB to LSB
                bits.append((byte >> i) & 1)
        return bits

    @classmethod
    def synthesize_bfsk_wave(cls, payload: bytes, output_filename: str = "acoustic_tx.wav"):
        frame = cls.build_frame(payload)
        bits = cls.bytes_to_bits(frame)
        
        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        audio_chunks = []
        phase = 0.0

        # 1. Preamble Tone (100ms sync burst to wake receiver filter)
        preamble_samples = int(cls.SAMPLE_RATE * 0.100)
        t_pre = np.arange(preamble_samples) / cls.SAMPLE_RATE
        audio_chunks.append(np.sin(2 * np.pi * cls.FREQ_PREAMBLE * t_pre))

        # 2. Modulate Bits into Phase-Continuous Frequencies
        for bit in bits:
            freq = cls.FREQ_MARK if bit == 1 else cls.FREQ_SPACE
            phase_increment = 2.0 * np.pi * freq / cls.SAMPLE_RATE
            phases = phase + np.arange(samples_per_symbol) * phase_increment
            phase = (phases[-1] + phase_increment) % (2.0 * np.pi)
            
            chunk = np.sin(phases)
            audio_chunks.append(chunk)

        # 3. Trailing Silence (50ms buffer)
        silence_samples = int(cls.SAMPLE_RATE * 0.050)
        audio_chunks.append(np.zeros(silence_samples))

        # 4. Concatenate and normalize to 16-bit PCM integer WAV format
        full_waveform = np.concatenate(audio_chunks)
        normalized_pcm = np.int16(full_waveform * 32767 * 0.8)

        # Save audio WAV file
        wavfile.write(output_filename, cls.SAMPLE_RATE, normalized_pcm)
        
        frame_hex = frame.hex()
        print(f"[Acoustic TX] Encoded Payload: '{payload.decode(errors='ignore')}'")
        print(f"[Acoustic TX] Output Frame: 0x{frame_hex}")
        print(f"[Acoustic TX] Generated WAV: '{output_filename}' ({len(normalized_pcm)} samples)")
        return output_filename

if __name__ == "__main__":
    payload_str = sys.argv[1] if len(sys.argv) > 1 else "tx_sound_pkt_0357"
    AcousticTxEncoder.synthesize_bfsk_wave(payload_str.encode('utf-8'))
