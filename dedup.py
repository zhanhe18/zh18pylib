# -*- coding:utf-8 -*-
# zh zhanhe18@gmail.com 2015-06-09 v0.1
''' Something dedup '''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import numpy
from PIL import Image
from math import sqrt,pi,cos

eight = (8,8)
thirty2 = (32,32)
same_image_value_limit = 10

numpy.set_printoptions(threshold='nan')

def image_ahash(orimage,compimage):
    '''  Average Hash '''
    try:
        orimage = Image.open(orimage)
        compimage = Image.open(compimage)
    except Exception as e:
        return None
    # resize to 8 * 8
    resize_width = eight
    orimage = orimage.resize(resize_width)
    compimage = compimage.resize(resize_width)
    # get gray value
    orimage = _get_gray_value(orimage)
    compimage = _get_gray_value(compimage)
    # get orimage average
    orimage_avg =  _get_average(orimage)
    compimage_avg = _get_average(compimage)
    # get findgerprint
    orimage_fingerprint = _get_fingerprint(orimage,orimage_avg)
    compimage_fingerprint = _get_fingerprint(compimage,compimage_avg)
    return __hamming_distance(orimage_fingerprint,compimage_fingerprint) == 0


def image_fingerprint(image):
    try:
        image = Image.open(image)
    except:
        return None
        # resize to 8 * 8
    resize_width = eight
    image = image.resize(resize_width)
    # get gray value
    image = _get_gray_value(image)
    # get orimage average
    image_avg = _get_average(image)
    # get findgerprint
    image_fingerprint = _get_fingerprint(image,image_avg)
    return image_fingerprint

def __hamming_distance(origin_fingerprint,compare_fingerprint):
    ''' Accept two byte [01]{64} , compare two byte number hamming
    distance '''
    count = 0
    for i in range(64):
        ori = origin_fingerprint & (1 << i)
        comp = compare_fingerprint & (1 << i)
        if ori != comp:
            count += 1
    return count


def _get_gray_value(image):
    ''' image is Image type '''
    im = numpy.array(image.convert("L"),'f')
    return im

def _get_average(image_array):
    ''' image is numpy array '''
    height,width = image_array.shape
    count = 0
    for dots in image_array:
        for dot in dots:
            count += dot
    return count/(width*height)

def __compute_gray_value(pixel):
    ''' 256 order , and I dont know why it is 256 '''
    red = (pixel >> 16) & 0xff
    green = (pixel >> 8) & 0xff
    blue = pixel & 0xff
    return 0.3 * red + 0.59 * green + 0.11 * blue

def _get_fingerprint(image_array,average):
    y,x = image_array.shape
    fingerprint = 0
    index = 0
    for y_index in range(y):
        for x_index in range(x):
            tmp_number = 1 \
                if image_array[y_index][x_index] >= average else 0
            fingerprint += tmp_number << index
            index += 1
    return fingerprint


def image_phash(orimage,compimage):
    ''' p hash '''

    def _get_8_from_32(dct_array):
        result = numpy.zeros((8,8))
        y,x = dct_array.shape
        for y_index in range(y):
            if y_index > 7 :break
            for x_index in range(x):
                if x_index > 7:break
                result[y_index][x_index] = dct_array[y_index][x_index]
        return result
    try:
        orimage = Image.open(orimage)
        compimage = Image.open(compimage)
    except Exception as e:
        return None
    # resize to 32 * 32
    resize_width = thirty2
    orimage = orimage.resize(resize_width)
    compimage = compimage.resize(resize_width)
    # get gray value
    orimage_gray = _get_gray_value(orimage)
    compimage_gray = _get_gray_value(compimage)
    # get dct value 8x8 from 32x32
    # -- use 32x32 directly
    # orimage_gray_dct = _get_8_from_32(dct(orimage_gray))
    orimage_gray_dct = dct(orimage_gray)
    # compimage_gray_dct = _get_8_from_32(dct(compimage_gray))
    compimage_gray_dct = dct(compimage_gray)
    # get average
    orimage_avg = _get_average(orimage_gray_dct)
    compimage_avg = _get_average(compimage_gray_dct)
    # get fingerprint
    orimage_fingerprint = _get_fingerprint(orimage_gray_dct,orimage_avg)
    compimage_fingerprint = _get_fingerprint(compimage_gray_dct,compimage_avg)
    hamming_distance = __hamming_distance(orimage_fingerprint,compimage_fingerprint)
    # print hamming_distance
    return hamming_distance == 0

def dct(image_array):
    ''' dct , Only accept a 'N x N' array'''
    dim,_ = image_array.shape
    def _make_zero_narray(dim):
        return numpy.zeros((dim,dim))
    zero = _make_zero_narray(dim)
    for i in range(dim):
        for j in range(dim):
            if i == 0:
                a = sqrt(1.0/dim)
            else:
                a = sqrt(2.0/dim)
            zero[i][j] = a*cos(pi*(j+0.5)*i*1.0/dim)
    # Y = zero*image_array*zero^T
    Y = numpy.dot(zero,image_array)
    Y = numpy.dot(Y,numpy.transpose(zero))
    return Y


if __name__ == '__main__':
    import time
    old = time.time()
    p = '/home/public/javaproject/SimilarPhotoHunter/origin/origin.jpg'
    comp = '/home/public/javaproject/SimilarPhotoHunter/images/similar_pic.jpg'
    print image_phash(p,comp)
    print time.time()-old
