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
            except _mysql_exceptions.ProgrammingError:
                pass
        
    database.commit()
    
    

def main():
    
    print Timer(RunGenerator)()
    
    SaveFileId()
    SaveFVId()
    print "main ok. Inserting..."
    database.close()
    Timer(InsertFromFile)()
    


main()
#print "Hello!"

#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
