#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Geradores de tipos numéricos.
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


def Integer(records_to_generate, data_type):
    """
    Define o tipo inteiro.
    USO: Integer:min_value:max_value (ex: Integer:0:10)
    """
    parts = data_type.split(":")
    min_val = int(parts[1])
    max_val = int(parts[2])
    return [random.randint(min_val, max_val) for _ in range(records_to_generate)]


def Serial(records_to_generate, data_type):
    """
    Define o tipo serial (autoincremento).
    USO:
        Serial:10  -> inicia em 10
        Serial     -> inicia em 0
    """
    start = int(data_type.split(":")[1]) if ":" in data_type else 0
    return [start + i for i in range(records_to_generate)]
