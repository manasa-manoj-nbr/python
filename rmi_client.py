import Pyro4

def main():
    server_host = "192.168.56.1"
    port = 5000
    proxy = Pyro4.Proxy(f"PYRO:concat@{server_host}:{port}")
    s1 = input("Give string 1")
    s2 = input("String 2")
    s3 = proxy.concatenate(s1,s2)
    print(s3)

if __name__ == "__main__":
    main()