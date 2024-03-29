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

def Integer(recordsToGenerate, arg):
    '''
    Define o tipo inteiro
        USO: 
            Integer:min_value:max_value
            ex: Integer:0:10
    '''
    dataList = []
    for i in range(recordsToGenerate):
        dataList.append(random.randint(int(arg.split(":")[1]), int(arg.split(":")[2])))
    return dataList

def Serial(recordsToGenerate, arg):
    '''
    Define o tipo serial, sendo um tipo inteiro, com comportamento semelhante ao autoincrimento,
    bastante usado em chavez primárias ou indices de tabelas
        USO: 
        Caso queira definir um valor inicial
            Serial:10
        Caso queira iniciar do zero
            Serial
    '''
    dataList = []
    # atribui o valor inicial do serial(autoincremento)
    if ":" in arg:
        serial = int(arg.split(":")[1])
    else:
        serial = 0

    for i in range(recordsToGenerate):
        dataList.append(serial)
        serial = serial + 1
    return dataList
