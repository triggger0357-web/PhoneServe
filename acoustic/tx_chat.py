import numpy as np
import modulator
import fec
import os
import sys

def text_to_bits(text):
    bits = []
    for char in text:
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return np.array(bits, dtype=np.int16)

def main():
    print("==================================================")
    print("   PhoneServe Interleaved Acoustic Transmitter   ")
    print("==================================================")
    print("Enter text. Shuffling bits to neutralize burst noise...")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            msg = input("PhoneServe_Mesh_TX> ")
            if msg.strip().lower() == 'exit':
                print("Closing transmitter shell.")
                break
            if not msg:
                continue
                
            raw_bits = text_to_bits(msg)
            fec_bitstream = fec.bits_to_fec_stream(raw_bits)
            interleaved_stream = fec.interleave(fec_bitstream)
            
            print(f"Encoding payload: {len(raw_bits)} bits -> {len(fec_bitstream)} FEC bits -> {len(interleaved_stream)} Scrambled bits.")
            
            waveform = modulator.modulate_bits_to_bfsk(interleaved_stream)
            modulator.save_wav(waveform, "phoneserve_packet.wav")
            
            print("Broadcasting burst-resilient acoustic stream...")
            os.system("play-audio phoneserve_packet.wav")
            print("Broadcast complete.\n")
            
        except KeyboardInterrupt:
            print("\nExiting safely.")
            sys.exit(0)

if __name__ == "__main__":
    main()
