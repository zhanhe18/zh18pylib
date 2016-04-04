# -*- coding:utf-8 -*-
'''
   @author  : zh
   @email   : zhanhe18@gmail.com
   @time    : 2015-01-04
   @version : 0.1
   @describe: zh python util tools
'''

from numbers import Number
import sys
import time


# lambda zon
FS_SPACE_DICT = lambda x:(x[0:x.find(" ")],x[x.find(" "):].strip())

# decorater zone

def etime(func):
    ''' see the execute time of a function
    '''
    from time import time
    name = ''
    old = time();
    def wrapper(*args, **kw):
        name = func.__name__
        return func(*args, **kw)
    print name +":" + str(time()-old)
    return wrapper

# functions
def showbar(name,now,total):
    ''' 80 chars before 10 is name , last 10 is numbers
    '''
    if isinstance(name, str) and isinstance(now, Number) and isinstance(total, Number):
        tmp = "[";
        rate = now*1.0/total
        for i in xrange(int(rate*60)):
            tmp += "=";
        tmp += ">"
        for i in xrange(60-int(rate*60)):
            tmp += " ";
        tmp += "]"
        line = "%-10s : %-60s %8.2f %% %10s\r" % (name,tmp,rate*100,str(now)+"/"+str(total))
        if rate == 1:
            line += '\n'
        sys.stdout.write(line);
        sys.stdout.flush()

def getlastline(inputfile):
    import os
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize :
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint-1)*blocksize)
    elif filesize :
        dat_file.seek(0, 0)
    lines =  dat_file.readlines()
    if lines :
        last_line = lines[-1].strip()
    dat_file.close()
    return last_line

def append(path,line,fn=lambda x:str(x)+"\n"):
    if isinstance(line,basestring):
        with open(path,"a") as fw:
            fw.write(fn(line));
            fw.close();
    elif isinstance(line,set) or isinstance(line,list):
        with open(path,"a") as fw:
            for l in line:
                fw.write(fn(str(l)))
        fw.close()

def readcol(path,fn=lambda x:x.strip()):
    with open(path,"r") as fr:
        for line in fr:
            line = fn(line)
            if line is None:
                continue
            yield line

def writecol(path,col,fn=lambda x:str(x)+"\n"):
    '''
    by default there append a newline in the end
    '''
    with open(path,"w") as fw:
        for line in col:
            fw.write(fn(line))
        fw.close()


def dup(col,fn=lambda x:x.strip()):
    s = set()
    result = []
    for c in col:
        c = fn(c);
        c = c.decode("utf-8").encode("utf-8")
        if c not in s:
            s.add(c)
            result.append(c)
    return result

def dup_t(col,fn=lambda x:x.strip()):
    s = set()
    result = []
    for c in col:
        c = fn(c);
        if c not in s:
            s.add(c)
        else:
            result.append(c);
    return result



def getdict(path,fn=lambda x:(x,x)):
    d = {};
    with open(path,"r") as fid:
        for line in fid:
            key,value = fn(line);
            d[key] = value;
    return d;

def splitfile(path,num):
    ''' This function has some problem , had not fixed .
        * DO NOT USE *
    '''
    line = getFLN(path)
    import os
    if not isinstance(num,Number) or not os.path.exists(path):
        raise Exception;
    l = readcol(path);
    path_dot = path.rfind(".")
    path_last_slash = path.rfind("/");
    suffix = None
    if path_dot > path_last_slash:
        suffix = path[path_dot+1:].strip()
        path = path[0:path_dot].strip()
    sep = line/num;
    record = 0;
    tmp = []
    for l1 in l:
        if record%sep == 0 and record != 0:
            writecol(path+"_"+str(record/sep)+("."+suffix if suffix is not None else ""),tmp);
            tmp = []
        tmp.append(l1)
        record += 1
    if len(tmp) != 0:
        writecol(path+"_"+str(record/sep)+("."+suffix if suffix is not None else ""),tmp);

def getFLN(path):
    count = -1
    for count, line in enumerate(open(path, 'rU')):
        pass
    count += 1
    return count

def getdirfiles(path):
    if isinstance(path,str):
        import os;
        dirs = os.listdir(path);
        return dirs;
    else:
        return None;


import hashlib
def md5(s):
    if isinstance(s,str):
        md5 = hashlib.md5(s.encode('utf-8')).hexdigest()
        return md5;
    return None


def remove_equal_element(l,equal=""):
    length = len(l)
    if length == 0:return l
    remove = []
    for x in range(len(l)):
        # here may be use regular expression
        if l[x] == equal:
            remove.append(x)
    remove.sort(reverse=True)
    for r in remove:
        del l[r]
    return l


def isN(x):
    ''' if x is a number , return int number , else return None '''
    try:
        x = int(x)
        return True
    except:
        return False


def find_leaf_folder(path):
    import os
    folders = os.popen('find '+path+' -type d').read().split("\n")
    leaf_folder = []
    for folder in folders:
        if folder.strip() == "" : continue
        isdir = False
        for f in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,f)):
                isdir = True
                break
        if isdir:
            continue
        leaf_folder.append(folder)
    return leaf_folder

def find_type_file(path,t):
    import os
    files = os.popen('find '+path+' -name "'+t+'"').read().split("\n")
    result = []
    for f in files:
        if f.strip() == "":continue
        result.append(f)
    return result

def loadAsList(path,fn=lambda x:x):
    l = readcol(path)
    result = []
    for l1 in l:
        result.append(fn(l1))
    return result

def loadAsOneLineString(path):
    result = ""
    with open(path,'r') as fr:
        result = fr.read()
        fr.close()
    result = result.replace("\n","")
    return result

def loadAsDict(path,fn=lambda x:(x,x)):
    l = readcol(path)
    result = {}
    index = 0
    for l1 in l:
        key,value = fn(l1)
        if value is None:
            result[key] = index
            index += 1
        else:
            result[key] = value
    return result


def wrapColStr(col,wrapstr,before=True):
    if not isinstance(col,(set,list)):
        return None
    sflag = False
    if isinstance(col,set):
        result = set()
        sflag = True
    else:
        result = []
    for c in col:
        if sflag:
            result.add(wrapstr+c if before else c+wrapstr)
        else:
            result.append(wrapstr+c if before else c+wrapstr)
    return result
