#-*- coding: utf-8 -*-
from classes.main import *

def DoFile(path):
    """Создает пустой файл"""
    with open(os.path.join(TEST_PATH_PREFIX, path), "w"):
        pass

def DoPath(path):
    """Создает все нужные папки для обеспечения правильности пути path"""
    elements = path.split("/")
    current_path = ''
    prev_path = TEST_PATH_PREFIX
    for x in elements[:-1]:
        current_path = os.path.join(prev_path, x)
        if not os.path.exists(current_path):
            os.mkdir(current_path)
        elif not os.path.isdir(current_path):
            raise ValueError("double path")
        prev_path = current_path
    DoFile(path)
    



def GenerateFS(count_files, max_height, pref=''):
    """Генерирует файл со списком директорий"""
    fd = open("run_generator_test_fs", "a")
    for x in range(count_files):
        path = pref
        for y in range(ran.randrange(1, max_height, 1)):
            path=os.path.join(path, hex(ran.randrange(10**60, 10**65,1)))
        print>>fd,  path

def DoFS(count_files, max_height):
    """Генерирует файловую систему. max_height - максимальная глубина вложения папок"""
    with open('run_generator_test_fs', "w"):
        pass
    print "starting to do FS..."
    if len(os.listdir(TEST_PATH_PREFIX))!=0:
        print "Remove TEST_DIR please. Exiting."
        exit()
    GenerateFS(count_files, max_height)
    print "FS plane was generated"
    with open('run_generator_test_fs') as fd:
        for line in fd:
            DoPath(line[:-1])
    print "FS was born"
    if ROOT_SNAPSHOT_FOLDER == TEST_PATH_PREFIX:
        main()
    else:
        raise ValueError("RSF and TPP must be the same")
    print "FS Done!"

last_test_id = int(Config("last_test_id").value)
files = []
with open('run_generator_test_fs') as fd:
        for line in fd:
            files.append(line[:-1])
            
import subprocess as su
def DropRecursive(path):
    su.call(["rm", "-r", path])
    if path == TEST_PATH_PREFIX:
        os.mkdir("test_folder")


def getRandomPrefix(path):
    elements = path.split("/")
    elements = elements[:ran.randrange(1,len(elements))]
    ret = ""
    for x in elements:
        ret+="/"+x
    return ret[1:]

def DoOneTest(count_add, count_remove):
    """Генерирует один список файлов"""
    with open("run_tests/test"+str(last_test_id), "w") as fd:
        for x in range(count_remove):
            start_path = getRandomElement(files, delete = True).split("/")
            for i in range(0, ran.randrange(1, len(start_path), 1)): pass

#DropRecursive(TEST_PATH_PREFIX)    
#DoFS(1000, 5)
print getRandomPrefix(files[0])

    
    