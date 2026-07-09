#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Funções auxiliares para extrair informações das definições de tabela.
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "2.1.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


def get_table_name(table_dict):
    """Recupera o nome da tabela a ser manipulada."""
    return table_dict[0]['TableName']


def get_count_records_to_generate(table_dict):
    """Recupera a quantidade de inserções a gerar."""
    return table_dict[0]['RecordsToGenerate']


def get_count_field_list(table_dict):
    """Conta os campos que foram passados no parâmetro FieldList."""
    return len(table_dict[0]['FieldList'].split(","))
