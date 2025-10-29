import socket

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen()
    print("Start server at 127.0.0.1")
    client_count = 0
    while True:
        conn,addr = s.accept()
        print(f"server conectd at {addr}")
        client_count+=1
        while True:
            data = conn.recv(1024).decode()
            if not data or data.strip().upper()=="OK":
                print("client disconncetd")
                break
            print(f"{client_count} says: {data}")
        conn.close()
if __name__ == "__main__":
    start_server()