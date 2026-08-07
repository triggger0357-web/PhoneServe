import asyncio
import json
from web3 import Web3
from eth_account import Account

RPC_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
SESSION_PRIVATE_KEY = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

CONTRACT_ABI = json.loads('''[
    {"inputs":[{"internalType":"address","name":"soulOwner","type":"address"}],"name":"getAgentState","outputs":[{"components":[{"internalType":"uint8","name":"tier","type":"uint8"},{"internalType":"uint32","name":"level","type":"uint32"},{"internalType":"uint64","name":"xp","type":"uint64"},{"internalType":"bytes32","name":"memoryIpfsHash","type":"bytes32"},{"internalType":"uint256","name":"dailyAllowanceWei","type":"uint256"},{"internalType":"uint256","name":"spentTodayWei","type":"uint256"},{"internalType":"uint256","name":"lastResetTimestamp","type":"uint256"}],"internalType":"struct ISoulForgeAI.AgentState","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"address","name":"soulOwner","type":"address"}],"name":"getCapabilities","outputs":[{"components":[{"internalType":"bool","name":"legalTriageEnabled","type":"bool"},{"internalType":"bool","name":"yieldAutoClaimEnabled","type":"bool"},{"internalType":"bool","name":"proxyRoutingEnabled","type":"bool"},{"internalType":"bool","name":"highComputeAccess","type":"bool"}],"internalType":"struct ISoulForgeAI.CapabilityFlags","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"bytes32","name":"newHash","type":"bytes32"}],"name":"updateMemoryHash","outputs":[],"stateMutability":"nonpayable","type":"function"}
]''')

class SoulForgeRuntimeBridge:
    def __init__(self, rpc_url, contract_address, session_key):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(session_key)
        self.contract = self.w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
        self.soul_owner = self.account.address

    def sync_onchain_capabilities(self):
        try:
            caps = self.contract.functions.getCapabilities(self.soul_owner).call()
            state = self.contract.functions.getAgentState(self.soul_owner).call()
            return {
                "tier": state[0],
                "level": state[1],
                "xp": state[2],
                "memory_hash": state[3].hex(),
                "legal_enabled": caps[0],
                "yield_claim_enabled": caps[1],
                "proxy_enabled": caps[2],
                "high_compute_enabled": caps[3]
            }
        except Exception as e:
            print(f"[Error] Failed to fetch on-chain state: {e}")
            return None

    def execute_legal_triage_query(self, user_query):
        capabilities = self.sync_onchain_capabilities()
        if not capabilities or not capabilities["legal_enabled"]:
            return {
                "status": "DENIED",
                "reason": "Legal Triage module not unlocked in Soul Forge ID."
            }

        model_type = "Cloud-LLM-HighReasoning" if capabilities["high_compute_enabled"] else "Local-3B-Quantized"
        print(f"[AI Agent] Routing legal triage via {model_type}...")
        return {
            "status": "SUCCESS",
            "engine": model_type,
            "response": "Legal intake processed. Informational disclaimer attached."
        }

if __name__ == "__main__":
    bridge = SoulForgeRuntimeBridge(RPC_URL, CONTRACT_ADDRESS, SESSION_PRIVATE_KEY)
    print("Fetching active Soul Forge AI permissions...")
    caps = bridge.sync_onchain_capabilities()
    print("Capabilities State:", caps)
    result = bridge.execute_legal_triage_query("What are the basic landlord notice periods?")
    print("Execution Result:", result)
