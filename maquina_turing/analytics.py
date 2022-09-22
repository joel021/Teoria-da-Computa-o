import pandas as pd
import numpy as np
import time
import glob
from tm import TM

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

def delta_time(ext_delta, words, name):
    time_df = []
    for w in words:
        t0 = time.time()
        ext_delta(w)
        t1 = time.time()

        time_df.append({"deltaT": t1-t0,
                        "len_w": len(w),
                        "name": name})

    return time_df

def generate_words(x,y):
    words = []

    for k in np.arange(0, 10_000, 100):
        x_k = x*int(k/2)
        y_k = y*int(k/2)
        words.append(x_k+y_k)
        words.append(y_k+x_k)
    return words

def case_test(path, name, x, y):
    mt_def = d_from_file(path+"/"+name+".tm")

    mt_instance = TM()
    mt_instance.setup(mt_def)

    ## Generate too many words
    words = generate_words(x=x,y=y)
    pd.DataFrame(delta_time(mt_instance.extended_delta, words, name)).to_csv(path+"/test_cases/"+name+".csv", index=False)