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
__version__ = "2.1.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"

import json
import glob
import os
from generators.DataLoader import *
from generators.Getters import *


def _get_next_number():
    files = glob.glob('results/*.sql')
    numbers = [int(os.path.basename(f).split('_')[0]) for f in files if f]
    return max(numbers) + 1 if numbers else 0


def main():
    num = _get_next_number()
    dir_path = 'results'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    output_file = f"{dir_path}/{num:02d}_saida.sql"

    with open(output_file, 'w') as sql_file:
        for file in glob.glob("tables/*.json"):
            with open(file, 'r') as f:
                table_dict = json.load(f)

                table_name = get_table_name(table_dict)
                records_to_generate = get_count_records_to_generate(table_dict)
                field_count = get_count_field_list(table_dict)

                value_dict = []
                fullname_values = []

                data_list = [item.strip() for item in table_dict[0]['DataType'].split(",")]

                # Gera FullName primeiro (necessário para FirstName, LastName, UserName, Email)
                has_fullname_field = any('FullName' in item for item in data_list)
                needs_fullname = any(
                    k in item for item in data_list
                    for k in ['FirstName', 'LastName', 'UserName', 'Email']
                )

                if has_fullname_field or needs_fullname:
                    for item in data_list:
                        if 'FullName' in item:
                            fullname_values = DataLoad(records_to_generate, item, value_dict)
                            break
                    else:
                        fullname_values = DataLoad(records_to_generate, 'FullName', value_dict)

                # Gera os outros campos
                for item in data_list:
                    if 'FullName' not in item:
                        if any(k in item for k in ['FirstName', 'LastName', 'UserName', 'Email']):
                            values = DataLoad(records_to_generate, item, [fullname_values])
                        else:
                            values = DataLoad(records_to_generate, item, value_dict)
                        value_dict.append(values)

                # Insere FullName na posição correta se estava no DataType
                for i, item in enumerate(data_list):
                    if 'FullName' in item:
                        value_dict.insert(i, [f"{name}" for name in fullname_values])
                        break

                sql_file.write(
                    f'INSERT INTO \n\t"{table_name}" ({table_dict[0]["FieldList"]}) \nVALUES\n'
                )

                for i in range(records_to_generate):
                    row_values = ', '.join(
                        str(value_dict[col][i]) for col in range(field_count)
                    )
                    separator = ';' if i == records_to_generate - 1 else ','
                    sql_file.write(f"\t({row_values}){separator}\n")

    print(f"Arquivo SQL gerado e salvo em '{output_file}'.")


if __name__ == "__main__":
    main()
