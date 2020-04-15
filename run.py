# -*- coding:utf-8 -*-

import json
import glob
import os

map(os.path.basename, glob.glob("your/path"))

#list json files on table folder
for file in glob.glob("table/*.json"):
    with open(file, 'r') as f:
        table_dict = json.load(f)
        tableName = os.path.basename(file)
        print ("insert into {}".format)





#for files in distros_dict:
    #print(distro['Name'])


#with open('table/table.json', 'r') as f:
#    distros_dict = json.load(f)

