import threading
import json
import time
import sys

from queue import Queue


data1 = []
data2 = []
data3 = []


# events
write_file1 = threading.Event()
write_file2 = threading.Event()
write_file3 = threading.Event()
parse_data = threading.Event()

# lock-objects
l1 = threading.Lock()
l2 = threading.Lock()
l3 = threading.Lock()

# semaphore
semaphore = threading.Semaphore(3)

# barrier
b = threading.Barrier(3)


def parser():
    while True:
        if parse_data.is_set():
            print("ppppppp")
            parse1 = None
            parse2 = None
            parse3 = None

            time.sleep(3)

            parse1 = {"data":"1"}

            data1.append(parse1)

            parse2 = {"data":"2"}
            data2.append(parse2)

            parse3 = {"data":"3"}
            data3.append(parse3)

            parse_data.clear()
            parse_data.wait()


def write1():
    while True:
        if write_file1.is_set():
            print("w1")
            if data1 != []:
                with open("file1.json", "a") as file1:
                    json.dump(data1.pop(0), file1, indent=4, sort_keys=True)
            write_file1.clear()
            write_file1.wait()            


def write2():
    while True:
        if write_file2.is_set():
            print("w2")
            if data2 != []:
                with open("file2.json", "a") as file2:
                    json.dump(data2.pop(0), file2, indent=4, sort_keys=True)
            write_file2.clear()
            write_file2.wait()
           
            


def write3():
    while True:
        if write_file3.is_set():
            
            print("w3")
            if data3 != []:
                with open("file3.json", "a") as file3:
                    json.dump(data3.pop(0), file3, indent=4, sort_keys=True)
            write_file3.clear()
            write_file3.wait()
            

def main():
    w1 = threading.Thread(target=write1, args=(), name="w1")
    w2 = threading.Thread(target=write2, args=(), name="w2")
    w3 = threading.Thread(target=write3, args=(), name="w3")
    p = threading.Thread(target=parser, args=(), name="p")

    pool = Queue(4)
    pool.put(write_file1)
    pool.put(write_file2)
    pool.put(write_file3)
    pool.put(parse_data)


    write_file1.clear()
    write_file2.clear()
    write_file3.clear()
    parse_data.clear()

    # write_file1.set()
    # write_file2.set()
    # write_file3.set()
    # parse_data.set()

    w1.start()
    print("start w1")
    w2.start()
    print("start w2")
    w3.start()
    print("start w3")
    p.start()
    print("start p")

    while True:
        e1 = pool.get()
        e1.set()

        e2 = pool.get()
        e2.set()

        e3 = pool.get()
        e3.set()

        pool.put(e1)
        pool.put(e2)
        pool.put(e3)
        


if __name__ == "__main__":
    main()


