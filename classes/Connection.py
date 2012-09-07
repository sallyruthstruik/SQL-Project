#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb.connections as connection
from classes.config import *
from classes.globals import *


class MyDatabase(connection.Connection):
    """Описывает всевозможные методы, запрашиваемые у базы данных"""
    def __init__(self, *args, **kwargs):
        connection.Connection.__init__(self, *args, **kwargs)
        self.myCursor = self.cursor()
        self.myCursor.execute("set names utf8;")
    
    def getPathCursor(self):
        """
            returns generator of files pathes"""

        self.myCursor.execute("select directory_path, pathlen from File order by pathlen;")
        for x in self.myCursor.fetchall():
            yield x
            
    def getFirstPathLength(self):
        """returns minimal pathlen in database"""
        self.myCursor.execute("SELECT pathlen from File order by pathlen limit 1;")
        return self.myCursor.fetchall()[0][0]
      
    def getLayer(self, number):
        i=0
        generator = self.getPathCursor()
        prefix_length = self.getFirstPathLength()
        output_layer = []
        while True:
            try:
                element = generator.next()
            except StopIteration:
                break
            if element[1]<prefix_length+number-1:
                pass
            elif element[1] == prefix_length+number-1:
                output_layer.append(element[0])
            else:
                break
            
        return output_layer
        
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

        
        