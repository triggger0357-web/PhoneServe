import asyncio
import json
import hashlib
import time
import random
import struct
import os
import threading
import http.server
import socketserver
import numpy as np

try:
    from websockets.asyncio.server import serve
except ImportError:
    from websockets.server import serve


# ==========================================
# 1. Background HTTP Static Web Server Thread
# ==========================================
def start_http_server(port=8000):
    class ReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    handler = http.server.SimpleHTTPRequestHandler
    try:
        with ReuseTCPServer(("127.0.0.1", port), handler) as httpd:
            print(f"[HTTP Server] Hosting UI at http://127.0.0.1:{port}/admin.html")
            httpd.serve_forever()
    except Exception as e:
        print(f"[HTTP Server] Error starting server on port {port}: {e}")


# ==========================================
# 2. Vectorized Acoustic Decoder Engine
# ==========================================
class AcousticFrameVerifier:
    MAGIC_HEADER = b'\xac\x01'
    SAMPLE_RATE = 44100
    FREQ_MARK = 2400.0
    FREQ_SPACE = 1800.0
    FREQ_PREAMBLE = 3000.0
    SYMBOL_DURATION = 0.010

    PREAMBLE_THRESH = float(os.getenv("ACOUSTIC_PREAMBLE_THRESH", "5.0"))
    SYMBOL_THRESH = float(os.getenv("ACOUSTIC_SYMBOL_THRESH", "0.05"))

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
    def compute_tone_powers_vectorized(cls, chunks: np.ndarray, freqs: list) -> np.ndarray:
        if chunks.ndim == 1:
            chunks = chunks.reshape(1, -1)

        N_samples = chunks.shape[1]
        t = np.arange(N_samples) / cls.SAMPLE_RATE
        angles = 2.0 * np.pi * np.outer(t, freqs)
        
        cos_mat = np.cos(angles)
        sin_mat = np.sin(angles)
        
        real = chunks @ cos_mat
        imag = chunks @ sin_mat
        return (real * real) + (imag * imag)

    @classmethod
    def process_buffer(cls, data: np.ndarray):
        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        if len(data) < samples_per_symbol * 10:
            return None

        scan_step = 44
        max_start = len(data) - samples_per_symbol
        if max_start <= 0:
            return None

        indices = np.arange(0, max_start, scan_step)
        if len(indices) == 0:
            return None

        sliding_chunks = np.lib.stride_tricks.sliding_window_view(data, window_shape=samples_per_symbol)[::scan_step]
        powers = cls.compute_tone_powers_vectorized(sliding_chunks, [cls.FREQ_PREAMBLE, cls.FREQ_MARK, cls.FREQ_SPACE])
        
        p_preamble, p_mark, p_space = powers[:, 0], powers[:, 1], powers[:, 2]
        preamble_mask = (p_preamble > cls.PREAMBLE_THRESH) & (p_preamble > (p_mark + p_space) * 2)
        preamble_end_idx = 0
        in_preamble = False

        for i, is_pre in enumerate(preamble_mask):
            if is_pre:
                in_preamble = True
            elif in_preamble:
                preamble_end_idx = indices[i]
                break

        if preamble_end_idx == 0:
            return None

        symbol_indices = np.arange(preamble_end_idx, len(data) - samples_per_symbol + 1, samples_per_symbol)
        if len(symbol_indices) == 0:
            return None

        symbol_chunks = np.array([data[idx : idx + samples_per_symbol] for idx in symbol_indices])
        symbol_powers = cls.compute_tone_powers_vectorized(symbol_chunks, [cls.FREQ_MARK, cls.FREQ_SPACE])

        m_power, s_power = symbol_powers[:, 0], symbol_powers[:, 1]
        bits = []
        for p_m, p_s in zip(m_power, s_power):
            if p_m < cls.SYMBOL_THRESH and p_s < cls.SYMBOL_THRESH:
                break
            bits.append(1 if p_m >= p_s else 0)

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


# ==========================================
# 3. Telemetry Daemon & WebSocket Server
# ==========================================
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
        print(f"\n[Acoustic Mic Auto-Mint] Verified: '{payload.decode(errors='ignore')}' | Hash: {block_hash[:12]}... | +${reward:.6f}")
        return block_hash

    async def live_acoustic_listener(self):
        cmd = ["rec", "-q", "-t", "raw", "-r", "44100", "-e", "signed-integer", "-b", "16", "-c", "1", "-"]
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
            print(f"[Acoustic Listener] Active on Mic (Preamble Thresh: {AcousticFrameVerifier.PREAMBLE_THRESH}).")
        except Exception as e:
            print(f"[Acoustic Listener] SoX rec process unavailable ({e}). Passive mode.")
            return

        buffer = np.array([], dtype=np.float32)
        chunk_size = 1024 * 2

        try:
            while True:
                raw = await proc.stdout.read(chunk_size)
                if not raw:
                    await asyncio.sleep(0.01)
                    continue

                chunk_int16 = np.frombuffer(raw, dtype=np.int16)
                buffer = np.append(buffer, chunk_int16.astype(np.float32) / 32768.0)

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

    async def simulate_mining_events(self):
        string_types = ["telecom_sms", "telecom_voice", "proxy_bandwidth", "ai_compute"]
        while True:
            await asyncio.sleep(3)
            active_string = random.choice(string_types)
            proof = hashlib.sha256(f"{active_string}:{time.time()}".encode()).hexdigest()
            reward = self.string_rates[active_string]
            self.unclaimed_balance += reward
            self.mined_strings_count += 1
            print(f"[Miner] Mined {active_string} | Proof: {proof[:12]}... | +${reward:.6f}")

    async def ws_handler(self, websocket):
        print("[WebSocket] Client connected.")
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


# ==========================================
# 4. Entrypoint
# ==========================================
async def main():
    # Start HTTP server in a background daemon thread
    http_thread = threading.Thread(target=start_http_server, args=(8000,), daemon=True)
    http_thread.start()

    miner = MultiStringMinerDaemon()
    asyncio.create_task(miner.live_acoustic_listener())
    asyncio.create_task(miner.simulate_mining_events())

    print("[Value Engine] Multi-String Daemon listening on ws://127.0.0.1:8080...")
    async with serve(miner.ws_handler, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Unified Server] Gracefully stopped.")
