import pandas as pd
import numpy as np
import time
import glob
from tm import TM
from threading import Thread
import matplotlib.pyplot as plt

def d_from_file(file):
    """Definition from file"""

    f = open(file,"r")
    data = []
    for l in f.readlines():
        data.append(l[0:-1])        
    f.close()
    return data

def get_definitions(path):
    definitions = []
    for file in glob.glob(path+"/*.mt"):
        definitions.append(d_from_file(file))

    return definitions

def process_word(turing_reference, word, result):
    result['t0'] = time.time()
    turing_reference.extended_delta(word)
    result['t1'] = time.time()

def delta_time(mt_instance, words, name, time_off):
    time_df = []
    for w in words:

        result = dict({"t0": time.time(),
                        "t1": None})

        t = Thread(target=process_word, args=(mt_instance, w, result))
        t.start()

        while (result['t1'] == None and (time.time() - result["t0"]) < time_off): #wait, on the main thread, if the result changes. If not change and time out of the time_off, stop this thread
            time.sleep(0.1) #sleep for 0.1 seconds

        if result['t1'] != None: #compute only the occurrences that MT not loop
            time_df.append({"deltaT": result['t1']-result['t0'],
                            "len_w": len(w),
                            "name": name})

    return time_df

def generate_words(x,y, qtd=10_000, step=100):
    words = []

    for k in np.arange(0, qtd, step):
        x_k = x*int(k/2)
        y_k = y*int(k/2)
        words.append(x_k+y_k)
    return words

def case_test(path, name, x, y, qtd, step, time_off):
    mt_def = d_from_file(path+"/"+name+".tm")

    mt_instance = TM()
    mt_instance.setup(mt_def)

    ## Generate too many words
    words = generate_words(x=x,y=y, qtd = qtd, step = step)
    pd.DataFrame(delta_time(mt_instance, words, name, time_off)).to_csv(path+"/"+name+".csv", index=False)


def plot(x_arr, y_arr, title, w=10, h=10):
    fig, ax = plt.subplots(figsize=(w, h))
    
    ax.axvline(x=0, color='red')
    ax.axhline(y=0, color='yellow')

    ax.plot(x_arr, y_arr, 'b-', label='y')

    ax.set(xlabel='|w|->', ylabel='deltaT(|w|) (s)->', title=title)
    ax.grid()
    ax.legend()
    plt.show()

def plot_compare(x_arr, y_arr, x_pred, y_pred, popt, mse_error, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axvline(x=0, color='red')
    ax.axhline(y=0, color='yellow')
    
    ax.plot(x_pred, y_pred, 'r-', label="fit: a = "+str(popt[0])+", b = "+str(popt[1])+", c = "+str(popt[2])+", erro mse = "+str(mse_error))
    ax.plot(x_arr, y_arr, 'b-', label='y')

    ax.set(xlabel='|w|->', ylabel='deltaT(|w|) (s)->', title=title)
    ax.grid()
    ax.legend()
    plt.show()