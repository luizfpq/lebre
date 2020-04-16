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

def FirstName():
    lines = open('./assets/FirstName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    return '\''+myline+'\''
def LastName():
    lines = open('./assets/LastName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    return '\''+myline+'\''
def FullName():
    lines = open('./assets/FirstName.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    lines = open('./assets/LastName.txt').read().splitlines()
    myline = myline + ' ' + random.choice(lines)
    myline = myline.split(",")[0]
    return '\''+myline+'\''