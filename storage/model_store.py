import urllib.request
import urllib.error
import os

WEBDAV_URL = "http://127.0.0.1:8090"

def upload_model(local_path: str, remote_filename: str):
    url = f"{WEBDAV_URL}/{remote_filename}"
    print(f"Uploading {local_path} to cluster as {remote_filename}...")
    try:
        with open(local_path, "rb") as f:
            data = f.read()
        req = urllib.request.Request(url, data=data, method="PUT")
        with urllib.request.urlopen(req) as response:
            print(f"Upload complete. Status: {response.status}")
    except Exception as e:
        print(f"Upload failed: {e}")

def download_model(remote_filename: str, local_path: str):
    url = f"{WEBDAV_URL}/{remote_filename}"
    print(f"Downloading {remote_filename} from cluster to {local_path}...")
    try:
        urllib.request.urlretrieve(url, local_path)
        print("Download complete.")
    except Exception as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    print("Model store utility ready.")
