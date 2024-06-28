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
__version__ = "0.2.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"

import json
import os

def obter_entrada(prompt):
    return input(prompt)

def obter_proximo_numero():
    """
    Verifica os arquivos na pasta 'tables' e determina o próximo número disponível.
    Os arquivos devem estar nomeados no formato NN_nome.json, onde NN é um número.
    """
    dir_path = 'tables'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    arquivos = os.listdir(dir_path)
    numeros_existentes = []
    
    for arquivo in arquivos:
        if arquivo.endswith('.json'):
            try:
                numero = int(arquivo.split('_')[0])
                numeros_existentes.append(numero)
            except ValueError:
                continue
    
    if numeros_existentes:
        return max(numeros_existentes) + 1
    else:
        return 0

def gerar_json():
    tabela = {}
    
    # Pergunta o nome da tabela
    tabela['TableName'] = obter_entrada("Digite o nome da tabela: ")

    # Pergunta a lista de campos
    fields = []
    print("Digite os nomes dos campos, separados por vírgula:")
    tabela['FieldList'] = obter_entrada("Nomes dos campos: ")
    fields = tabela['FieldList'].split(',')

    # Pergunta o tipo de dado para cada campo
    data_types = []
    print("Para cada campo, insira o tipo de dado correspondente.")
    for field in fields:
        data_type = obter_entrada(f"Tipo de dado para {field.strip()}: ")
        data_types.append(data_type)

    tabela['DataType'] = ','.join(data_types)

    # Pergunta a quantidade de registros a gerar
    tabela['RecordsToGenerate'] = int(obter_entrada("Digite o número de registros a gerar: "))

    return tabela

def salvar_tabela(tabela):
    # Verifica o próximo número disponível para nomear a tabela
    numero = obter_proximo_numero()
    numero_formatado = f"{numero:02d}"  # Formata para dois dígitos
    nome_arquivo = f"tables/{numero_formatado}_tbl_{tabela['TableName']}.json"

    with open(nome_arquivo, 'w') as json_file:
        json.dump([tabela], json_file, indent=4)
    
    print(f"\nTabela salva em '{nome_arquivo}'.")

def main():
    tabela = gerar_json()
    salvar_tabela(tabela)

if __name__ == "__main__":
    main()
