import threading
import json
import time
import sys

from queue import Queue


records1 = []
records2 = []
records3 = []

# lock-objects
lock_file1 = threading.Semaphore()
lock_file2 = threading.Semaphore()
lock_file3 = threading.Semaphore()


def parser():
    parse1 = {"data":"1"}
    parse2 = {"data":"2"}
    parse3 = {"data":"3"}
    while True:
        time.sleep(0.1)
        records1.append(parse1)
        records2.append(parse2)
        records3.append(parse3)


def write1():
    while True:
        print("w1")
        lock_file1.acquire()
        if records1 != []:
            with open("file1.json", "w") as file1:
                json.dump(records1.pop(0), file1, indent=4, sort_keys=True)
        lock_file1.release()
        

def write2():
    while True:
        print("w2")
        lock_file2.acquire()
        if records2 != []:
            with open("file2.json", "a") as file2:
                json.dump(records2.pop(0), file2, indent=4, sort_keys=True)
        lock_file2.release()

                        
def write3():
    while True:
        print("w3")
        lock_file3.acquire()
        if records3 != []:
            with open("file3.json", "a") as file3:
                json.dump(records3.pop(0), file3, indent=4, sort_keys=True)
        lock_file3.release()
        

def read():
    while True:
        # 1
        lock_file1.acquire()
        print("reading from file 1")
        with open("file1.json", "r") as file:
            data = file.read()
            print(data)
        lock_file1.release()
        

        # 2
        lock_file2.acquire()
        print("reading from file 2")
        with open("file2.json", "r") as file:
            data = file.read()
            print(data)
        lock_file2.release()
        # time.sleep(1)


        # 3
        lock_file3.acquire()
        print("reading from file 3")
        with open("file3.json", "r") as file:
            data = file.read()
            print(data)
        lock_file3.release()
        # time.sleep(1)

        # 4
        print("not reading")
        

def main():
    w1 = threading.Thread(target=write1, args=(), name="w1")
    w2 = threading.Thread(target=write2, args=(), name="w2")
    w3 = threading.Thread(target=write3, args=(), name="w3")
    r = threading.Thread(target=read, args=(), name="r")
    p = threading.Thread(target=parser, args=(), name="p")

    w1.start()
    print("start w1")
    w2.start()
    print("start w2")
    w3.start()
    print("start w3")
    r.start()
    print("start r")
    p.start()
    print("start p")
        

if __name__ == "__main__":
    main()


