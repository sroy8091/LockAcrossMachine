from main import LoxAM
import threading
import time


def func(i):
    print("this is the thread", i)
    with LoxAM("Sumit", i, thread=i) as sc:
        sc.acquire()
        print("do something after getting lock for thread {}".format(i))
        time.sleep(5)

    print("End of func")


def main(i):
    global x
    x = 0

    print("this is iteration", i)
    t1 = threading.Thread(target=func, args=[1])
    time.sleep(10)
    t2 = threading.Thread(target=func, args=[2])

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    for i in range(2):
        main(i)
        print("x = {1} after Iteration {0}".format(i, x))

    # func(1)
