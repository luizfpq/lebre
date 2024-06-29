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

import json
import glob
import os
from generators.DataLoader import *
from generators.Getters import *

def obter_proximo_numero():
    arquivos = glob.glob('results/*.sql')
    numeros = [int(os.path.basename(arquivo).split('_')[0]) for arquivo in arquivos if arquivo]
    return max(numeros) + 1 if numeros else 0

def main():
    numero = obter_proximo_numero()
    numero_formatado = f"{numero:02d}"
    dir_path = 'results'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    nome_arquivo = f"{dir_path}/{numero_formatado}_saida.sql"
    
    with open(nome_arquivo, 'w') as sql_file:
        for file in glob.glob("tables/*.json"):
            with open(file, 'r') as f:
                table_dict = json.load(f)
                tableName = get_table_name(table_dict)
                recordsToGenerate = get_count_records_to_generate(table_dict)
                CountFieldListSize = get_count_field_list(table_dict)

                ValueDict = []  # Armazena todos os valores gerados
                FullNameValues = []  # Armazena os nomes completos

                DataList = list(table_dict[0]['DataType'].split(","))

                # Gera FullName primeiro
                for i, item in enumerate(DataList):
                    if 'FullName' in item:
                        FullNameValues = DataLoad(recordsToGenerate, item.strip(), ValueDict)
                        break

                # Gera os outros campos
                for item in DataList:
                    if 'FullName' not in item:
                        # Passa FullNameValues para as funções que precisam
                        if any(k in item for k in ['FirstName', 'LastName', 'UserName', 'Email']):
                            values = DataLoad(recordsToGenerate, item.strip(), [FullNameValues])
                        else:
                            values = DataLoad(recordsToGenerate, item.strip(), ValueDict)
                        ValueDict.append(values)

                # Adiciona FullName ao ValueDict apenas se solicitado no DataType
                for i, item in enumerate(DataList):
                    if 'FullName' in item:
                        ValueDict.insert(i, [f"{name}" for name in FullNameValues])
                        break

                lineSeparator = ','
                sql_file.write(f"INSERT INTO \n\t\"{tableName}\" ({table_dict[0]['FieldList']}) \nVALUES\n")
                
                for i in range(recordsToGenerate):
                    values = ''
                    FieldValue = 0
                    
                    while FieldValue < CountFieldListSize:
                        values += f"{ValueDict[FieldValue][i]}, "
                        FieldValue += 1
                    
                    if i == recordsToGenerate - 1:
                        lineSeparator = ';'
                    
                    sql_file.write(f"\t({values[:-2]}){lineSeparator}\n")
    
    print(f"Arquivo SQL gerado e salvo em '{nome_arquivo}'.")

if __name__ == "__main__":
    main()