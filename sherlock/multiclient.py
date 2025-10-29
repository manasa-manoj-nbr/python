import socket

def start_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("127.0.0.1", 5000))
    while True:
        print("connected at 127.0.0.1")
        msg = input()
        c.send(msg.encode())
        if msg.strip().upper()=="OK":
            print("client shutdown")
            break
    c.close()
if __name__ == "__main__":
    start_client()