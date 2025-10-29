import socket
import threading
def receive(conn,):
    while True:
        data = conn.recv(1024).decode()
        if not data or data.strip().upper()== "OK":
            print("Client disconnected")
            break
        print(f"Client {data}")
    conn.close()

def send(conn):
    while True:
        msg = input()
        conn.sendall(msg.encode())
        if msg.strip().upper() == "OK":
            print("You ended chat")
            conn.close()
            break


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()
    print("Server starting at 127.0.0.0:5000")
    conn, addr = s.accept()
    print(f"connected at {addr}")

    threading.Thread(target=receive, args=(conn,), daemon=True).start()
    send(conn)
    s.close()
if __name__ == "__main__":
    start_server()
