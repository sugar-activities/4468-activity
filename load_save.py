#load_save.py
import g,utils

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    f.write(str(g.n)+'\n')
    f.write(g.found4+'\n')
    f.write(g.found5+'\n')

# note need for utils.chop() on strings
def retrieve():
    global loaded
    if len(loaded)>2:
        g.n=int(loaded[0])
        g.found4=loaded[1].rstrip()
        g.found5=loaded[2].rstrip()


    
