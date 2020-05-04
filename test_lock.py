import threading
import time

lock = threading.Lock()


def unlock_function():
    time.sleep(5)


def one():
    print("lock 1")
    lock.acquire()
    print("sleep for 5 second")
    time.sleep(5)
    lock.release()
    print("exiting 1")


def two():
    print("lock 2")
    lock.acquire()
    print("sleep for 5 second")
    time.sleep(5)
    lock.release()
    print("exiting 2")


def main():
    t1 = threading.Thread(target=one, args=())
    t2 = threading.Thread(target=two, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()