import socket
import threading

LOCAL_PORT = 8080
TARGET_PORT = 8081

def handle_client(client_socket):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect(('127.0.0.1', TARGET_PORT))
        
        def forward(source, destination):
            try:
                while True:
                    data = source.recv(4096)
                    if not data:
                        break
                    destination.sendall(data)
            except:
                pass
            finally:
                source.close()
                destination.close()

        threading.Thread(target=forward, args=(client_socket, remote_socket), daemon=True).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket), daemon=True).start()
    except:
        client_socket.close()

def run_wrapper():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', LOCAL_PORT))
    server.listen(5)
    print(f"[*] Userspace Mesh Wrapper active on port {LOCAL_PORT}")
    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == '__main__':
    run_wrapper()
