#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 
    A Database Populator is a tool which helps you to populate your projects' database tables 
    with randomly generated content. With this tool you no longer need to write queries or to 
    compile forms by yourself wasting a lot of time before to start to work on your applications.
"""
__author__ = “Luiz F. P. Quirino”
__copyright__ = “Copyright 2020, JMIY - Just Make It Yours”
__credits__ = [“LuizQuirino”]
__license__ = “MPL 2.0”
__version__ = “0.1.0”
__maintainer__ = “LuizQuirino”
__email__ = “luizfpq@gmail.com”
__status__ = “Dev”


import random
from assets.Name import *
from assets.Varchar import *
from assets.DateTime import *

def DataLoad( dType ):
    if dType == 'FirstName':
        return  FirstName()
    if dType == 'LastName':
        return  LastName()
    if dType == 'FullName':
        return  FullName()
    if dType == 'Integer':
        return random.randint(0, 999999)
    if dType == 'CPF':
        return random.randint(10000000000, 99999999999)
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