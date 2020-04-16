#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 
    A Database Populator is a tool which helps you to populate your projects' database tables 
    with randomly generated content. With this tool you no longer need to write queries or to 
    compile forms by yourself wasting a lot of time before to start to work on your applications.
"""
__author__ = “Luiz F. P. Quirino”
__copyright__ = “Copyright 2020, JMIY - Just Make It Yours”
__credits__ = [“LuizQuirino”]
__license__ = “MPL 2.0”
__version__ = “0.1.0”
__maintainer__ = “LuizQuirino”
__email__ = “luizfpq@gmail.com”
__status__ = “Dev”

import json
import glob
import os
from assets.DataLoader import *


for file in glob.glob("table/*.json"):
    with open(file, 'r') as f:
        table_dict = json.load(f)
        tableName = os.path.splitext(os.path.basename(file))[0]
        
        for i in range(table_dict[0]['RecordsToGenerate']):
            valueList = ''
            DataList = list(table_dict[0]['DataType'].split(","))
            
            for i in DataList:
               valueList = valueList + str(DataLoad(i)) + ', '

            print("insert into \"{}\" ({}) values ({})".format(tableName,table_dict[0]['FieldList'],valueList[:-2]))       
