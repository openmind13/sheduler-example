import threading
import json
import time
import sys

from queue import Queue


records1 = []
records2 = []
records3 = []


# events
write_file1 = threading.Event()
write_file2 = threading.Event()
write_file3 = threading.Event()
read_file = threading.Event()



# parse_data = threading.Event()

# event_pool = Queue(4)

# file_pool = Queue(3)
# file_pool.put("file1.json")
# file_pool.put("file2.json")
# file_pool.put("file3.json")

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
        # if write_file1.is_set():
        write_file1.wait()
        print("w1")

        lock_file1.acquire()
        if records1 != []:
            with open("file1.json", "w") as file1:
                json.dump(records1.pop(0), file1, indent=4, sort_keys=True)
        lock_file1.release()

        write_file1.clear()
        

def write2():
    while True:
        # if write_file2.is_set():
        write_file2.wait()
        print("w2")

        lock_file2.acquire()
        if records2 != []:
            with open("file2.json", "a") as file2:
                json.dump(records2.pop(0), file2, indent=4, sort_keys=True)
        lock_file2.release()

        write_file2.clear()
        
                        
def write3():
    while True:
        # if write_file3.is_set():
        write_file3.wait()
        print("w3")

        lock_file3.acquire()
        if records3 != []:
            with open("file3.json", "a") as file3:
                json.dump(records3.pop(0), file3, indent=4, sort_keys=True)
        lock_file3.release()

        write_file3.clear()
        

def read():
    time.sleep(1)
    write_file1.clear()
    write_file2.clear()
    write_file3.clear()


    write_file1.set()
    write_file2.set()
    write_file3.set()

    time.sleep(1)

    while True:
        with lock_file1:
            write_file2.set()
            write_file3.set()

            lock_file1.acquire()
            print("reading from file 1")
            with open("file1.json", "r") as file:
                data = file.read()
                print(data)
            lock_file1.release()

            time.sleep(1)

        with lock_file2:
            write_file1.set()
            write_file3.set()

            lock_file2.acquire()
            print("reading from file 2")
            with open("file2.json", "r") as file:
                data = file.read()
                print(data)
            lock_file2.release()
    
            time.sleep(1)

        with lock_file3:
            write_file1.set()
            write_file2.set()

            lock_file2.acquire()
            print("reading from file 3")
            with open("file3.json", "r") as file:
                data = file.read()
                print(data)
            lock_file3.release()

            time.sleep(1)

        write_file1.set()
        write_file2.set()
        write_file3.set()

        # print("not reading")
        # time.sleep(1)


    # while True:
    
        # 1
        # with lock_file1:
        #     write_file2.set()
        #     write_file3.set()
            
        #     lock_file1.acquire()
        #     print("reading from file 1")
        #     # time.sleep(1)
        #     lock_file1.release()

        # with lock_file2:
        #     write_file1.set()
        #     write_file3.set()
            
        #     lock_file2.acquire()
        #     print("reading from file 2")
        #     # time.sleep(1)
        #     lock_file2.release()

        # with lock_file3:
        #     write_file1.set()
        #     write_file2.set()
            
        #     lock_file3.acquire()
        #     print("reading from file 3")
        #     # time.sleep(1)
        #     lock_file3.release()

        # time.sleep(3)

        # with lock_file1:
        #     write_file1.clear()
        #     # lock_file1.acquire()
        #     print("read from file 1")
        #     # lock_file1.release()
        #     write_file1.set()

        # with lock_file2:
        #     write_file2.clear()
        #     # lock_file2.acquire()
        #     print("read from file 2")
        #     # lock_file2.release()
        #     write_file2.set()

        # with lock_file3:
        #     write_file3.clear()
        #     # lock_file3.acquire()
        #     print("read from file 3")
        #     # lock_file3.release()
        #     write_file1.set()

        # print("not reading")
        # 2

        # 3

        # 4

        
        # time.sleep(4)
        # print("waiting for 4 second")
       

def main():
    w1 = threading.Thread(target=write1, args=(), name="w1")
    w2 = threading.Thread(target=write2, args=(), name="w2")
    w3 = threading.Thread(target=write3, args=(), name="w3")
    r = threading.Thread(target=read, args=(), name="r")
    p = threading.Thread(target=parser, args=(), name="p")

    write_file1.clear()
    write_file2.clear()
    write_file3.clear()
    read_file.clear()

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


