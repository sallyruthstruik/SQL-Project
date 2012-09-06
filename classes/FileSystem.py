#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import datetime
import time
from classes.Connection import *
from classes.globals import *
from classes.helpers import *


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


fdquer = open("query.sql", "w")

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
        query = "INSERT INTO File VALUES(%(id)s, '%(name)s', '%(path)s', '%(type)s', %(len)s);"%{
                                 "id": self.id,
                                 "name": Ecran(self.name),
                                 "path": Ecran(self.absolute_path),
                                 "type": self.type,
                                 'len': getPathLen(self.absolute_path)}
        #try:
        print >> fdquer, query
        #cursor.execute(query)
        FileVersion(self).insertIntoDatabase()
        #except:

        
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

global_version = Version()
global_version.insertIntoDatabase()
SaveVersId()

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
        query1 = "INSERT INTO FileVersion VALUES(%(id)s, %(fid)s, %(vid)s);"%{
            'id': self.id,
            'fid': self.file.id,
            'vid': self.version.id
            }
        print>>fdquer, query1
        #cursor.execute(query1)
        query2 = "INSERT INTO FileVersionAttr VALUES(%(fvid)s, '%(mtime)s', '%(latime)s', %(size)s, %(h)s);"%{
            'fvid': self.id,
            'mtime': timeFromSeconds(self.modification_time),
            'latime': timeFromSeconds(self.la_time),
            'size': self.size,
            'h': self.is_hidden
            }
        print>>fdquer, query2
        #cursor.execute(query2)


#generator = database.getPathCursor() 
#next_object = generator.next()
fd = open("test", 'w')

def SeeTwoArray(arr1, arr2):
    """
        returns (a,b) where a - elements from arr1 and not in arr2 and 
        b - elements from arr2 and not in arr1"""
    common_elements=[]
    for item in arr1:
        if item in arr2:
            common_elements.append(item)
            
    returning = [[],[]]
    
    for item in arr1:
        if item not in common_elements:
            returning[0].append(item)
            
    for item in arr2:
        if item not in common_elements:
            returning[1].append(item)
    
    return returning
    

class Folder(File):
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("not folder")
        File.__init__(self, path)
    
    
#    def Run(self):
#        global next_object
#        #if Get("count_files_cur")%SET_PRINTING_INTERVAL == 0:
#        #    print "Now "+str(Get("count_files_cur")) + " from "+str(Get("count_files"))
#        files =[]
#        folders = []
#        for item in os.listdir(self.absolute_path):
#            new_path = self.absolute_path + '/' + item
#            if getType(new_path) == 'folder':
#                try:
#                    folders.append(Folder(new_path))
#                except ValueError:
#                    pass
#            else:
#                try:
#                    files.append(File(new_path))
#                except ValueError:
#                    pass
#            Inc("count_files_cur")
#        
#        
#        for item in files+folders:
#            item.insertIntoDatabase()
#
#        for item in folders:
#            try:
#                item.Run()
#            except OSError:
#                print "Permission denied on " + item.absolute_path
            
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

memory = []
def ArrayInMemory(element = None):   #Статическая переменная memory хранит файлы, которые надо обработать
    global memory
    if element: memory.append(element)
    else:
        memory = memory[1:]
    return memory

label = True    #Отвечает за выход из функции внесения в базу данных. InsertInto
def threadDo():
    global label
    label = False


def RunGeneratorDecorator(f):
    def InsertInto():
        memory = ArrayInMemory()
        while label:
            while len(memory)>0:
            #try:
                if len(memory)%1000 == 0:
                    print len(memory)
                try:
                    element = memory[0]
                except:
                    continue
                element.insertIntoDatabase()
                memory = ArrayInMemory()
            #except:
                pass
        database.commit()
    
    def _inside():
        thread = Threading(InsertInto)()
        x = Timer(f)()
        print "Файлы собраны. Вношу в базу..."
        thread.join()
        return x
    
    return _inside
        
#@RunGeneratorDecorator
def RunGenerator():
        folders_first=[ROOT_SNAPSHOT_FOLDER]
        folders_last=[]
        i=0
        generator = database.getPathCursor()    #Получаем список путей из базы данных
        is_new = False  #По умолчанию дамп не новый
        try:
            first_element = generator.next()
            layer = int(first_element[1])
        except:
            is_new = True   #Если список путей пуст - значит дамп новый.
            
        print is_new
        labelquit = True    #Отвечает за выход из главного цикла
        while labelquit:     #Пока есть слои  
            last_files = []     #Файлы из базы из текущего слоя
            if not is_new:
                while layer == first_element[1]:     #пока номер слоя совпадает с номером слоя файла из генератора, сохраняем этот файл 
                    last_files.append(first_element[0])
                    try:
                        first_element = generator.next()
                    except StopIteration:
                        break
                
            for item in getSliceFSGenerator(folders_first):     #для каждого элемента в текущем слое
                i+=1  
                if item in last_files:  #Если этот элемент есть в базе значит ФАЙЛ не изменился. Удаляем из рассмотрения
                    last_files.remove(item) 
                else:
                    pass#print >>fd, item + " new!"  #Иначе файл - новый
                    
                try:
                    file = File(item)   # Создаем файл для пути
                    if file.type == "folder":   #Если файл - папка то 
                        folders_last.append(item)   #добавляем в дочерние папки
                    #ArrayInMemory(file)
                    file.insertIntoDatabase()    #и пишем в базу данных
                except BaseException as x:
                    print x
                    
            
            if len(folders_last) == 0:  #если дочерних папок не осталось
                labelquit = False   #выходим из цикла
            else:
                folders_first = folders_last[:] #иначе меняем местами исходные и дочерние папки и идем в начало цикла
                folders_last = []
            
            if not is_new:
                layer = first_element[1]    #увеличиваем слой
                print >>fd, "Removed elements "+str(last_files) #если в проверяемом слое остались файлы, значит мы что то удалили. При этом, все дочерние элементы данных также должны быть удалены.
        threadDo() 
        return i    #Возвращаем число обработанных файлов.
        
    
    
    
    
    
    
    