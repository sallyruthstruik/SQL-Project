import time
import threading as th
import random as ran


def Ecran(string):
    string = string.replace("'", r"\'").replace('"', r'\"').replace("\n", '')
    return string

def Timer(f):
    def _inside(*a, **kw):
        start = time.time()
        x = f(*a, **kw)
        t = str(time.time()-start)
        print "Working "+t
        return [x, t]
    return _inside

def Threading(f):
    def inside(*args, **kwargs):
        thread = th.Thread(target = f, args = args, kwargs = kwargs)
        thread.start()
        return thread
    return inside

def getRandomElement(arr, delete = False):
    index = ran.randrange(0, len(arr), 1)
    value = arr[index]
    if delete:
        arr.remove(value)
    return value
