#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Dataloader defines data types and load them all from datasource files
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "2.1.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"


import random

from generators.TextTypes import *
from generators.DateTime import *
from generators.NumericTypes import *


def DataLoad(records_to_generate, data_type, value_dict):
    """
    Dispatcher principal — roteia para o gerador correto conforme data_type.
    Nomes de tipo usam PascalCase (API pública dos geradores).
    """

    # --- TextTypes ---
    if 'FullName' in data_type:
        return FullName(records_to_generate, data_type)
    if 'FirstName' in data_type:
        return FirstName(records_to_generate, data_type, value_dict)
    if 'LastName' in data_type:
        return LastName(records_to_generate, data_type, value_dict)
    if 'Email' in data_type:
        return Email(records_to_generate, data_type, value_dict)
    if data_type == 'InitName':
        return InitName(records_to_generate, data_type, value_dict)
    if data_type == 'UserName' or data_type.startswith('UserName:'):
        return UserName(records_to_generate, data_type, value_dict)
    if data_type == 'Sex':
        return Sex(records_to_generate, data_type)
    if data_type == 'CPF':
        return CPF(records_to_generate, data_type)
    if "Varchar" in data_type:
        return Varchar(records_to_generate, data_type)
    if "Address" in data_type:
        return Address(records_to_generate, data_type)
    if "City" in data_type:
        return City(records_to_generate, data_type, value_dict)
    if "StateProvince" in data_type:
        return StateProvince(records_to_generate, data_type, value_dict)

    # --- NumericTypes ---
    if 'Serial' in data_type:
        return Serial(records_to_generate, data_type)
    if 'Integer' in data_type:
        return Integer(records_to_generate, data_type)

    # --- DateTimeTypes ---
    if 'Date' in data_type and 'DateTime' not in data_type:
        return Date(records_to_generate, data_type)
    if 'DateTime' in data_type:
        return DateTime(records_to_generate, data_type)

    # --- Default (retorna valor fixo) ---
    if "Default" in data_type:
        return [data_type.split(":")[1] for _ in range(records_to_generate)]

    # --- Novos tipos v2.1 ---
    if 'Phone' in data_type:
        return Phone(records_to_generate, data_type)
    if 'CNPJ' in data_type:
        return CNPJ(records_to_generate, data_type)
    if 'CEP' in data_type:
        return CEP(records_to_generate, data_type)
    if 'UUID' in data_type:
        return UUID(records_to_generate, data_type)
    if 'Boolean' in data_type:
        return Boolean(records_to_generate, data_type)
