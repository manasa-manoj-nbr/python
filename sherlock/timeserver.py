import socket
import threading
import datetime

HOST = "127.0.0.1"
PORT = 5000


def format_message(msg, addr):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{now}] ({addr[0]}:{addr[1]}) {msg}"


def receive(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            print(data)
        except:
            break
    client.close()


def send(client):
    addr = client.getsockname() 
    while True:
        msg = input()
        if msg.strip() == "#EXIT":
            print("Disconnected from server.")
            client.close()
            break
        message = format_message(msg, addr)
        client.sendall(msg.encode())
        print(message)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    print("Type #EXIT to leave the chat.\n")

    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)


if __name__ == "__main__":
    main()
