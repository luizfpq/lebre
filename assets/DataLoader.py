#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    A Database Populator is a tool which helps you to populate your projects' database tables
    with randomly generated content. With this tool you no longer need to write queries or to
    compile forms by yourself wasting a lot of time before to start to work on your applications.
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
from assets.TextTypes import *
from assets.DateTime import *

def DataLoad( dType ):
    if dType == 'FirstName':
        return  FirstName()
    if dType == 'LastName':
        return  LastName()
    if dType == 'FullName':
        return  FullName()
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



    # Set a default dataType, wich returns itself, to set default values on fields
    # Model
    #      Default:'00235'
    # Return: '00235'
    # Model
    #      Default:00235
    # Return: 00235

    if "Default" in dType:
        return dType.split(":")[1]
