from time import time

def Timer(f):
    def _inside(*a, **kw):
        start = time()
        x = f(*a, **kw)
        print "Working "+str(time()-start)
        return x
    return _inside