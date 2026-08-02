import numpy as np
import receiver
import os

def calculate_ber():
    np.random.seed(42)
    tx_bits = np.random.randint(0, 2, 128)
    
    target_file = "phoneserve_packet.wav"
    if not os.path.exists(target_file):
        print("Error: Record a packet first.")
        return
        
    audio_data = receiver.load_wav(target_file)
    rx_bits = receiver.demodulate_audio_to_bits(audio_data)
    rx_bits = rx_bits[:128]
    
    if len(rx_bits) < 128:
        rx_bits = np.pad(rx_bits, (0, 128 - len(rx_bits)), 'constant')

    errors = np.sum(tx_bits != rx_bits)
    ber = errors / 128.0
    
    print("\n==========================================")
    print("         DPSK LINK INTEGRITY REPORT       ")
    print("==========================================")
    print(f"Transmitted Bits: {len(tx_bits)}")
    print(f"Recovered Bits:   {len(rx_bits)}")
    print(f"Confirmed Errors: {errors}")
    print(f"True Bit Error Rate: {ber * 100:.2f}%")
    print("==========================================")
    
    if ber < 0.05:
        print("🎉 CRUSHED IT: Absolute phase tracking achieved over the air!")
    elif ber < 0.15:
        print("👍 PASSING LINK: Minor acoustic noise detected, ready for networking layer.")
    else:
        print("⚠️ HIGH NOISE: Check volume levels or mechanical obstructions.")

if __name__ == "__main__":
    calculate_ber()
