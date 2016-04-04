# -*- coding:utf-8 -*-
# zh zhanhe18@gmail.com 2015-07-09 v0.3
''' New version , new docstring .'''

# from pathos.multiprocessing import ProcessPool
from multiprocessing import Pool
import time

from util import isN

from termcolors import colorize

class Disp(object):

    def __init__(self,fun,number=4):
        self.pool = Pool(processes=number)
        self.fun = fun

    def cin(self,*args,**kwargs):
        self.pool.apply_async(self.fun,args,kwargs)

    def doing(self):
        self.pool.close()
        self.pool.join()


class Doable(object):

    def __init__(self,**kwargs):
        self.method = kwargs.get('target',None)
        sleeptime = kwargs.get('sleeptime',0)
        self.name = type(self).__name__
        self.sleeptime = sleeptime if sleeptime >= 0 else 0

    def x(self,*args,**kwargs):
        if self.method:
            self.method(*args,**kwargs)
        else:
            raise NotImplementedError

    def getSleepTime(self):
        return self.sleeptime

POT_BODY_MAX_SIZE = 50
EMPTY_WAIT_TIME = 0.1
from multiprocessing import Lock,Process

class Pot(object):

    def __init__(self,doableObj):
        self.doableObj = doableObj
        self.body = []
        self.lock = Lock()
        self.live = True

    def __full(self):
        result = (len(self.body) == POT_BODY_MAX_SIZE)
        return result

    def __empty(self):
        result = False
        with self.lock:
            result = (len(self.body) == 0)
        return result

    def __get(self):
        result = self.body[0]
        del self.body[0]
        return result

    def put(self,*args,**kwargs):
        result = False
        with self.lock:
            if not self.__full():
                self.body.append((args,kwargs))
                result = True
        return result

    def killed(self):
        self.live = False

    def run(self):
        while self.live or self.__empty():
            if self.__empty():
                time.sleep(EMPTY_WAIT_TIME)
                continue
            args,kwargs = self.__get()
            # how to handle exception ?
            # if this layer can't handle this , then raise it .
            self.doableObj.x(*args,**kwargs)
            time.sleep(self.doableObj.getSleepTime())

import threading
DISP_FAIL_WATI_TIME = 0.1

class Disp2(object):

    PROCESS = 'p'
    THREADING = 't'

    def __init__(self,doableObj,processNumber=5,potDeepin=50,method=THREADING):
        assert isinstance(doableObj,Doable)
        assert isN(processNumber)
        global POT_BODY_MAX_SIZE
        if processNumber < 1:
            processNumber = 1
        self.doableObj = doableObj
        self.processNumber = processNumber
        self.processList = []
        self.potList = []
        POT_BODY_MAX_SIZE = potDeepin
        self._fastInit(method)
        self.potsNumber = len(self.potList)
        self.dispCountNumber = 1

    def _fastInit(self,method):
        for i in range(self.processNumber):
            pot = Pot(self.doableObj)
            if method == self.PROCESS:
                process = Process(target=pot.run)
            else:
                process = threading.Thread(target=pot.run)
            self.potList.append(pot)
            self.processList.append(process)
            process.start()

    def cin(self,*args,**kwargs):
        ''' if all pots is full , sleep for a while and continue '''
        tryTime = 0
        while True:
            if tryTime == self.potsNumber:
                time.sleep(DISP_FAIL_WATI_TIME)
                tryTime = 0
                continue
            pot = self.potList[self.dispCountNumber % self.potsNumber]
            result = pot.put(*args,**kwargs)
            self.dispCountNumber += 1
            if not result:
                tryTime += 1
            else:
                break

    def killAllPots(self):
        for pot in self.potList:
            pot.killed()

    def doing(self):
        self.killAllPots()
        for process in self.processList:
            process.join()
