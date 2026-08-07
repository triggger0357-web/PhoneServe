import wave
import numpy as np
import struct
import sys

class AcousticRxDecoder:
    """
    Decodes BFSK acoustic WAV files using vectorized single-bin DFT tone power matrix operations.
    Detects 0xAC01 magic header, extracts payload, and verifies CRC16.
    Uses pure NumPy and standard library wave module (Zero SciPy dependencies).
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
    def read_wav_file(cls, wav_path: str):
        """Reads WAV file samples into float32 array using standard library wave module."""
        with wave.open(wav_path, 'rb') as wav_in:
            sr = wav_in.getframerate()
            n_channels = wav_in.getnchannels()
            sampwidth = wav_in.getsampwidth()
            n_frames = wav_in.getnframes()
            raw_bytes = wav_in.readframes(n_frames)

            if sampwidth == 2:
                raw_data = np.frombuffer(raw_bytes, dtype=np.int16)
                data = raw_data.astype(np.float32) / 32768.0
            elif sampwidth == 4:
                raw_data = np.frombuffer(raw_bytes, dtype=np.int32)
                data = raw_data.astype(np.float32) / 2147483648.0
            else:
                raw_data = np.frombuffer(raw_bytes, dtype=np.uint8)
                data = (raw_data.astype(np.float32) - 128.0) / 128.0

            if n_channels > 1:
                data = data[::n_channels]

            return sr, data

    @classmethod
    def compute_tone_powers_vectorized(cls, chunks: np.ndarray, freqs: list) -> np.ndarray:
        """
        Vectorized Goertzel/DFT power filter using BLAS matrix multiplication.
        chunks: np.ndarray of shape (N_chunks, N_samples)
        freqs: list of target frequencies [f1, f2, ...]
        returns: np.ndarray of shape (N_chunks, len(freqs)) containing spectral powers
        """
        if chunks.ndim == 1:
            chunks = chunks.reshape(1, -1)

        N_samples = chunks.shape[1]
        t = np.arange(N_samples) / cls.SAMPLE_RATE
        angles = 2.0 * np.pi * np.outer(t, freqs) # Shape: (N_samples, len(freqs))
        
        cos_mat = np.cos(angles)
        sin_mat = np.sin(angles)
        
        real = chunks @ cos_mat   # Shape: (N_chunks, len(freqs))
        imag = chunks @ sin_mat   # Shape: (N_chunks, len(freqs))
        return (real * real) + (imag * imag)

    @classmethod
    def decode_wav(cls, wav_path: str):
        sr, data = cls.read_wav_file(wav_path)
        if sr != cls.SAMPLE_RATE:
            raise ValueError(f"Sample rate mismatch: expected {cls.SAMPLE_RATE} Hz, got {sr} Hz")

        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)

        # 1. Vectorized Sliding Scan for Preamble Synchronization
        scan_step = 44  # ~1ms sliding window steps
        indices = np.arange(0, len(data) - samples_per_symbol, scan_step)
        if len(indices) == 0:
            return False, "Audio file too short", b""

        # Create 2D strided matrix of sliding windows without memory copies
        sliding_chunks = np.lib.stride_tricks.sliding_window_view(data, window_shape=samples_per_symbol)[::scan_step]
        
        # Calculate powers for [PREAMBLE, MARK, SPACE] across all windows simultaneously in BLAS
        target_freqs = [cls.FREQ_PREAMBLE, cls.FREQ_MARK, cls.FREQ_SPACE]
        powers = cls.compute_tone_powers_vectorized(sliding_chunks, target_freqs)
        
        p_preamble = powers[:, 0]
        p_mark = powers[:, 1]
        p_space = powers[:, 2]

        preamble_mask = (p_preamble > 50.0) & (p_preamble > (p_mark + p_space) * 2)
        preamble_end_idx = 0
        in_preamble = False

        for i, is_pre in enumerate(preamble_mask):
            if is_pre:
                in_preamble = True
            elif in_preamble:
                preamble_end_idx = indices[i]
                break

        if preamble_end_idx == 0:
            return False, "Preamble sync tone (3000 Hz) not detected", b""

        # 2. Extract symbol chunks starting from synchronized preamble end
        symbol_indices = np.arange(preamble_end_idx, len(data) - samples_per_symbol + 1, samples_per_symbol)
        if len(symbol_indices) == 0:
            return False, "No data symbols found after preamble", b""

        symbol_chunks = np.array([data[idx : idx + samples_per_symbol] for idx in symbol_indices])
        symbol_powers = cls.compute_tone_powers_vectorized(symbol_chunks, [cls.FREQ_MARK, cls.FREQ_SPACE])

        m_power = symbol_powers[:, 0]
        s_power = symbol_powers[:, 1]

        bits = []
        for p_m, p_s in zip(m_power, s_power):
            if p_m < 0.5 and p_s < 0.5:
                break
            bits.append(1 if p_m >= p_s else 0)

        # 3. Locate Magic Header (0xAC01) in bitstream
        decoded_bytes = bytearray()
        for offset in range(len(bits) - 16):
            byte1, byte2 = 0, 0
            for i in range(8):
                byte1 = (byte1 << 1) | bits[offset + i]
                byte2 = (byte2 << 1) | bits[offset + 8 + i]

            if bytes([byte1, byte2]) == cls.MAGIC_HEADER:
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
    print(f"[Acoustic RX Vectorized] Processing WAV file: '{wav_file}'...")
    
    success, message, payload = AcousticRxDecoder.decode_wav(wav_file)
    if success:
        print(f"[Acoustic RX] SUCCESS: {message}")
        print(f"[Acoustic RX] Decoded Text Payload: '{payload.decode(errors='ignore')}'")
    else:
        print(f"[Acoustic RX] ERROR: {message}")
