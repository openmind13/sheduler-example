# задача об обедающих философах

import time
import threading


sem = threading.Semaphore()

count = {}

def philosopher(name):
    count[name] = 0
    while True:
        print(name + " is thinking")
        sem.acquire()
        print(name + " is eating")
        count[name] += 1
        sem.release()
        time.sleep(0.5)


def main():
    ph1 = threading.Thread(target=philosopher, args=("ph1", ), name="ph1")
    ph2 = threading.Thread(target=philosopher, args=("ph2", ), name="ph2")
    ph3 = threading.Thread(target=philosopher, args=("ph3", ), name="ph3")
    ph4 = threading.Thread(target=philosopher, args=("ph4", ), name="ph4")
    ph5 = threading.Thread(target=philosopher, args=("ph5", ), name="ph5")

    philosophers = []
    philosophers.append(ph1)
    philosophers.append(ph2)
    philosophers.append(ph3)
    philosophers.append(ph4)
    philosophers.append(ph5)

    for t in philosophers:
        t.start()

    while True:
        time.sleep(5)
        sem.acquire()
        for key in count:
            print(key,  " => ", count[key])
        sem.release()


    


if __name__ == "__main__":
    main()