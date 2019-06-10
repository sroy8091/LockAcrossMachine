from main import LoxAM
import threading


class SampleContext():
    def __init__(self, name):
        self.name = name

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        print("Exiting context")

    def print_name(self):
        print(self.name)


def func():
    with LoxAM("Sumit", "sumit") as sc:
        sc.acquire()

    print("End of func")


class Celsius(object):
    def __init__(self, value=0.0):
        print(type(value))
        self.value = float(value)

    def __get__(self, instance, owner):
        print(instance)
        print(owner)
        return self.value

    def __set__(self, instance, value):
        print(instance)
        print(value)
        self.value = float(value)

    def __delete__(self, instance):
        pass


class Temperature(object):
    celsius = Celsius()

# t = Temperature()


def main(i):
    global x
    x = 0

    print("this is thread", i)
    t1 = threading.Thread(target=func)
    t2 = threading.Thread(target=func)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    for i in range(4):
        main(i)
        print("x = {1} after Iteration {0}".format(i, x))
