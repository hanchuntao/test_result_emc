"""
Created on: Mar 21, 2017
Author: Chuntao Han

File name:
    storageArrayTestCases.py

Code function:
    This class contain all the test cases for testing the storage array simulator web service API

Test cases:
    1. Create one or multiple LUNs.
    2. Remove a LUN.
    3. Resize a LUN.
    4. Retrieve the information (size) of a LUN.
    5. Concurrent requests.(the featuren not finished, so hold on this test )
    6. Data persistence.

"""

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib,urllib2
import json
import random

class StorageArrayAPIUnitTest():
    def setUp(self):
        '''
        the set up operation for all the unit test
        :return:
        '''
        print "Running set up for storage array simulator web service API"
        global lunsize, lunresize, lunnumber, exist_luns
        lunsize = 3
        lunresize = 7
        lunnumber = 10
        exist_luns = []


    def tearDown(self):
        '''
        The teardown operation for all the unit test
        :return:
        '''
        print "Running teardown for storage array simulator web service API"

    def test_create_lun(self):
        '''
        Create one or multiple LUNs
        :return:
        '''
        global exist_luns
        serv_create_url = "http://127.0.0.1:5000/create_lun"
        create_data = {"lunsize":lunsize,"lunnumber":lunnumber}
        url_create_data = json.dumps(create_data)
        request = urllib2.Request(url=serv_create_url, data=url_create_data)
        request.get_method = lambda: 'PUT'
        resp = urllib2.urlopen(request)
        create_resp = json.loads(resp.read())
        assert create_resp[1].keys()[0] == 0,"Create LUN's fail"

    def test_delete_lun(self):
        '''
        :return:
        '''
        global exist_luns
        serv_delete_url = "http://127.0.0.1:5000/delete_lun"
        randomNum = random.randint(0, len(exist_luns)-1)
        lunid = exist_luns[randomNum]
        delete_data = {"lunid":lunid}
        usl_delete_data = urllib.urlencode(delete_data)
        full_delete_url = urllib2.Request(serv_delete_url, usl_delete_data)
        resp = urllib2.urlopen(full_delete_url)
        delete_resp = json.loads(resp.read())
        exist_luns -= delete_resp[0].keys()
        assert delete_resp[1].keys()[0] == 0, "Delete LUN fail"

    def test_resize_lun(self):
        '''
        Resize a LUN
        :return:
        '''
        serv_resize_url = "http://127.0.0.1:5000/resize_lun"
        randomNum = random.randint(0, len(exist_luns)-1)
        lunid = exist_luns[randomNum]
        resize_data = {"lunid":lunid,"lunsize":lunresize}
        usl_resize_data = urllib.urlencode(resize_data)
        full_resize_url = urllib2.Request(serv_resize_url, usl_resize_data)
        resp = urllib2.urlopen(full_resize_url)
        resize_resp = json.loads(resp.read())
        assert resize_resp[1].keys()[0] == 0, "Resize LUN fail"

    def test_list_lun(self,lunid):
        '''
        Retrieve the information (size) of a LUN.
        :param lunid:
        :return:
        '''
        serv_list_url = "http://127.0.0.1:5000/list_lun"
        randomNum = random.randint(0, len(exist_luns)-1)
        lunid = exist_luns[randomNum]
        list_data = {"lunsize":lunid}
        usl_list_data = urllib.urlencode(list_data)
        full_list_url = urllib2.Request(serv_list_url, usl_list_data)
        resp = urllib2.urlopen(full_list_url)
        list_resp = json.loads(resp.read())
        assert list_resp[1].keys()[0] == 0, "List LUN fail"

    def test_storage_array_persistence(self):
        '''
        Data persistence.
        :return:
        '''
        serv_persistence_url = "http://127.0.0.1:5000/storage_array_persistence"
        full_persistence_url = urllib2.Request(serv_persistence_url)
        resp = urllib2.urlopen(full_persistence_url)
        persistence_resp = json.loads(resp.read())
        assert persistence_resp[1].keys()[0] == 0, "Data persistence fail"

if __name__ == "__main__":
    api_unit_test = StorageArrayAPIUnitTest()
    api_unit_test.setUp()
    api_unit_test.test_create_lun()
    #api_unit_test.test_delete_lun()
    #api_unit_test.test_resize_lun()
    #api_unit_test.test_list_lun()
    #api_unit_test.test_storage_array_persistence()
    #api_unit_test.tearDown()
