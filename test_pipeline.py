from storage import list_models
from acoustic_beacon import encode_chunk_to_tones

def verify_pipeline():
    print("Verifying PhoneServe distributed storage and acoustic pipeline...")
    list_models()
    payload = encode_chunk_to_tones("PhoneServe-Model")
    print(f"Pipeline check complete. Encoded payload size: {len(payload)} bytes.")

if __name__ == "__main__":
    verify_pipeline()
