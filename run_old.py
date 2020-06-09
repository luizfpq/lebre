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
__version__ = "0.1.1"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"

import json
import glob
import os
from generators.DataLoader import *


for file in glob.glob("table/*.json"):
    with open(file, 'r') as f:
        table_dict = json.load(f)
        tableName = table_dict[0]['TableName']
        for i in range(table_dict[0]['RecordsToGenerate']):
            valueList = ''
            DataList = list(table_dict[0]['DataType'].split(","))

            for i in DataList:
                ''' # TODO: need to find a way to put this functionality inside DataLoader
                    Create a serial id, like an auto increment
                '''
                if DataLoad(i) == 'serial':
                    '''
                        serial:indexos.path.splitext(os.path.basename(file))[0]
                    '''
                    value = serial = 0
                    serial = serial + 1
                elif DataLoad(i) == 'initname':
                    value =  valueList[-1][:1]
                    print(valueList[-4])
                else:
                    value = DataLoad(i)

                valueList = valueList + str(value) + ', '

            print("insert into \"{}\" ({}) values ({})".format(tableName,table_dict[0]['FieldList'],valueList[:-2]))
