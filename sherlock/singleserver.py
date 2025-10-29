import socket
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()
    print("Server starting at 127.0.0.0:5000")
    conn, addr = s.accept()
    print(f"Connected to {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data or data.strip().upper()== "OK":
            print("Client disconnected")
            break
        print(f"Client says: {data}")
    conn.close()
    s.close()

if __name__ == "__main__":
    start_server()
