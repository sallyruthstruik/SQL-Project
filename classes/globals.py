count_files = 0
count_files_cur = 0
import os, datetime, time

def Inc(*args):
    """
        args: count_files, count_files_cur 
    """
    if args[0] == "count_files":
        global count_files
        count_files+=1
    if args[0] == "count_files_cur":
        global count_files_cur
        count_files_cur+=1
        
def Get(what):
    if what == 'count_files':
        return count_files
    if what == 'count_files_cur':
        return count_files_cur
  
def getPathLen(path):
    return len(path.split("/"))

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
    
def timeFromSeconds(t):
    return datetime.datetime(*time.localtime(time.time())[:6])

def SeeDifferentsInTwoArray(arr1, arr2):
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
    
