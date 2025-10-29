import socket
import threading

def receive(c):
    while True:
        data = c.recv(1024).decode()
        if not data or data.strip().upper()=="OK":
            print("bye")
            break
        print(f"Server says : {data}")
    c.close()
def send(c):
    while True:
        msg = input()
        c.sendall(msg.encode())
        if msg.strip().upper() == "OK":
            print("Bye")
            c.close()
            break
def start_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("127.0.0.1", 5000))
    print("connected")
    threading.Thread(target=receive, args=(c,), daemon=True).start()
    send(c)

if __name__ == "__main__":
    start_client()


