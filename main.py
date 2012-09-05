#!/usr/bin/python
#-*- coding: utf-8 -*-
from classes.FileSystem import *
from classes.helpers import *

def main():
    file = Folder(ROOT_SNAPSHOT_FOLDER)
    print "Getting count files..."
    file.childCount()
    print "Getted!\n"
    start = time.time()
    file.Run()
    print str(time.time() - start)
    print Get('count_files_cur')
    SaveFileId()
    SaveVersId()
    SaveFVId()
    database.commit()
    
#folder = Folder(ROOT_SNAPSHOT_FOLDER)
#Timer(folder.childCount)()
#print Get('count_files')
print Timer(RunGenerator)()
#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
