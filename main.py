#!/usr/bin/python
#-*- coding: utf-8 -*-
from classes.FileSystem import *
from classes.helpers import *
import _mysql_exceptions


def InsertFromFile():
    database = MyDatabase(HOST, USER, PASS, DATABASE_NAME)
    cursor = database.myCursor

    with open("query.sql") as fd:
        i=0
        for line in fd:
            i+=1
            if i%10000 == 0:
                print i
            try:
                cursor.execute(line)
            except BaseException as x:
                print "\n---------------------------------------\n"+line+"\n-------------------------------------\n"
                print x
        
    database.commit()
    
    

def main():
    
    RunGenerator2()
    
    SaveFileId()
    SaveFVId()
    print "main ok. Inserting..."
    database.close()
    Timer(InsertFromFile)()
    


#main()
#print "Hello!"
def test(f=None):
    def lens(fd):
        i=0
        for x in fd:
            i+=1
        return i
    with open("tests", 'w') as fd:
        print>>fd,''

    for i in range(11):
        with open("tests", 'a') as fd:
            x =  Timer(getFSLayer2)(i)
            print >> fd,  str(i), lens(x[0]), x[1]
            #print "test "+str(i)+" doing"
        
#main()
with open(memory_past, 'w') as fd:
    pass
    
with open(memory_next, 'w') as fd:
    pass
#test()
print "Hello"
def printing(resp):
    return str(resp[0])+" "+str(resp[1])

"""tester(
    getFSLayerRecursive,
    [
     [["/home/stas/workspace/Dudu.com"], {}],
     [["/home/stas/workspace/SQL Project"], {}],
     [["/home/stas/workspace"], {}],
     [["/home/stas/Изображения"], {}],
     [["/home/stas/.config"],{}],
     [["/home/stas"], {}]
     ],
    printing
       )"""
print getFSLayerRecursive()
#print "Привет!"##
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
