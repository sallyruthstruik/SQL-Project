#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb.connections as connection
from classes.config import *


class MyDatabase(connection.Connection):
    def __init__(self, *args, **kwargs):
        connection.Connection.__init__(self, *args, **kwargs)
        self.myCursor = self.cursor()
        self.myCursor.execute("set names utf8;")
    
    def clear(self):
        #self.myCursor.execute("delete from File; delete from FileVersion; delete from FileVersionAttr; delete from Versions")
        pass
    
    def getPathCursor(self):
        self.myCursor.execute("select directory_path from File;")
        for x in self.myCursor.fetchall():
            yield x[0]
        
database = MyDatabase(HOST, USER, PASS, DATABASE_NAME)
cursor = database.myCursor

class Config:
    def __init__(self, key):
        self.key = key
        cursor.execute("SELECT `value` FROM KeyValue WHERE `key` = '%s';"%(key))
        try:
            self.value = cursor.fetchall()[0][0]
        except:
            self.value = 0
    
    def insertIntoDatabase(self):
        try:
            cursor.execute("INSERT INTO KeyValue VALUES('%(key)s', '%(val)s');"%{'key': self.key, 'val': self.value})
        except:
            cursor.execute("UPDATE KeyValue SET `value` = '%(val)s' WHERE `key` = '%(key)s';"%{'key': self.key, 'val': self.value})
        database.commit()
    def __str__(self):
        return self.key + " - "+self.value

        
        