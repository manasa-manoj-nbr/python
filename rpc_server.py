import Pyro4
@Pyro4.expose

class Calculator(object):
    def addition (self, a, b):
        return a+b
    def subtraction (self, a, b):
        return a-b
    def multiplication (self, a, b):
        return a*b
    def divison (self, a, b):
        if(b==0):
            return "Error"
        return a/b

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Calculator)
    ns.register("calculator.rpc",uri)
    print("Server Ready")

    daemon.requestLoop()

if __name__ == "__main__":
    main()