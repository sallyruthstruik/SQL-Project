#!/usr/bin/python
#-*- coding: utf-8 -*-
from classes.FileSystem import *
from classes.helpers import *

def main():
    
    print Timer(RunGenerator)()
    
    SaveFileId()
    SaveVersId()
    SaveFVId()
    database.commit()


main()
#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
