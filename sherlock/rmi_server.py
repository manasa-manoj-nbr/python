import Pyro4
@Pyro4.expose

class StringConcatenator:
    def concatenate(self, s1,s2):
        return s1+s2

def main():
    server = "192.168.56.1"
    PORT = 5000
    daemon = Pyro4.Daemon(host=server, port=PORT)

    uri = daemon.register(StringConcatenator, objectId="concat")

    print(f"Server ready at {uri}")
    print("Serving..")

    daemon.requestLoop()

if __name__ == "__main__":
    main()