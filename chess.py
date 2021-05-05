'''
Created on May 5, 2021

@author: garycalvin
'''


def column_num(col):
    assert len(col) == 1
    assert col >= 'a' and col <= 'h'
    return ord(col) - ord('a')
