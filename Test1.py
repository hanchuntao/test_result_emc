"""
Created on: Mar 21, 2017
Author: Chuntao Han

File name:
    Test1.py

Code function:
    Write a program to reverse every k nodes of a linked list.
    If the list size is not a multiple of k, then leave the remainder nodes as is.

Input example:
    Inputs:  1->2->3->4->5->6->7->8->NULL and k = 3

Correct output example:
    Output:  3->2->1->6->5->4->7->8->NULL

Error output example:
    Output:  None
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list

def reverseLinkedList( linedList, key ):
    linedListLength = len(linedList)
    if ( linedListLength == 0 ):
        print "You have input a empty list, Please input a list.\n"
        return None
    if not isinstance(key,int):
        print "please input a int for key.\n"
        return None
    elif ( key <= 0 ):
        print "The key must bigger then zero.\n"
        return None
    elif ( key > linedListLength ):
        print "the key length is large then linedListLength, so will not reverse.\n"
        return linedList
    else:
        pass

    reverseTimes = linedListLength // key
    remainder = linedListLength % key
    reverseList = []
    for i in range(reverseTimes):
        tempList = linedList[i* key: (i +1) * key ]
        tempList.reverse()
        reverseList = reverseList + tempList
    if remainder != 0:
        reverseList = reverseList + linedList[-remainder:]
    return reverseList

def main():
    linkedList = raw_input("Please input a list: ").split()
    key = input("Please input a key: ")
    print "Iutput: ",
    print linkedList
    myList = reverseLinkedList(linkedList, key)
    print "Output: ",
    print myList

def test1():
    linkedList = random_int_list(1,100,10)
    print linkedList
    key = random.randint(-10,10)
    print key
    myList = reverseLinkedList(linkedList, key)
    print "Output: ",
    print myList

def test2():
    linkedList = random_int_list(1,100,10)
    print linkedList
    key = random.uniform(-10,10)
    print key
    myList = reverseLinkedList(linkedList, key)
    print "Output: ",
    print myList

if __name__ == '__main__':
    main()
    #test1()
    #test2()