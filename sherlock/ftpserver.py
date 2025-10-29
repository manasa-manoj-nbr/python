from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user1", "test123", ".", perm="elradfmw")
    authorizer.add_anonymouse(".")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 2121))
    server.serve_forever()
if __name__ == "__main__":
    main()