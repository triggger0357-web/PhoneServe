import wave
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  # Length of the audio recording
WAVE_OUTPUT_FILENAME = "/data/data/com.termux/files/home/PhoneServe/phoneserve_bootstrap.wav"

p = pyaudio.PyAudio()

print("[*] Preparing to record acoustic bootstrap payload...")
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print(f"[*] Recording for {RECORD_SECONDS} seconds... Play your source tone now!")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("[*] Recording complete. Saving audio file...")

stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded frames as a standard .wav audio file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"[+] Acoustic payload saved successfully to:\n    {WAVE_OUTPUT_FILENAME}")
