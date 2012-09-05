#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import datetime
import time
from classes.Connection import *
from classes.globals import *

version_id = int(Config("max_v_id").value)+2

def IncVersId():
    global version_id
    version_id +=1
def GetVersId():
    return version_id
def SaveVersId():
    x = Config("max_v_id")
    x.value = GetVersId()
    x.insertIntoDatabase()

file_id = int(Config("max_f_id").value)+1
def IncFileId():
    global file_id
    file_id+=1
def GetFileId():
    return file_id
def SaveFileId():
    x = Config("max_f_id")
    x.value = GetFileId()
    x.insertIntoDatabase()

fv_id = int(Config("max_fv_id").value)+1
def IncFVId():
    global fv_id
    fv_id+=1
def GetFVId():
    return fv_id 
def SaveFVId():
    x = Config("max_fv_id")
    x.value = GetFVId()
    x.insertIntoDatabase()

def getType(s):
    
    if os.path.islink(s):
        return "link"
    elif os.path.ismount(s):
        return "mount"
    elif os.path.isdir(s):
        return "folder"
    elif os.path.isfile(s):
        return "file"
    else:
        return "unexpected"
    
def getPathLen(path):
    return len(path.split("/"))

def timeFromSeconds(t):
    return datetime.datetime(*time.localtime(time.time())[:6])




class File:
    color = "white"
    def __init__(self, full_path):
        self.id = GetFileId()
        IncFileId()
        if os.path.exists(full_path):
            if len(full_path)>1 and full_path[-1] == '/':
                full_path = full_path[:-1]
            self.absolute_path = full_path
            
            if os.path.split(full_path)[1] == '':
                self.name = 'root'
            else:
                self.name = os.path.split(full_path)[1]
            self.type = getType(full_path)
        else:
            raise ValueError("path is bad")
    
    def insertIntoDatabase(self):
        query = "INSERT INTO File VALUES(%(id)s, '%(name)s', '%(path)s', '%(type)s');"%{
                                 "id": self.id,
                                 "name": self.name,
                                 "path": self.absolute_path,
                                 "type": self.type}
        #try:
        cursor.execute(query)
        FileVersion(self).insertIntoDatabase()
        #except:
        #    pass
        
    def __str__(self):
        return self.absolute_path +" "+ self.name+ " "


def getSliceFSGenerator(arr=[ROOT_SNAPSHOT_FOLDER]):
    """
        Генератор.
        Возвращает адреса всеx папок, являющихся прямыми потомками папок, указанных в arr
        """
    for item in arr:
        folder = Folder(item)
        try:
            for x in os.listdir(folder.absolute_path):
                yield os.path.join(item, x)
        except:
            pass


class Version:
    def __init__(self):
            self.name = input("Введите название версии \n")
            self.description = input("Введите описание версии \n")
            self.id = GetVersId()
            IncVersId()
            self.date = datetime.datetime.now()

    def insertIntoDatabase(self):
        query = "Insert into Versions values(%(id)s, '%(date)s', '%(name)s', '%(desc)s')"%{
                                                                                         'id': self.id,
                                                                                         'date': self.date,
                                                                                         'name': self.name,
                                                                                         'desc': self.description
                                                                                         }
        cursor.execute(query)
        database.commit()

#global_version = Version()
#global_version.insertIntoDatabase()

class FileVersion:
    def __init__(self, file):
        self.file = file
        path = file.absolute_path
        self.id = GetFVId()
        IncFVId()
        self.size = os.path.getsize(path)
        self.modification_time = os.path.getmtime(path)
        self.la_time = os.path.getatime(path)
        self.version = global_version
        if file.name[0] == '.':
            self.is_hidden = True
        else:
            self.is_hidden = False
    
    
    def insertIntoDatabase(self):
        query1 = "INSERT INTO FileVersion VALUES(%(id)s, %(fid)s, %(vid)s)"%{
            'id': self.id,
            'fid': self.file.id,
            'vid': self.version.id
            }
        cursor.execute(query1)
        query2 = "INSERT INTO FileVersionAttr VALUES(%(fvid)s, '%(mtime)s', '%(latime)s', %(size)s, %(h)s)"%{
            'fvid': self.id,
            'mtime': timeFromSeconds(self.modification_time),
            'latime': timeFromSeconds(self.la_time),
            'size': self.size,
            'h': self.is_hidden
            }
        cursor.execute(query2)


#generator = database.getPathCursor() 
#next_object = generator.next()
fd = open("test", 'w')

def SeeTwoArray(arr1, arr2):
    """
        returns (a,b) where a - elements from arr1 and not in arr2 and 
        b - elements from arr2 and not in arr1"""
    class colorel:
        def __init__(self, el):
            self.element = el
            self.color = "white"

class Folder(File):
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("not folder")
        File.__init__(self, path)
    
    
    def Run(self):
        global next_object
        if Get("count_files_cur")%SET_PRINTING_INTERVAL == 0:
            print "Now "+str(Get("count_files_cur")) + " from "+str(Get("count_files"))
        files =[]
        folders = []
        for item in os.listdir(self.absolute_path):
            new_path = self.absolute_path + '/' + item
            if getType(new_path) == 'folder':
                try:
                    folders.append(Folder(new_path))
                except ValueError:
                    pass
            else:
                try:
                    files.append(File(new_path))
                except ValueError:
                    pass
            Inc("count_files_cur")
        
        
        folder_objects = []
        
        while str(next_object).find(self.absolute_path) != -1 and ((getPathLen(self.absolute_path)+1)==getPathLen(next_object)):
            folder_objects.append(next_object)
            next_object = generator.next()

        print >> fd, self.absolute_path
        for x in folder_objects:
            print >>fd, "\t\t"+x
        

        for item in files+folders:
            pass#item.insertIntoDatabase()

        for item in folders:
            try:
                item.Run()
            except OSError:
                print "Permission denied on " + item.absolute_path
            
    def childCount(self):
        for item in os.listdir(self.absolute_path):
            new_path = self.absolute_path + '/' + item
            if getType(new_path) == 'folder':
                try:
                    Folder(new_path).childCount()
                except:
                    pass
                
            Inc("count_files")
        self.child_count = Get("count_files")

def RunGenerator(folders_first=[ROOT_SNAPSHOT_FOLDER], folders_last=[], i=0):
        while True:
            for item in getSliceFSGenerator(folders_first):
                i+=1
                try:
                    file = File(item)
                    if file.type == "folder":
                        folders_last.append(item)
                    file.insertIntoDatabase()
                except:
                    pass
            
            database.commit()
            
            if len(folders_last) == 0:
                break
            else:
                folders_first = folders_last[:]
                folders_last = []
        return i
        
    
    
    
    
    
    
    