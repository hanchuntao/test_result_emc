"""
Created on: Mar 21, 2017
Author: Chuntao Han

File name:
    StorageArrayServer.py

Code function:
    This contains some functions to control the LUNs
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime;
import random;


def CreateId():
    # Create the current time
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # Create randon int n, 0<=n<=100
    randomNum=random.randint(0,100);
    if randomNum<=10:
        randomNum=str(0)+str(randomNum)
    uniqueNum=str(nowTime)+str(randomNum)
    return uniqueNum