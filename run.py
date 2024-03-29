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
__version__ = "0.2.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"

from dataclasses import Field, field
import json
import glob
import os
from signal import pause
from generators.DataLoader import *
from generators.Getters import *


for file in glob.glob("table/*.json"):
    with open(file, 'r') as f:
        table_dict = json.load(f)
        tableName = get_table_name(table_dict)
        recordsToGenerate = get_count_records_to_generate(table_dict)
        CountFieldListSize =  get_count_field_list(table_dict)
        '''
            A estratégia usada é de criar um conjunto de listas para cada tipo de dados recebido no DataType
            Sendo assim, temos os parametros disponíveis para receber os campos que dependam entre si, como por exemplo,
            para definir iniciais de nomes ou nomes de usuario.

            # TODO: criar uma estrutura de chaves estrangeiras no json da tabela de modo que uma chave
            estrangeira possa ser consultada e definida mantendo a consistencia da tabela.
        '''
        ''' ValueDict receberá uma lista de listas com os valores devolvidos pelos generators '''
        ValueDict = []
        ''' DataList recebe uma lista com os tipos de dados que iremos utilizar '''
        DataList = list(table_dict[0]['DataType'].split(","))
        
        for item in DataList:
            values = DataLoad(recordsToGenerate, item.strip(), ValueDict)
            ValueDict.append(values)

        '''separa as linhas dos inserts, vira ; apenas no ultimo valor'''
        lineSeparator = ','
        print("INSERT INTO \n\t\"{}\" ({}) \nVALUES".format(tableName,table_dict[0]['FieldList']))
        #percorre todas as linhas da lista
        for i in range(recordsToGenerate):
            values = ''
            #percorre todos os campos da sublista
            FieldValue = 0
            
            while (FieldValue < CountFieldListSize):
                values = values + str(ValueDict[FieldValue][i]) + ', '
                FieldValue += 1
            
            if (i == recordsToGenerate-1):
                lineSeparator = ';'
            
            print("\t({}){}".format(values[:-2], lineSeparator))
            