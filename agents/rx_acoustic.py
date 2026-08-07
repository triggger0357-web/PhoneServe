import numpy as np
import struct
import sys
from scipy.io import wavfile

class AcousticRxDecoder:
    """
    Decodes BFSK acoustic WAV files using Goertzel tone filters.
    Detects 0xAC01 magic header, extracts payload, and verifies CRC16.
    """
    MAGIC_HEADER = b'\xac\x01'
    SAMPLE_RATE = 44100       # Hz
    FREQ_MARK = 2400.0        # Hz (Bit 1)
    FREQ_SPACE = 1800.0       # Hz (Bit 0)
    FREQ_PREAMBLE = 3000.0    # Hz (Sync Tone)
    SYMBOL_DURATION = 0.010   # 10ms per symbol (441 samples @ 44.1kHz)

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
    def goertzel_filter(cls, samples: np.ndarray, target_freq: float) -> float:
        """Calculates power spectral density at target_freq using Goertzel algorithm."""
        N = len(samples)
        if N == 0:
            return 0.0
        k = int(0.5 + (N * target_freq) / cls.SAMPLE_RATE)
        w = (2.0 * np.pi / N) * k
        cosine = np.cos(w)
        sine = np.sin(w)
        coeff = 2.0 * cosine
        
        q1, q2 = 0.0, 0.0
        for sample in samples:
            q0 = coeff * q1 - q2 + sample
            q2 = q1
            q1 = q0
            
        real = q1 - q2 * cosine
        imag = q2 * sine
        return (real * real) + (imag * imag)

    @classmethod
    def decode_wav(cls, wav_path: str):
        sr, raw_data = wavfile.read(wav_path)
        if sr != cls.SAMPLE_RATE:
            raise ValueError(f"Sample rate mismatch: expected {cls.SAMPLE_RATE} Hz, got {sr} Hz")

        # Normalize audio samples to [-1.0, 1.0]
        if raw_data.dtype == np.int16:
            data = raw_data.astype(np.float32) / 32768.0
        else:
            data = raw_data.astype(np.float32)

        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)

        # 1. Detect Preamble (3000 Hz) to synchronize symbol boundary
        scan_step = 44 # ~1ms sliding window steps
        preamble_end_idx = 0
        in_preamble = False

        for idx in range(0, len(data) - samples_per_symbol, scan_step):
            chunk = data[idx : idx + samples_per_symbol]
            p_preamble = cls.goertzel_filter(chunk, cls.FREQ_PREAMBLE)
            p_mark = cls.goertzel_filter(chunk, cls.FREQ_MARK)
            p_space = cls.goertzel_filter(chunk, cls.FREQ_SPACE)

            if p_preamble > 50.0 and p_preamble > (p_mark + p_space) * 2:
                in_preamble = True
            elif in_preamble:
                preamble_end_idx = idx
                break

        # 2. Extract bitstream starting at data symbol boundary
        bits = []
        curr = preamble_end_idx
        while curr + samples_per_symbol <= len(data):
            chunk = data[curr : curr + samples_per_symbol]
            p_mark = cls.goertzel_filter(chunk, cls.FREQ_MARK)
            p_space = cls.goertzel_filter(chunk, cls.FREQ_SPACE)

            # Silence threshold check
            if p_mark < 0.5 and p_space < 0.5:
                break

            bit = 1 if p_mark >= p_space else 0
            bits.append(bit)
            curr += samples_per_symbol

        # 3. Locate Magic Header (0xAC01) in bitstream
        decoded_bytes = bytearray()
        for offset in range(len(bits) - 16):
            byte1, byte2 = 0, 0
            for i in range(8):
                byte1 = (byte1 << 1) | bits[offset + i]
                byte2 = (byte2 << 1) | bits[offset + 8 + i]

            if bytes([byte1, byte2]) == cls.MAGIC_HEADER:
                # Align bytes from header offset
                for b_idx in range(offset, len(bits) - 7, 8):
                    val = 0
                    for i in range(8):
                        val = (val << 1) | bits[b_idx + i]
                    decoded_bytes.append(val)
                break

        if len(decoded_bytes) < 5:
            return False, "Failed to detect 0xAC01 magic header in acoustic signal", b""

        # 4. Parse frame & verify CRC16 checksum
        payload_len = decoded_bytes[2]
        total_frame_len = 3 + payload_len + 2
        
        if len(decoded_bytes) < total_frame_len:
            return False, f"Frame incomplete (expected {total_frame_len} bytes)", b""

        frame_data = bytes(decoded_bytes[:total_frame_len])
        raw_header_and_payload = frame_data[:3 + payload_len]
        received_crc = struct.unpack('<H', frame_data[3 + payload_len : total_frame_len])[0]
        computed_crc = cls.calculate_crc16(raw_header_and_payload)

        if received_crc != computed_crc:
            return False, f"CRC mismatch: expected {hex(computed_crc)}, got {hex(received_crc)}", b""

        payload = frame_data[3 : 3 + payload_len]
        return True, "CRC16 Verified", payload

if __name__ == "__main__":
    wav_file = sys.argv[1] if len(sys.argv) > 1 else "acoustic_tx.wav"
    print(f"[Acoustic RX] Processing WAV file: '{wav_file}'...")
    
    success, message, payload = AcousticRxDecoder.decode_wav(wav_file)
    if success:
        print(f"[Acoustic RX] SUCCESS: {message}")
        print(f"[Acoustic RX] Decoded Text Payload: '{payload.decode(errors='ignore')}'")
    else:
        print(f"[Acoustic RX] ERROR: {message}")
