import socket

def start_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("127.0.0.1", 5000))
    print("client connected to srver")

    while True:
        msg = input()
        c.send(msg.encode())
        if msg.strip().upper() == "OK":
            print("Client disconnetd")
            break
    c.close()

if __name__ == "__main__":
    start_client()
