import asyncio
import json
import hashlib
import time
import random
import struct
import numpy as np
from websockets.server import serve

class AcousticFrameVerifier:
    """
    Goertzel tone analysis and CRC16 frame verification for live PCM streams.
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
        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        if len(data) < samples_per_symbol * 10:
            return None

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


class MultiStringMinerDaemon:
    def __init__(self):
        self.unclaimed_balance = 14.829104
        self.base_rate_per_sec = 0.000038
        self.mined_strings_count = 0
        
        self.string_rates = {
            "telecom_sms": 0.0002,
            "telecom_voice": 0.0020,
            "proxy_bandwidth": 0.0005,
            "ai_compute": 0.0010,
            "acoustic_sound": 0.0015
        }

    def mint_acoustic_reward(self, payload: bytes):
        raw_token = f"acoustic:{payload.hex()}:{time.time()}"
        block_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        reward = self.string_rates["acoustic_sound"]
        
        self.unclaimed_balance += reward
        self.mined_strings_count += 1
        
        print(f"\n[Acoustic Mic Auto-Mint] Verified Payload: '{payload.decode(errors='ignore')}' | Hash: {block_hash[:12]}... | +${reward:.6f}")
        return block_hash

    async def live_acoustic_listener(self):
        """Asynchronous background worker capturing mic input via SoX stdout stream."""
        cmd = ["rec", "-q", "-t", "raw", "-r", "44100", "-e", "signed-integer", "-b", "16", "-c", "1", "-"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL
            )
            print("[Acoustic Mic Listener] Active in background (SoX -> asyncio pipe).")
        except Exception as e:
            print(f"[Acoustic Mic Listener] Warning: Could not execute SoX rec process ({e}). Live capture disabled.")
            return

        buffer = np.array([], dtype=np.float32)
        chunk_size = 1024 * 2  # 1024 int16 samples (~23ms chunk)

        try:
            while True:
                raw = await proc.stdout.read(chunk_size)
                if not raw:
                    await asyncio.sleep(0.01)
                    continue

                chunk_int16 = np.frombuffer(raw, dtype=np.int16)
                chunk_float = chunk_int16.astype(np.float32) / 32768.0
                buffer = np.append(buffer, chunk_float)

                max_samples = 44100 * 2
                if len(buffer) > max_samples:
                    buffer = buffer[-max_samples:]

                payload = AcousticFrameVerifier.process_buffer(buffer)
                if payload:
                    self.mint_acoustic_reward(payload)
                    buffer = np.array([], dtype=np.float32)

                await asyncio.sleep(0.001)

        except asyncio.CancelledError:
            proc.terminate()
            await proc.wait()
            print("[Acoustic Mic Listener] Stream stopped.")

    def generate_simulated_proof(self, string_type):
        raw_string = f"{string_type}:{random.randint(1000,9999)}:{time.time()}"
        block_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        reward = self.string_rates[string_type]
        self.unclaimed_balance += reward
        self.mined_strings_count += 1
        return block_hash

    async def simulate_mining_events(self):
        """Simulates non-acoustic multi-string telemetry background events."""
        string_types = ["telecom_sms", "telecom_voice", "proxy_bandwidth", "ai_compute"]
        
        while True:
            await asyncio.sleep(3)
            active_string = random.choice(string_types)
            proof = self.generate_simulated_proof(active_string)
            reward = self.string_rates[active_string]
            print(f"[Miner] Mined {active_string} string | Proof: {proof[:12]}... | +${reward:.6f}")

    async def ws_handler(self, websocket):
        """Broadcasts real-time mining telemetry to dashboard UI."""
        print("[WebSocket] Dashboard client connected.")
        try:
            while True:
                payload = {
                    "timestamp": time.time(),
                    "user_unclaimed_balance_usd": round(self.unclaimed_balance, 6),
                    "user_current_rate_per_sec": round(self.base_rate_per_sec, 6),
                    "mined_strings_count": self.mined_strings_count,
                    "active_services": ["sms", "voice", "proxy", "ai", "acoustic"]
                }
                await websocket.send(json.dumps(payload))
                await asyncio.sleep(0.1)
        except Exception:
            print("[WebSocket] Client disconnected.")

async def main():
    miner = MultiStringMinerDaemon()
    
    # Spawn background tasks concurrently
    asyncio.create_task(miner.live_acoustic_listener())
    asyncio.create_task(miner.simulate_mining_events())
    
    print("[Value Engine] Multi-String Daemon listening on ws://127.0.0.1:8080...")
    async with serve(miner.ws_handler, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Value Engine] Stopped.")
