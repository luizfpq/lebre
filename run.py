#!/usr/bin/env python3
# -*- coding:utf-8 -*-


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
