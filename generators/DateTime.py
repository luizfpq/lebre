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
__version__ = "2.0.1"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"

import random
import time

def str_time_prop(start, end, fmt, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, fmt))
    etime = time.mktime(time.strptime(end, fmt))

    ptime = stime + prop * (etime - stime)

    return time.strftime(fmt, time.localtime(ptime))


def random_date_time(start, end, prop):
    randDateTime = str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)
    return '\''+randDateTime+'\''

def random_date(start, end, prop):
    randDate = str_time_prop(start, end, '%d/%m/%Y', prop)
    return '\''+randDate+'\''


def Date(recordsToGenerate, dType):
    """
    Gera uma lista de datas aleatórias.
    USO:
        Date                        -> data entre 01/01/1970 e 01/01/2000
        Date:01/01/1990:31/12/2020  -> data no intervalo especificado
    """
    if ":" in dType:
        parts = dType.split(":")
        start = parts[1]
        end = parts[2]
    else:
        start = "1/1/1970"
        end = "1/1/2000"

    dataList = []
    for _ in range(recordsToGenerate):
        dataList.append(random_date(start, end, random.random()))
    return dataList


def DateTime(recordsToGenerate, dType):
    """
    Gera uma lista de datas com hora aleatórias.
    USO:
        DateTime                                        -> entre 01/01/1970 e 01/01/2000
        DateTime:01/01/1990 8:00 AM:31/12/2020 6:00 PM -> intervalo especificado
    """
    start = "1/1/1970 12:00 AM"
    end = "1/1/2000 11:59 PM"

    dataList = []
    for _ in range(recordsToGenerate):
        dataList.append(random_date_time(start, end, random.random()))
    return dataList