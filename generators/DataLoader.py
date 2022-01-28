#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Dataloader defines data types and load them all from datasource files
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "0.2.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


import random
''' TextTypes reponses for all nom numeric data'''
from generators.TextTypes import *
''' DateTime responses for all DateTime based data'''
from generators.DateTime import *
''' NumericTypes responses for all generic numeric data '''
from generators.NumericTypes import *

def DataLoad(recordsToGenerate, dType, ValueDict):

    '''
        TextTypes
    '''
    if dType == 'FirstName':
        return  FirstName(recordsToGenerate, dType)
    if dType == 'LastName':
        return  LastName(recordsToGenerate, dType)
    if dType == 'FullName':
        return  FullName(recordsToGenerate, dType)
    ''' 
        USO: 
        Sempre que usar um campo inicial, ao criar o campo para os inserts, 
        sempre colocar o campo da inicial logo a seguir do campo nome, 
        pode-se usar a seguir de um FirstName, LastName, FullName, ou qualquer 
        string que se queira obter a inicial
    '''
    if dType == 'InitName':
        return  InitName(recordsToGenerate, dType, ValueDict)
    ''' 
        USO: 
        Caso queira uma uma concatenação dos 3 primeiros e 3 ultimos carateres da string
        Sempre que usar um campo inicial, ao criar o campo para os inserts, 
        sempre colocar o campo da inicial logo a seguir do campo nome, 
        pode-se usar a seguir de um FirstName, LastName, FullName, ou qualquer 
        string que se queira obter a inicial
    '''
    if dType == 'UserName':
        return UserName(recordsToGenerate, dType, ValueDict)
    '''
        USO:
        Caso queira alterar o tipo de dado retornado, alterar o dicionario de sexos em 
        datasources/Sex.txt
    '''
    if dType == 'Sex':
        return  Sex(recordsToGenerate, dType)
    if dType == 'CPF':
        return CPF(recordsToGenerate, dType)
    '''
        USO: 
            Varchar:size
    '''
    if "Varchar" in dType:
        return Varchar(recordsToGenerate, dType)
    ''' 
        USO: 
            caso queira definir um numero aleatório ao endereço
                Address:Num
            caso queira apenas um logradouro aleatório
                Address
    '''
    if "Address" in dType:
        return Address(recordsToGenerate, dType)
    if "City" in dType:
        return City(recordsToGenerate, dType, ValueDict)   
    if "StateProvince" in dType:
        return StateProvince(recordsToGenerate, dType, ValueDict)

    '''
        NumericTypes
    '''
    if 'Serial' in dType:
        return Serial(recordsToGenerate, dType)
    
    if 'Integer' in dType:
        return Integer(recordsToGenerate, dType)


    '''
        DateTimeTypes
    '''
    # TODO permit date interval selection
    if dType == 'Date':
        return random_date("1/1/1970", "1/1/2000", random.random(recordsToGenerate, dType))
    '''
        Set a Default data, wich returns itself, to set default values on fields
        Example1
        Default:'00235'
        Return: '00235'
        Example2
        Default:00235
        Return: 00235
    '''
    if "Default" in dType:
        dataList = []
        for i in range(recordsToGenerate):
            dataList.append(dType.split(":")[1])
        return dataList
