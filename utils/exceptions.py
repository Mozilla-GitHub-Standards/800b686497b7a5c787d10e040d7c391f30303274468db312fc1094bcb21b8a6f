#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
dictionary
'''

class AutodomainError(Exception):
    '''
    AutodomainError
    '''
    def __init__(self, message):
        '''
        __init__
        '''
        self._message = message
        super(AutodomainError, self).__init__(message)

    @property
    def name(self):
        '''
        name
        '''
        return self.__class__.__name__

    @property
    def message(self):
        '''
        message
        '''
        return self._message
