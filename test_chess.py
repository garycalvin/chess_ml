'''
Created on May 5, 2021

@author: garycalvin
'''
import unittest
import chess as ch


class TestChess(unittest.TestCase):

    def test_column_num(self):
        result = ch.column_num('a')
        assert result == 0
        result = ch.column_num('h')
        assert result == 7


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()
