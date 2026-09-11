import urllib.request
import urllib.error

WEBDAV_URL = "http://127.0.0.1:8090"

def check_cluster():
    try:
        req = urllib.request.Request(f"{WEBDAV_URL}/test.txt", method="GET")
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            print(f"Cluster status: OK. Retrieved -> {content.strip()}")
    except urllib.error.URLError as e:
        print(f"Connection failed: {e.reason}")

if __name__ == "__main__":
    check_cluster()
