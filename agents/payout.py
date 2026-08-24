import os
from web3 import Web3

# Configure Web3 RPC (e.g., Polygon Mainnet / Amoy Testnet)
RPC_URL = os.getenv("WEB3_RPC_URL", "https://polygon-rpc.com")
PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY", "") # Your node sender private key
RECEIVER_ADDRESS = os.getenv("DESTINATION_WALLET", "") # Your destination wallet address

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def send_crypto_payout(to_address, amount_in_wei):
    """Executes an on-chain transfer from node account to user wallet."""
    if not w3.is_connected() or not PRIVATE_KEY:
        print("[Wallet Engine] Web3 RPC not configured or no private key set. Running local mock transfer.")
        return None

    try:
        sender_account = w3.eth.account.from_key(PRIVATE_KEY)
        nonce = w3.eth.get_transaction_count(sender_account.address)

        tx = {
            'nonce': nonce,
            'to': w3.to_checksum_address(to_address),
            'value': amount_in_wei,
            'gas': 21000,
            'maxFeePerGas': w3.to_wei('50', 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),
            'chainId': w3.eth.chain_id
        }

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[Wallet Engine] On-chain Transfer Sent! Tx Hash: {tx_hash.hex()}")
        return tx_hash.hex()
    except Exception as e:
        print(f"[Wallet Engine] Transaction Failed: {e}")
        return None
