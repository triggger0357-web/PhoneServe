import asyncio
import json
import hashlib
import time
import random
import struct
from websockets.server import serve

class AcousticFrameVerifier:
    """
    Parses and verifies data-over-sound acoustic packet frames.
    Frame Structure:
    [2-Byte Header: 0xAC01] + [1-Byte Length] + [N-Byte Payload] + [2-Byte CRC16 Checksum]
    """
    MAGIC_HEADER = b'\xac\x01'

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
    def create_frame(cls, payload: bytes) -> bytes:
        header_and_len = cls.MAGIC_HEADER + bytes([len(payload)])
        raw = header_and_len + payload
        checksum = cls.calculate_crc16(raw)
        return raw + struct.pack('<H', checksum)

    @classmethod
    def verify_frame(cls, frame_bytes: bytes):
        if len(frame_bytes) < 5:
            return False, "Frame truncated (< 5 bytes)", b""
        
        if frame_bytes[:2] != cls.MAGIC_HEADER:
            return False, "Invalid acoustic magic header (expected 0xAC01)", b""
        
        payload_len = frame_bytes[2]
        expected_len = 3 + payload_len + 2
        if len(frame_bytes) < expected_len:
            return False, f"Incomplete payload (expected {expected_len} bytes)", b""

        raw_content = frame_bytes[:3 + payload_len]
        received_crc = struct.unpack('<H', frame_bytes[3 + payload_len : expected_len])[0]
        computed_crc = cls.calculate_crc16(raw_content)

        if received_crc != computed_crc:
            return False, f"CRC mismatch: expected {hex(computed_crc)}, got {hex(received_crc)}", b""

        payload = frame_bytes[3 : 3 + payload_len]
        return True, "CRC16 Verified", payload


class MultiStringMinerDaemon:
    def __init__(self):
        self.unclaimed_balance = 14.829104
        self.base_rate_per_sec = 0.000038
        self.mined_strings_count = 0
        
        # String Mining Micro-Rewards
        self.string_rates = {
            "telecom_sms": 0.0002,
            "telecom_voice": 0.0020,
            "proxy_bandwidth": 0.0005,
            "ai_compute": 0.0010,
            "acoustic_sound": 0.0015
        }

    def process_acoustic_string(self, raw_frame_bytes: bytes):
        """Verifies an incoming acoustic packet and calculates PoUW string proof."""
        valid, reason, payload = AcousticFrameVerifier.verify_frame(raw_frame_bytes)
        
        if not valid:
            print(f"[Acoustic] Packet rejection: {reason}")
            return None

        # Hash verified payload + timestamp into Proof of Useful Work (PoUW) string
        raw_token = f"acoustic:{payload.hex()}:{time.time()}"
        block_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        
        reward = self.string_rates["acoustic_sound"]
        self.unclaimed_balance += reward
        self.mined_strings_count += 1
        
        print(f"[Acoustic] Verified 0xAC01 Frame | Payload: '{payload.decode(errors='ignore')}' | Hash: {block_hash[:12]}... | +${reward:.6f}")
        return block_hash

    def generate_simulated_proof(self, string_type):
        raw_string = f"{string_type}:{random.randint(1000,9999)}:{time.time()}"
        block_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        reward = self.string_rates[string_type]
        self.unclaimed_balance += reward
        self.mined_strings_count += 1
        return block_hash

    async def simulate_mining_events(self):
        """Simulates incoming multi-string events including valid acoustic data bursts."""
        string_types = ["telecom_sms", "telecom_voice", "proxy_bandwidth", "ai_compute", "acoustic_sound"]
        
        while True:
            await asyncio.sleep(2)
            active_string = random.choice(string_types)
            
            if active_string == "acoustic_sound":
                # Generate valid acoustic binary frame
                sample_payload = f"tx_sound_pkt_{random.randint(100, 999)}".encode('utf-8')
                frame = AcousticFrameVerifier.create_frame(sample_payload)
                self.process_acoustic_string(frame)
            else:
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
    asyncio.create_task(miner.simulate_mining_events())
    
    print("[Value Engine] Multi-String Daemon listening on ws://127.0.0.1:8080...")
    async with serve(miner.ws_handler, "127.0.0.1", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Value Engine] Stopped.")
