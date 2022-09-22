from multiprocessing import Process
from analytics import *
from threading import Thread

def new_thread(path, name, x, y, qtd, step, time_off):
    p1 = Process(target=case_test, args=(path, name, x, y, qtd, step, time_off))
    p1.start()
    p1.join() #wait for the finish
    print(name+" finished")

if __name__ == "__main__":

    """
    #Maquina de Turing 1:
    print("M1")
    t1 = Thread(target=new_thread, args=("./data", "def1", "a", "b", 1_000, 100, 30))
    t1.start()

    #Maquina de Turing 2:
    print("M2")
    t2 = Thread(target=new_thread, args=("./data", "def2", "0", "1", 10_000, 100, 30))
    t2.start()
    """
    #Maquina de Turing 3:
    print("M3")
    t3 = Thread(target=new_thread, args=("./data", "def3", "a", "a",  2_000, 100, 30))
    t3.start()

    """
    #Maquina de Turing 4:
    print("M4")
    t4 = Thread(target=new_thread, args=("./data", "def4", "a", "a", 10_000, 100, 30))
    t4.start()
    """
    #Maquina de Turing 5:
    print("M5")
    t5 = Thread(target=new_thread, args=("./data", "def5", "1", "1",  2_000, 100, 30))
    t5.start()