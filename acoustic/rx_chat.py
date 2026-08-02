import os
import numpy as np
import receiver
import fec

def bits_to_text(bits):
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i : i + 8]
        if len(byte_bits) < 8:
            break
        byte_str = "".join(str(b) for b in byte_bits)
        bytes_list.append(int(byte_str, 2))
        
    raw_text = bytes(bytes_list).decode('ascii', errors='replace')
    return raw_text.replace('\x00', '')

def main():
    target_file = "phoneserve_packet.wav"
    if not os.path.exists(target_file):
        print("Error: Target 'phoneserve_packet.wav' not found.")
        return
        
    audio_data = receiver.load_wav(target_file)
    rx_bits = receiver.demodulate_audio_to_bits(audio_data)
    
    if len(rx_bits) == 0:
        print("Error: No bitstream data recovered from stream.")
        return
        
    unshuffled_bits = fec.deinterleave(rx_bits)
    decoded_bits, corrected_errors = fec.fec_stream_to_bits(unshuffled_bits)
    decoded_message = bits_to_text(decoded_bits)
    
    print("\n==================================================")
    print(f"📩 MESH DECODER: Burst-Corrected Report")
    print("==================================================")
    print(f"Total Bit Positions Untangled: {len(rx_bits)}")
    print(f"Healed Burst Bit Flips:        {corrected_errors} errors cleanly auto-corrected")
    print(f"--> {decoded_message}")
    print("==================================================")

if __name__ == "__main__":
    main()
