# -*- coding:utf-8 -*-
# zh zhanhe18@gmail.com 2015-07-19 v0.2
''' Multiple Dealer and Sender module '''

import logging
import os,sys,threading
import zmq
from mul import Disp
from pathos.multiprocessing import ProcessPool

class Dealer(object):
    pass

class Worker(object):

    argsNumber = 0
    address = 0

    def __init__(self,address,argsNumber):
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(address)
        self.argsNumber = argsNumber
        number argsNumber - 1
        while number > 0:
            self.socket.send('',2)
            number -= 1
        self.socket.send('worker')
        self.running = True
        self.thread = None

    def dojob(self,*a):
        raise NotImplementedError

    def start(self):
        self.thread = threading.Thread(target=self.__receive)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def __receive(self):
        while self.running:
            tmpNumber = self.argsNumber
            argsReceviedList = []
            while tmpNumber > 0:
                args = self.socket.recv()
                argsReceviedList.append(args)
                tmpNumber -= 1
            tmpList = list(argsReceviedList)
            self.dojob(*tmpList)


class Router(object):

    def __init__(self,port,workercls):
        self.port = port
        self.context = zmq.Context.instance()
        self.router = self.context.socket(zmq.ROUTER)
        self.router.bind('tcp://*:'+str(self.port))
        self.running = True
        self.workercls = workercls
        self.argsNumber = workercls.argsNumber
        # {rid:[]}
        self.workers = {}
        self.disp.dispIndex = 0

    def start(self):
        log.info('%s had started at PORT %d' %
                 (type(self).__name__,self.port))
        self.thread = threading.Thread(target=self.__receive)
        self.thread.start()

    def close(self):
        self.thread.join()


    def __receive(self):
        while self.running:
            tmpNumber = self.argsNumber
            argsReceviedList = []
            while tmpNumber > 0:
                args = self.socket.recv()
                argsReceviedList.append(args)
                tmpNumber -= 1
            tmpList = list(argsReceviedList)
            self.disp(*tmpList)

    def disp(self,*args):
        # dispatcher to workers .
        # resigter task in workers list
        if not self._isWorker(*args):
            self._disp(*args)

    def _disp(self,*args):
        rid = args[0]
        # if rid is from worker , send it to request dealer
        # else send it to worker
        if rid in self.workers.keys():

    def _isWorker(self,*args):
        rid = args[0]
        result = False
        for arg in args[1:]:
            if arg == 'worker':
                result = True
                self.worker[rid] = []
                break
        return result
