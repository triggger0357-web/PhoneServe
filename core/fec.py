import numpy as np

def encode_hamming74(d):
    p0 = d[0] ^ d[1] ^ d[3]
    p1 = d[0] ^ d[2] ^ d[3]
    p2 = d[1] ^ d[2] ^ d[3]
    return [p0, p1, d[0], p2, d[1], d[2], d[3]]

def decode_hamming74(r):
    s0 = r[0] ^ r[2] ^ r[4] ^ r[6]
    s1 = r[1] ^ r[2] ^ r[5] ^ r[6]
    s2 = r[3] ^ r[4] ^ r[5] ^ r[6]
    
    syndrome = s0 + (s1 << 1) + (s2 << 2)
    r_corrected = list(r)
    
    if syndrome != 0:
        r_corrected[syndrome - 1] ^= 1
        
    return [r_corrected[2], r_corrected[4], r_corrected[5], r_corrected[6]]

def bits_to_fec_stream(bitstream):
    fec_bits = []
    for i in range(0, len(bitstream), 4):
        chunk = bitstream[i:i+4]
        if len(chunk) < 4:
            chunk = np.pad(chunk, (0, 4 - len(chunk)), 'constant')
        fec_bits.extend(encode_hamming74(chunk))
    return np.array(fec_bits, dtype=np.int16)

def fec_stream_to_bits(fec_stream):
    decoded_bits = []
    corrected_count = 0
    for i in range(0, len(fec_stream), 7):
        chunk = fec_stream[i:i+7]
        if len(chunk) < 7:
            break
            
        s0 = chunk[0] ^ chunk[2] ^ chunk[4] ^ chunk[6]
        s1 = chunk[1] ^ chunk[2] ^ chunk[5] ^ chunk[6]
        s2 = chunk[3] ^ chunk[4] ^ chunk[5] ^ chunk[6]
        if (s0 + (s1 << 1) + (s2 << 2)) != 0:
            corrected_count += 1
            
        decoded_bits.extend(decode_hamming74(chunk))
    return np.array(decoded_bits, dtype=np.int16), corrected_count

def interleave(bitstream):
    BLOCK_SIZE = 112
    ROWS = 7
    COLS = 16
    rem = len(bitstream) % BLOCK_SIZE
    if rem != 0:
        bitstream = np.pad(bitstream, (0, BLOCK_SIZE - rem), 'constant')
        
    interleaved = []
    for b in range(0, len(bitstream), BLOCK_SIZE):
        block = bitstream[b:b+BLOCK_SIZE]
        matrix = block.reshape(ROWS, COLS)
        interleaved.extend(matrix.flatten(order='F'))
    return np.array(interleaved, dtype=np.int16)

def deinterleave(bitstream):
    BLOCK_SIZE = 112
    ROWS = 7
    COLS = 16
    deinterleaved = []
    for b in range(0, len(bitstream), BLOCK_SIZE):
        block = bitstream[b:b+BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:
            block = np.pad(block, (0, BLOCK_SIZE - len(block)), 'constant')
        matrix = block.reshape(COLS, ROWS).T
        deinterleaved.extend(matrix.flatten())
    return np.array(deinterleaved, dtype=np.int16)
