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
__version__ = "0.2.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


from random import randint
import random
import string

def random_char(y):
    randChar = ''.join(random.choice(string.ascii_letters) for x in range(y))
    return '\''+randChar+'\''

def search_string_in_file(file_name, string_to_search):
    """
        Search for the given string in file and return lines containing that string,
        along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if str(string_to_search) in str(line):
            # If yes, then add the line number & line as a tuple in the list
                list_of_results.append(line)
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results[0]

# TODO generate valid cpf
def CPF(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        block_1 = str(randint(0, 999)).rjust(3, "0")
        block_2 = str(randint(0, 999)).rjust(3, "0")
        block_3 = str(randint(0, 999)).rjust(3, "0")
        block_4 = str(randint(0, 99)).rjust(2, "0")
        dataList.append('\''+block_1+'.'+block_2+'.'+block_3+'-'+block_4+'\'')
    return dataList

#def InitName(recordsToGenerate, dType, ValueDict):
#    dataList = []
#    for i in range(recordsToGenerate):
#        
#    return dataList

def FirstName(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        lines = open('./datasources/FirstNameBR.txt').read().splitlines()
        myline = random.choice(lines).capitalize()
        myline = myline.split(",")[0].capitalize()
        dataList.append('\''+myline+'\'')
    return dataList

# TODO migrar listas para dicionarios
def InitName(recordsToGenerate, dType, ValueDict):
    dataList = []
    for i in range(recordsToGenerate):
        # recebemos o primeiro caracter do ultimo nome usado na lista
        myline = str(ValueDict[-1][i][1])
        myline = myline.split(",")[0].capitalize()
        dataList.append('\''+myline+'\'')
    return dataList

def UserName(recordsToGenerate, dType, ValueDict):
    dataList = []
    for i in range(recordsToGenerate):
        # recebemos o primeiro caracter do ultimo nome usado na lista
        if ":" in dType:
            if 'Num' in dType:
                number = str(randint(0, 999999)).rjust(6, "0")
                myline = myline + ', ' + number
        else:
            myline = str(ValueDict[-1][i][1]) +str(ValueDict[-1][i][2]) +str(ValueDict[-1][i][3]) +str(ValueDict[-1][i][-3]) +str(ValueDict[-1][i][-2]) +str(ValueDict[-1][i][-1])
            myline = myline.split(",")[0].lower()
        dataList.append('\''+myline+'\'')
    return dataList    

def LastName(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        lines = open('./datasources/LastNameBR.txt').read().splitlines()
        myline = random.choice(lines).capitalize()
        myline = myline.split(",")[0]
        myline = str(myline.split()[0])
        dataList.append('\''+myline+'\'')
    return dataList

def FullName(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        lines = open('./datasources/FirstNameBR.txt').read().splitlines()
        myline = random.choice(lines).capitalize()
        myline = myline.split(",")[0]
        lines = open('./datasources/LastNameBR.txt').read().splitlines()
        myline = myline + ' ' + random.choice(lines).capitalize()
        myline = myline.split(",")[0]
        dataList.append('\''+myline+'\'')
    return dataList

def Sex(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        lines = open('./datasources/Sex.txt').read().splitlines()
        myline = random.choice(lines).capitalize()
        dataList.append('\''+myline+'\'')
    return dataList

def Address(recordsToGenerate, dType):
    dataList = []
    # atribui o valor inicial do serial(autoincremento)
    for i in range(recordsToGenerate):
        lines = open('./datasources/AddressTypeBR.txt').read().splitlines()
        myline = random.choice(lines)
        myline = myline.split(",")[0].capitalize()

        lines = open('./datasources/FirstNameBR.txt').read().splitlines()
        myline = myline + ' ' + random.choice(lines).capitalize()
        myline = myline.split(",")[0]
        
        if ":" in dType:
            if 'Num' in dType:
                number = str(randint(0, 999))
                myline = myline + ', ' + number
                
        dataList.append('\''+myline+'\'')
    return dataList

def City(recordsToGenerate, dType, ValueDict):
    dataList = []
    for i in range(recordsToGenerate):
        lines = open('./datasources/CityBR.txt').read().splitlines()
        myline = random.choice(lines)
        myline = myline.split(",")[2]
        dataList.append('\''+myline+'\'')
    return dataList

def StateProvince(recordsToGenerate, dType, ValueDict):
    dataList = []
    for i in range(recordsToGenerate):
        if ":" in dType:
            if 'Find' in dType:  
                lines = search_string_in_file('./datasources/CityBR.txt', str(ValueDict[-1][i].replace("'", '')))
                myline = lines.split(",")[0]
        else:
            lines = open('./datasources/StateProvinceBR.txt').read().splitlines()
            myline = random.choice(lines)
            myline = myline.split(",")[0]
        dataList.append(str('\''+myline+'\''))
    return dataList

def Varchar(recordsToGenerate, dType):
    dataList = []
    for i in range(recordsToGenerate):
        dataList.append(random_char(int(dType.split(":")[1])).upper())
    return dataList
