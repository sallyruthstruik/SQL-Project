#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import datetime
import time
from classes.Connection import *
from classes.globals import *
from classes.helpers import *



version_id = int(Config("max_v_id").value)+2
with open("query.sql", "w") as fdquer:
    print>>fdquer, ''

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
        with open("query.sql", "a") as fdquer:
            print >> fdquer, query
        #cursor.execute(query)
        FileVersion(self).insertIntoDatabase()
        #except:

        
    def __str__(self):
        return self.absolute_path +" "+ self.name+ " "

memory_past = "fs_layer_memory_1"
memory_next = "fs_layer_memory_2"
def getLayerChildren():
    """
        Пишет потомков папок, указанных в memory_past в memory_next
        """
    global memory_past, memory_next
    if not os.path.exists(memory_past):
        with open(memory_past, 'w') as fd:
            pass
    
    with open(memory_next, 'w') as fd:
            pass
        
    arr = []
    with open(memory_past, 'r') as fd:
        for x in fd:
            arr.append(x[:-1])
    if len(arr) == 0:
        arr = [ROOT_SNAPSHOT_FOLDER]

    for item in arr:
        try:
            folder = Folder(item)
        except ValueError as x:
            #print item + " not folder"
            continue

        try:
            for x in os.listdir(folder.absolute_path):
                with open(memory_next, 'a') as fd:
                    print >> fd, os.path.join(item, x)
        except OSError:
            print "permission denied on "+item
            pass
    temp = memory_next
    memory_next = memory_past
    memory_past = temp

last = 0
last_result = (ROOT_SNAPSHOT_FOLDER)
def getFSLayer2(i):
    global last, last_result
    while last<i:
        getLayerChildren()
        last+=1
    return open(memory_past, 'r')
    
with open("files_for_fs_recursive", 'w'):
    pass

count = 0

def getFSLayerRecursive(root = ROOT_SNAPSHOT_FOLDER, len=getPathLen(ROOT_SNAPSHOT_FOLDER)):
    global count
    len = len+1
    with open("files_for_fs_recursive", "a") as fd:
        for x in os.listdir(root):
            count +=1
            try:
                folder = Folder(os.path.join(root,x))
                print >>fd, folder.absolute_path, len
                getFSLayerRecursive(folder.absolute_path, len) 
            except BaseException as x:
                pass
    return count

refresh = True
def getFSLayer3(i):
    global refresh
    if refresh:
        getFSLayerRecursive()
        refresh = False
    returning = []
    with open("files_for_fs_recursive", "r") as fd:
        for line in fd:
            x = line.split()
            if x[1] == str(i):
                returning.append(x[0])
    return returning
    
    
            
            
            
    


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
        
        with open("query.sql", "a") as fdquer:
            print>>fdquer, query1
        #cursor.execute(query1)
        query2 = "INSERT INTO FileVersionAttr VALUES(%(fvid)s, '%(mtime)s', '%(latime)s', %(size)s, %(h)s);"%{
            'fvid': self.id,
            'mtime': timeFromSeconds(self.modification_time),
            'latime': timeFromSeconds(self.la_time),
            'size': self.size,
            'h': self.is_hidden
            }
        with open("query.sql", "a") as fdquer:
            print>>fdquer, query2
        #cursor.execute(query2)


#generator = database.getPathCursor() 
#next_object = generator.next()
fd = open("test", 'w')
#global_version = Version()
#global_version.insertIntoDatabase()
#SaveVersId()


class Folder(File):
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("not folder")
        File.__init__(self, path)
            
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

def RunGenerator2(database = database):
    i=1
    current_database_layer = database.getLayer(i)
    files_layer_generator = getFSLayerGenerator()
    current_files_layer = files_layer_generator.next()
    while len(current_database_layer)>0 or len(current_files_layer)>0:
        strange_elements = SeeDifferentsInTwoArray(current_database_layer, current_files_layer)
        print "I`m in layer " + str(i)
        for x in strange_elements[0]:
            print x+" удален"
            pass
        for x in strange_elements[1]:
            print x+" добавлен"
            try:
                File(x).insertIntoDatabase()
            except:
                pass
        i+=1
        current_database_layer = database.getLayer(i)
    current_files_layer = files_layer_generator.next()
        
        
        
        
    

#def RunGenerator():
#        folders_first=[ROOT_SNAPSHOT_FOLDER]
#        folders_last=[]
#        i=0
#        generator = database.getPathCursor()    #Получаем список путей из базы данных
#        is_new = False  #По умолчанию дамп не новый
#        try:
#            first_element = generator.next()
#            layer = int(first_element[1])
#        except:
#            is_new = True   #Если список путей пуст - значит дамп новый.
#            
#        print is_new
#        labelquit = True    #Отвечает за выход из главного цикла
#        while labelquit:     #Пока есть слои  
#            last_files = []     #Файлы из базы из текущего слоя
#            if not is_new:
#                while layer == first_element[1]:     #пока номер слоя совпадает с номером слоя файла из генератора, сохраняем этот файл 
#                    last_files.append(first_element[0])
#                    try:
#                        first_element = generator.next()
#                    except StopIteration:
#                        break
#                
#            for item in getSliceFSGenerator(folders_first):     #для каждого элемента в текущем слое
#                i+=1  
#                if item in last_files:  #Если этот элемент есть в базе значит ФАЙЛ не изменился. Удаляем из рассмотрения
#                    last_files.remove(item) 
#                else:
#                    pass#print >>fd, item + " new!"  #Иначе файл - новый
#                    
#                try:
#                    file = File(item)   # Создаем файл для пути
#                    if file.type == "folder":   #Если файл - папка то 
#                        folders_last.append(item)   #добавляем в дочерние папки
#
#                    file.insertIntoDatabase()    #и пишем в базу данных
#                except BaseException as x:
#                    print x
#                    
#            
#            if len(folders_last) == 0:  #если дочерних папок не осталось
#                labelquit = False   #выходим из цикла
#            else:
#                folders_first = folders_last[:] #иначе меняем местами исходные и дочерние папки и идем в начало цикла
#                folders_last = []
#            
#            if not is_new:
#                layer = first_element[1]    #увеличиваем слой
#                print >>fd, "Removed elements "+str(last_files) #если в проверяемом слое остались файлы, значит мы что то удалили. При этом, все дочерние элементы данных также должны быть удалены.
#
#        return i    #Возвращаем число обработанных файлов.
#        
#    
#    
    
    
    
    
    