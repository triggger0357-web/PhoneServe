import asyncio
import json
import hashlib
import time
import random
from websockets.server import serve

class MultiStringMinerDaemon:
    def __init__(self):
        this_timestamp = time.time()
        self.unclaimed_balance = 14.829104
        self.base_rate_per_sec = 0.000038
        self.mined_strings_count = 0
        
        # String Mining Rate Multipliers
        self.string_rates = {
            "telecom_sms": 0.0002,
            "telecom_voice": 0.0020,
            "proxy_bandwidth": 0.0005,
            "ai_compute": 0.0010,
            "acoustic_sound": 0.0015
        }

    def generate_block_proof(self, string_type, payload_data):
        """Generates a cryptographic hash proof for a mined data string."""
        raw_string = f"{string_type}:{payload_data}:{time.time()}"
        block_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        self.mined_strings_count += 1
        return block_hash

    async def simulate_mining_events(self):
        """Simulates background multi-string data mining activity."""
        string_types = list(self.string_rates.keys())
        while True:
            await asyncio.sleep(2)
            active_string = random.choice(string_types)
            payload = f"bytes_{random.randint(100, 9999)}"
            proof = self.generate_block_proof(active_string, payload)
            
            # Increment balance based on mined string type
            reward = self.string_rates[active_string]
            self.unclaimed_balance += reward
            
            print(f"[Miner] Mined {active_string} string | Proof: {proof[:12]}... | +${reward:.6f}")

    async def ws_handler(self, websocket):
        """Broadcasts real-time mining state to front-end WebSocket clients."""
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
                await asyncio.sleep(0.1) # 10Hz ticker updates
        except Exception:
            print("[WebSocket] Client disconnected.")

async def main():
    miner = MultiStringMinerDaemon()
    
    # Run mining loop and WebSocket server concurrently
    asyncio.create_task(miner.simulate_mining_events())
    
    print("[Value Engine] Multi-String Daemon starting on ws://127.0.0.1:8080...")
    async with serve(miner.ws_handler, "127.0.0.1", 8080):
        await asyncio.Future()  # Keep server alive

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Value Engine] Multi-String Daemon stopped.")
