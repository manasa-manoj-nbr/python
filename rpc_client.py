import Pyro4

def main():
    calculator = Pyro4.Proxy( "PYRONAME:calculator.rpc")

    while True:
        print("Calculator \n1. Addition \n2.Subtraction \n3.Mult \n4.Div \n5.exit")
        choice = int(input())

        if choice==5:
            print("exiting client")
            break
        a = int(input("Enter num 1 :"))
        b = int(input("enter no 2 :"))

        if choice==1:
            print(calculator.addition(a,b))
        if choice==2:
            print(calculator.subtraction(a,b))
        if choice==3:
            print(calculator.multiplication(a,b))
        if choice==4:
            print(calculator.divison(a,b))

if __name__ == "__main__":
    main()
