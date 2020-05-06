import threading
import json
import time
import sys

from queue import Queue


data1 = []
data2 = []
data3 = []


event_pool = Queue(4)

file_pool = Queue(3)
file_pool.put("file1.json")
file_pool.put("file2.json")
file_pool.put("file3.json")

# lock objects
lock_file1 = threading.Lock()
lock_file2 = threading.Lock()
lock_file3 = threading.Lock()


def parser():
    parse1 = {"data":"1"}
    parse2 = {"data":"2"}
    parse3 = {"data":"3"}
    while True:
        print("parser")
        time.sleep(2)
        data1.append(parse1)
        data2.append(parse2)
        data3.append(parse3)


def write1():
    while True:
        lock_file1.acquire()
        print("w1")
        if data1 != []:
            with open("file1.json", "a") as file1:
                json.dump(data1.pop(0), file1, indent=4, sort_keys=True)
        lock_file1.release()  


def write2():
    while True:
        lock_file2.acquire()
        print("w2")
        if data2 != []:
            with open("file2.json", "a") as file2:
                json.dump(data2.pop(0), file2, indent=4, sort_keys=True)
        lock_file2.release()

              
def write3():
    while True:
        lock_file3.acquire()
        print("w3")
        if data3 != []:
            with open("file3.json", "a") as file3:
                json.dump(data3.pop(0), file3, indent=4, sort_keys=True)
        lock_file3.release()


def read():
    while True:
        if read_file.is_set():
            lock_file1.acquire()
            with open("file1.json", "r") as file:
                data = json.load(file)
            print(data)
            read_file.clear()
            lock_file1.release()
            write_file.wait()

        if read_file.is_set():
            lock_file2.acquire()
            with open("file2.json", "r") as file:
                data = json.load(file)
            print(data)
            read_file.clear()
            lock_file2.release()
            write_file.wait()

        if read_file.is_set():
            lock_file3.acquire()
            with open("file3.json", "r") as file:
                data = json.load(file)
            print(data)
            read_file.clear()
            lock_file3.release()
            write_file.wait()


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

