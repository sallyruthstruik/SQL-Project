#!/usr/bin/python
#-*- coding: utf-8 -*-
from classes.FileSystem import *
from classes.helpers import *

def main():
    
    print Timer(RunGenerator)()
    
    SaveFileId()
    SaveFVId()


main()
print "main ok"

database.close()
database = MyDatabase(HOST, USER, PASS, DATABASE_NAME)
cursor = database.myCursor

with open("query.sql") as fd:
    for line in fd:
        try:
            cursor.execute(line)
        except:
            pass
        
database.commit()

#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
