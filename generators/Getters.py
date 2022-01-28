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

def get_table_name(table_dict):
    '''
    Recupera o nome da tabela a ser manipulada
    '''
    tableName = table_dict[0]['TableName']
    return tableName

def get_count_records_to_generate(table_dict):
    '''
        Recupera a quantidade de inserções a gerar
    '''
    recordsToGenerate = table_dict[0]['RecordsToGenerate']
    return recordsToGenerate

def get_count_field_list(table_dict):
    '''
    Conta os campos que foram passados no parametro FieldList
    '''
    num_fields = len(list(table_dict[0]['FieldList'].split(",")))
    return num_fields