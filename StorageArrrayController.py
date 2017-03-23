"""
Created on: Mar 21, 2017
Author: Chuntao Han

File name:
    StorageArrayController.py

Code function:
    Provie web service API of all the lun operation for the users
"""

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import string

from StorageArrayServer import StorageArray, LunOperation

from flask import Flask, render_template, request
app = Flask(__name__)

default_storage_array = StorageArray(100)

#@app.route("/")
#def index():
#    return render_template("index.html")

@app.route("/create_lun", methods=["PUT"])
def create_lun():
    '''
    create one or multiple LUNs
    :return:
    '''
    lun_size = request.json["lunsize"]
    lun_number = request.json["lunnumber"] or 1

    if "." in lun_size:
        lun_size = string.atof(lun_size)
    else:
        lun_size = string.atoi(lun_size)

    if "." in lun_number:
        lun_number = string.atof(lun_number)
    else:
        lun_number = string.atoi(lun_number)

    lun_info= {}

    if not isinstance(lun_number, int):
        print "The LUN number must input a int"
        return json.dumps([lun_info, {1: "The input LUN number is not int"}])
    elif lun_number <= 0:
        print "The LUN number must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN number less then 0"}])

    unused_size = default_storage_array.storage_array_unused_size
    if not isinstance(lun_size, int):
        print "The LUN size must input a int"
        return json.dumps([lun_info, {1: "The input LUN size is not int"}])
    elif lun_size <= 0:
        print "The LUN size must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN size less then 0"}])
    elif unused_size < lun_size * lun_number:
        print "The sum of input LUNs size must less then unused storage array size"
        return json.dumps([lun_info, {3: "The input LUN size is greater then unused storage array size"}])

    for lun_index in range(lun_number):
        create_lun_info = LunOperation(default_storage_array)
        create_lun_info.create_lun(lun_size)
        default_storage_array.storage_array_exist_luns[create_lun_info.lunId] = create_lun_info.lunSize
        lun_info[create_lun_info.lunId] = create_lun_info.lunSize
        print "The LUN create successfully"

    return json.dumps([lun_info, {0: "The LUN create successfully"}])

@app.route("/delete_lun", methods=["DELETE"])
def delete_lun():
    '''
    Delete the LUN in the storage array
    :return:
    '''

    lun_id = request.json["lunid"]
    print lun_id
    if "." in lun_id:
        lun_id = string.atof(lun_id)
    else:
        lun_id = string.atoi(lun_id)

    lun_info= {}
    exist_luns = default_storage_array.storage_array_exist_luns

    if not isinstance(lun_id, int):
        print "The LUN ID must input a int"
        return json.dumps([lun_info, {1: "The input LUN ID is not int"}])
    elif lun_id <= 0:
        print "The LUN ID must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN size less then 0"}])
    elif exist_luns.get(str(lun_id)):
        delete_lun_info = LunOperation(default_storage_array)
        lun_info[lun_id] = exist_luns.get(str(lun_id))
        delete_lun_info.delete_lun(lun_id)
        print "Delete the LUN in the storage array seccussfully"
    else:
        return json.dumps([lun_info, {3: "Cannot find the LUN in the storage array"}])
    return json.dumps([lun_info, {0: "Delete the LUN in the storage array seccussfully"}])

@app.route("/resize_lun", methods=["POST"])
def resize_lun():
    '''
    resize the LUN in the storage array
    :return:
    '''
    lun_id = request.json["lunid"]
    lun_size = request.json["lunsize"]

    if "." in lun_id:
        lun_id = string.atof(lun_id)
    else:
        lun_id = string.atoi(lun_id)

    if "." in lun_size:
        lun_size = string.atof(lun_size)
    else:
        lun_size = string.atoi(lun_size)

    lun_info= {}

    if not isinstance(lun_id, int):
        print "The LUN ID must input a int"
        return json.dumps([lun_info, {1: "The input LUN number is not int"}])
    elif lun_id <= 0:
        print "The LUN ID must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN number less then 0"}])

    unused_size = default_storage_array.storage_array_unused_size
    exist_luns = default_storage_array.storage_array_exist_luns
    if not isinstance(lun_size, int):
        print "The LUN size must input a int"
        return json.dumps([lun_info, {1: "The input LUN size is not int"}])
    elif lun_size <= 0:
        print "The LUN size must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN size less then 0"}])
    elif not exist_luns.get(str(lun_id)):
        print "Cannot find the LUN in the storage array"
        return  json.dumps([lun_info, {3: "Cannot find the LUN in the storage array"}])
    elif unused_size < lun_size :
        print "The LUN size must less then unused storage array size"
        return json.dumps([lun_info, {3: "The input LUN size is greater then unused storage array size"}])
    else:
        lun_info[lun_id] = lun_size
        resize_lun_info = LunOperation(default_storage_array)
        resize_lun_info.resize_lun(lun_id,lun_size)
        print "Resize the LUN seccussfully"
    return json.dumps([lun_info, {0: "Resize the LUN seccussfully"}])

@app.route("/list_lun", methods=["GET"])
def list_lun():
    '''
    list the size of a LUN
    :return:
    '''
    lun_id = request.json["lunid"]
    if "." in lun_id:
        lun_id = string.atof(lun_id)
    else:
        lun_id = string.atoi(lun_id)

    lun_info= {}
    exist_luns = default_storage_array.storage_array_exist_luns

    if not isinstance(lun_id, int):
        print "The LUN ID must input a int"
        return json.dumps([lun_info, {1: "The input LUN ID is not int"}])
    elif lun_id <= 0:
        print "The LUN ID must greater then 0"
        return json.dumps([lun_info, {2: "The input LUN size less then 0"}])
    elif exist_luns.get(str(lun_id)):
        lun_info[lun_id] = exist_luns.get(str(lun_id))
        print "List LUN information seccussfully"
    else:
        return json.dumps([lun_info, {3: "Cannot find the LUN in the storage array"}])
    return json.dumps([lun_info, {0: "List LUN information seccussfully"}])

@app.route("/storage_array_persistence", methods=["GET"])
def storage_array_persistence():
    '''
    storage array persistence,store all the LUN and storage array to a file
    :return:
    '''
    all_size =  default_storage_array.storage_array_size
    unused_size = default_storage_array.storage_array_unused_size
    exist_luns = default_storage_array.storage_array_exist_luns
    persistence_file = open("persistence_file.txt", "w")
    persistence_file.write( "all_size: " + str(all_size) + "\n"+ "unused_size: "
                            + str(unused_size) + "\nexist_luns: \n".exist_luns)
    persistence_file.close()
    return json.dumps([{'0':'Persistence the storage array and LUN info seccuessfully'}])

if __name__ == "__main__":
    app.run()
