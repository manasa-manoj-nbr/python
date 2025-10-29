import socket
import threading

def handle_client(conn, addr):
    while True:
        data = conn.recv(1024).decode()
        if not data or data.strip().upper == "OK":
            print("duisconected")
            break
        print(f"CLient {addr} : says : {data} ")
    conn.close()
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()
    print("server listening")
    while True:
        conn, addr = s.accept()
        print(f"Connected at {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
if __name__ == "__main__":
    start_server()
