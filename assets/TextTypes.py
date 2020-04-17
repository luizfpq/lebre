#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 
    A Database Populator is a tool which helps you to populate your projects' database tables 
    with randomly generated content. With this tool you no longer need to write queries or to 
    compile forms by yourself wasting a lot of time before to start to work on your applications.


    Aways return strings in this format '\''+randChar+'\'', to pass the '' to variable


"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "0.1.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


import random
import string

def random_char(y):

    randChar = ''.join(random.choice(string.ascii_letters) for x in range(y))
    return '\''+randChar+'\''

def CPF():
    block_1 = str(randint(0, 999)).rjust(3, "0")
    block_2 = str(randint(0, 999)).rjust(3, "0")
    block_3 = str(randint(0, 999)).rjust(3, "0")
    block_4 = str(randint(0, 99)).rjust(2, "0")
    return '\''+block_1+'.'+block_2+'.'+block_3+'-'+block_4+'\''


def FirstName():
    lines = open('./datasources/FirstNameBR.txt').read().splitlines()
    myline = random.choice(lines).capitalize()
    myline = myline.split(",")[0].capitalize()
    return '\''+myline+'\''

def LastName():
    lines = open('./datasources/LastNameBR.txt').read().splitlines()
    myline = random.choice(lines).capitalize()
    myline = myline.split(",")[0]
    return '\''+myline+'\''

def FullName():
    lines = open('./datasources/FirstNameBR.txt').read().splitlines()
    myline = random.choice(lines).capitalize()
    myline = myline.split(",")[0]
    lines = open('./datasources/LastNameBR.txt').read().splitlines()
    myline = myline + ' ' + random.choice(lines).capitalize()
    myline = myline.split(",")[0]
    return '\''+myline+'\''

def Address():
    lines = open('./datasources/AddressTypeBR.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0].capitalize()

    lines = open('./datasources/FirstNameBR.txt').read().splitlines()
    myline = myline + ' ' + random.choice(lines).capitalize()
    myline = myline.split(",")[0]
    
    #lines = open('./datasources/LastNameBR.txt').read().splitlines()
    #myline = myline + ' ' + random.choice(lines)
    #myline = myline.split(",")[0]
    return '\''+myline+'\''

def StateProvince():
    lines = open('./datasources/StateProvinceBR.txt').read().splitlines()
    myline = random.choice(lines)
    myline = myline.split(",")[0]
    return '\''+myline+'\''