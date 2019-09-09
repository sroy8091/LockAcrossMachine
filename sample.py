"""
test file to test the LoxAM by spawning multiple threads and trying to lock using same string
"""
from main import LoxAM
from multiprocessing import Process, current_process
import time


def func():
    print("This is the process ", current_process().name)
    with LoxAM("Sumit", current_process().name) as sc:
        sc.acquire()
        print("Do something after getting lock for process {}".format(current_process().name))
        time.sleep(5)

    print("End of func")


def main(i):

    print("This is starting of iteration", i)
    p1 = Process(target=func, name="Process - 1")
    p2 = Process(target=func, name="Process - 2")
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("This is end of iteration", i)


if __name__ == "__main__":
    for i in range(2):
        main(i)

    # func(1)
