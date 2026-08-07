import numpy as np
import struct
import subprocess
import sys
import time

class LiveAcousticRxDecoder:
    """
    Decodes live BFSK audio streams from a rolling buffer using Goertzel tone filters.
    """
    MAGIC_HEADER = b'\xac\x01'
    SAMPLE_RATE = 44100       # Hz
    FREQ_MARK = 2400.0        # Hz (Bit 1)
    FREQ_SPACE = 1800.0       # Hz (Bit 0)
    FREQ_PREAMBLE = 3000.0    # Hz (Sync Tone)
    SYMBOL_DURATION = 0.010   # 10ms (441 samples @ 44.1kHz)

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
        N = len(samples)
        if N == 0:
            return 0.0
        k = int(0.5 + (N * target_freq) / cls.SAMPLE_RATE)
        w = (2.0 * np.pi / N) * k
        coeff = 2.0 * np.cos(w)
        
        q1, q2 = 0.0, 0.0
        for sample in samples:
            q0 = coeff * q1 - q2 + sample
            q2 = q1
            q1 = q0
            
        real = q1 - q2 * np.cos(w)
        imag = q2 * np.sin(w)
        return (real * real) + (imag * imag)

    @classmethod
    def process_buffer(cls, data: np.ndarray):
        """Scans floating-point PCM audio buffer for acoustic frames."""
        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        if len(data) < samples_per_symbol * 10:
            return None

        # 1. Detect Preamble (3000 Hz)
        scan_step = 44  # ~1ms sliding window steps
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

        if preamble_end_idx == 0:
            return None

        # 2. Extract Bits
        bits = []
        curr = preamble_end_idx
        while curr + samples_per_symbol <= len(data):
            chunk = data[curr : curr + samples_per_symbol]
            p_mark = cls.goertzel_filter(chunk, cls.FREQ_MARK)
            p_space = cls.goertzel_filter(chunk, cls.FREQ_SPACE)

            if p_mark < 0.5 and p_space < 0.5:
                break

            bits.append(1 if p_mark >= p_space else 0)
            curr += samples_per_symbol

        # 3. Locate Magic Header 0xAC01
        decoded_bytes = bytearray()
        for offset in range(len(bits) - 16):
            b1, b2 = 0, 0
            for i in range(8):
                b1 = (b1 << 1) | bits[offset + i]
                b2 = (b2 << 1) | bits[offset + 8 + i]

            if bytes([b1, b2]) == cls.MAGIC_HEADER:
                for b_idx in range(offset, len(bits) - 7, 8):
                    val = 0
                    for i in range(8):
                        val = (val << 1) | bits[b_idx + i]
                    decoded_bytes.append(val)
                break

        if len(decoded_bytes) < 5:
            return None

        payload_len = decoded_bytes[2]
        total_frame_len = 3 + payload_len + 2
        if len(decoded_bytes) < total_frame_len:
            return None

        frame_data = bytes(decoded_bytes[:total_frame_len])
        raw_content = frame_data[:3 + payload_len]
        received_crc = struct.unpack('<H', frame_data[3 + payload_len : total_frame_len])[0]
        computed_crc = cls.calculate_crc16(raw_content)

        if received_crc == computed_crc:
            return frame_data[3 : 3 + payload_len]
        return None


def stream_sox():
    """Captures mic audio stream using SoX (rec) in Termux stdout."""
    cmd = ["rec", "-q", "-t", "raw", "-r", "44100", "-e", "signed-integer", "-b", "16", "-c", "1", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    buffer = np.array([], dtype=np.float32)
    chunk_bytes = 1024 * 2  # 1024 int16 samples (~23ms)
    
    print("[Acoustic RX Live] Listening on microphone (SoX stream)... Press Ctrl+C to stop.")
    
    try:
        while True:
            raw = proc.stdout.read(chunk_bytes)
            if not raw:
                break
            
            chunk_int16 = np.frombuffer(raw, dtype=np.int16)
            chunk_float = chunk_int16.astype(np.float32) / 32768.0
            buffer = np.append(buffer, chunk_float)
            
            # Maintain a 2-second rolling buffer
            max_samples = 44100 * 2
            if len(buffer) > max_samples:
                buffer = buffer[-max_samples:]
            
            payload = LiveAcousticRxDecoder.process_buffer(buffer)
            if payload:
                print(f"\n[Acoustic RX] >>> PACKET VERIFIED: '{payload.decode(errors='ignore')}' <<<")
                buffer = np.array([], dtype=np.float32)
                
    except KeyboardInterrupt:
        print("\n[Acoustic RX Live] Stopped.")
    finally:
        proc.terminate()

def stream_pyaudio():
    """Captures mic audio stream using PyAudio (for standard Linux environments)."""
    import pyaudio
    
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )
    
    buffer = np.array([], dtype=np.float32)
    print("[Acoustic RX Live] Listening on microphone (PyAudio stream)... Press Ctrl+C to stop.")
    
    try:
        while True:
            raw = stream.read(1024, exception_on_overflow=False)
            chunk_int16 = np.frombuffer(raw, dtype=np.int16)
            chunk_float = chunk_int16.astype(np.float32) / 32768.0
            buffer = np.append(buffer, chunk_float)
            
            max_samples = 44100 * 2
            if len(buffer) > max_samples:
                buffer = buffer[-max_samples:]
                
            payload = LiveAcousticRxDecoder.process_buffer(buffer)
            if payload:
                print(f"\n[Acoustic RX] >>> PACKET VERIFIED: '{payload.decode(errors='ignore')}' <<<")
                buffer = np.array([], dtype=np.float32)
                
    except KeyboardInterrupt:
        print("\n[Acoustic RX Live] Stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sox"
    if mode == "pyaudio":
        stream_pyaudio()
    else:
        stream_sox()
