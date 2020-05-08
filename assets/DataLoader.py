#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Dataloader defines data types and load them all from datasource files
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "0.1.1"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


import random
''' TextTypes reponses for all nom numeric data'''
from assets.TextTypes import *
''' DateTime responses for all DateTime based data'''
from assets.DateTime import *

def DataLoad( dType ):
    if dType == 'FirstName':
        return  FirstName()
    if dType == 'LastName':
        return  LastName()
    if dType == 'FullName':
        return  FullName()
    if dType == 'InitName':
            return  InitName()
    if dType == 'Serial':
        return  'serial'
    if 'Integer' in dType:
        return random.randint(int(dType.split(":")[1]), int(dType.split(":")[2]))
    if dType == 'CPF':
        return CPF()
    # Use: Varchar:size
    if "Varchar" in dType:
        return random_char(int(dType.split(":")[1])).upper()
    if dType == 'Date':
        return random_date("1/1/1970", "1/1/2000", random.random())
    if dType == 'Address':
        return Address()
    if "StateProvince" in dType:
        return StateProvince()



    # Set a default dataType, wich returns itself, to set default values on fields
    # Model
    #      Default:'00235'
    # Return: '00235'
    # Model
    #      Default:00235
    # Return: 00235

    if "Default" in dType:
        return dType.split(":")[1]
