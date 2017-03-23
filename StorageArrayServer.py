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


from Config import CreateId

class StorageArray(object):
    '''
    the opereation about storage array
    '''
    def __init__(self, allsize):
        '''
        Init storage array
        :param size:
        '''
        self.storage_array_size = allsize
        self.storage_array_unused_size = self.storage_array_size
        self.storage_array_exist_luns = {}

    def storage_size_assign(self, lunid, lunsize):
        '''
        Assign the storage to the LUN that need to create
        :param lunid:
        :param lunsize:
        :return: None / True
        '''
        self.storage_array_unused_size -= lunsize
        self.storage_array_exist_luns[str(lunid)] = lunsize

    def storage_size_restore(self, lunid):
        '''
        when delete the LUN, restore the storage to the storage array
        :param lunid:
        :return:
        '''
        restore_lun_size = self.storage_array_exist_luns[str(lunid)]
        self.storage_array_exist_luns.pop(str(lunid))
        self.storage_array_unused_size += restore_lun_size

class LunOperation(object):
    '''
    The operation about the LUN
    '''
    def __init__(self, storagearray):
        '''
        Init the LUN
        :param storagearray:
        '''
        self.storageArray = storagearray
        self.lunSize = 0
        self.lunId = CreateId()

    def create_lun(self, lunsize):
        '''
        Create a LUN, and assign storage to the LUN
        :param size:
        :return:
        '''
        self.lunSize = lunsize
        self.storageArray.storage_size_assign(self.lunId, self.lunSize)

    def delete_lun(self, lunid):
        '''
        Delete the LUN in the storage array
        :param lunid:
        :return:
        '''
        self.lunId = lunid
        self.storageArray.storage_size_restore(self.lunId)

    def resize_lun(self, lunid, lunsize):
        '''
        Resize the LUN in the storage array
        :param lunid:
        :param lunsize:
        :return:
        '''

        self.lunSize = lunsize
        before_lun_size =  self.storageArray.storage_array_exist_luns.get(str(lunid))
        reassign_lun_size = self.lunSize - before_lun_size
        self.storageArray.storage_size_assign(self.lunId, reassign_lun_size)
        self.storageArray.storage_array_exist_luns[str(lunid)] = self.lunSize


