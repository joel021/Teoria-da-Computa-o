from multiprocessing import Process
from analytics import *

if __name__ == "__main__":
    #Maquina de Turing 1:
    print("M1")
    p1 = Process(target=case_test, args=("./data", "def1", "a", "b"))
    p1.start()

    #Maquina de Turing 2:
    print("M2")
    p2 = Process(target=case_test, args=("./data", "def2", "0", "1"))
    p2.start()

    #Maquina de Turing 3:
    print("M3")
    p3 = Process(target=case_test, args=("./data", "def3", "a", "a"))
    p3.start()

    #Maquina de Turing 4:
    print("M4")
    p4 = Process(target=case_test, args=("./data", "def4", "a", "a"))
    p4.start()

    #Maquina de Turing 5:
    print("M5")
    p5 = Process(target=case_test, args=("./data", "def5", "1", "1"))
    p5.start()