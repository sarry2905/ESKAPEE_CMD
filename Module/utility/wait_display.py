# -*- coding: utf-8 -*-
"""
Created on Sun May  1 19:41:43 2022

@author: Sarthak
"""
import time
from itertools import cycle


def print_dot(n=0):
    if n > 0:
        count = 0
        for dot in cycle('...'):
            for rep in range(1, 4):
                print('\r', dot * rep, sep='', end='', flush=True)
                time.sleep(n / 10)
            print('\r', '   ', sep='', end='', flush=True)
            count += 1
            if count == n:
                print('\r', '', sep='', end='', flush=True)
                return
    else:
        print('\r', '', sep='', end='', flush=True)
        return


def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)
    time.sleep(0.001)
    return
