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
       Busca a string no arquivo e retorna uma lista filtrada apenas com a presença desta string
    """
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
    return list_of_results


def CPF(recordsToGenerate, dType):
    '''
    Gera o cadastro de pessoas físicas, com um valor validável
    '''
    dataList = []
    for i in range(recordsToGenerate):
        cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                    
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                    
            cpf.append(11 - val if val > 1 else 0)                                  

        dataList.append('%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf))
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
            myline = str(ValueDict[-1][i][1]) +str(ValueDict[-1][i][2]) +str(ValueDict[-1][i][3]) +str(ValueDict[-1][i][-4]) +str(ValueDict[-1][i][-3]) +str(ValueDict[-1][i][-2])
            
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
    ''' 
        USO: 
            caso queira definir uma cidade de estado específico
            adicione a sigla do estado desejado em maiusculo
                City:SP
            caso queira apenas uma cidade aleatória
                City
    '''
    dataList = []
    for i in range(recordsToGenerate):
        if ":" in dType:
           lines = search_string_in_file('./datasources/CityBR.txt',  str(dType.split(":")[1] ))
           myline = random.choice(lines)
           myline = myline.split(",")[2].replace("\n", "")
        else:
            lines = open('./datasources/CityBR.txt').read().splitlines()
            myline = random.choice(lines)
            myline = myline.split(",")[2]
        dataList.append('\''+myline+'\'')
    return dataList

def StateProvince(recordsToGenerate, dType, ValueDict):
    ''' 
        USO: 
            Caso queira apenas um estado aleatório
                StateProvince
            Caso queira um estado específico, use o tipo "Default",
            e adicione a sigla do estado desejado em maiusculo
                Default:SP
            Caso queira que o estado seja compatível com a cidade aleatória
                StateProvince:Find
            
            IMPORTANTE
            NUNCA USE O FIND COM recordsToGenerate > 50
            isso causa um estouro nos indices das listas usadas
            
    '''
    dataList = []
    for i in range(recordsToGenerate):
        if ":" in dType:
            if 'Find' in dType:  
                lines = search_string_in_file('./datasources/CityBR.txt',  str(ValueDict[-1][i].replace("'", '') ))
                myline = str(lines[0])
                myline = myline.split(",")[0].replace("\n", "")
            else:
                lines = search_string_in_file('./datasources/CityBR.txt',  str(dType.split(":")[1] ))
                myline = random.choice(lines)
                myline = myline.split(",")[0].replace("\n", "")
                
        else:
            lines = open('./datasources/StateProvinceBR.txt').read().splitlines()
            myline = random.choice(lines)
            #myline = myline.split(",")[0]
        dataList.append(str('\''+myline+'\''))
    return dataList

def Varchar(recordsToGenerate, dType):

    dataList = []
    for i in range(recordsToGenerate):
        dataList.append(random_char(int(dType.split(":")[1])).upper())
    return dataList
