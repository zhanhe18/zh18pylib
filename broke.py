# -*- coding:utf-8 -*-
'''
   @author  : zh
   @email   : zhanhe18@gmail.com
   @time    : 2015-01-18
   @version : 0.1
   @describe: From now on , every document from me will writing by english
              This program will find out all the password charector in 5-digit
'''

def code(length,chars,start=-1):
    '''
    got all code in chars have length digit
    all have not input check
    '''
    target = [];
    MAX = [];
    for i in range(length):
        MAX.append(chars[-1]);
        if i == start:
            target.append(chars[start]);
            continue;
        target.append(chars[0]);
    while target != MAX:
        #add number , check last number is the chars[len(chars)-1] char
        # if is , then carry over
        for i in range(len(chars)):
            if target[-1] == chars[-1]:
                # carry over and break
                target = __carryover(target,chars);
                break;
            target[-1] = chars[i];
            yield __arraytostring(target);


def __carryover(target,chars):
    for i in range(len(target)):
        i=i+1;
        if i == 1:
            target[-1] = chars[0];
            continue;
        if target[-i] == chars[-1]:
            target[-i] = chars[0];
            continue;
        else:
            index = chars.index(target[-i]);
            target[-i] = chars[index+1];
            break;
    return target


def __arraytostring(array):
    result = "";
    for i in array:
        result += str(i);
    return result;

def interval(low,height,chars):
    '''
    low digit numbers
    height dight numbers
    chars , input chars
    '''
    for i in range(low,height+1):
        for j in code(i,chars):
            yield j;


if __name__ == '__main__':
    '''
    test admin spent time
    '''
    target = 'adminadmin';
    record = 0;
    import time;
    old = time.time();
    for i in interval(10,11,[ chr(x) for x in range(97,123)]):
        if target == i:
            break;
        record += 1
    print record;
    print time.time()-old;
