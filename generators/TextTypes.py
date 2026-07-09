#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    A Database Populator is a tool which helps you to populate your projects' database tables
    with randomly generated content. With this tool you no longer need to write queries or to
    compile forms by yourself wasting a lot of time before to start to work on your applications.


    Aways return strings in this format '\''+randChar+'\'', to pass the '' to variable


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
from random import randint
import string
import os

# ---------------------------------------------------------------------------
# Cache de datasources — carrega cada arquivo apenas uma vez em memória
# ---------------------------------------------------------------------------
_datasource_cache = {}

def _get_datasource(filename):
    """Retorna as linhas do datasource em cache. Carrega do disco apenas na primeira chamada."""
    if filename not in _datasource_cache:
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'datasources', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            _datasource_cache[filename] = f.read().splitlines()
    return _datasource_cache[filename]


def _search_in_datasource(filename, search_term):
    """Filtra linhas do datasource que contêm search_term."""
    lines = _get_datasource(filename)
    return [line for line in lines if search_term in line]


def random_char(y):
    randChar = ''.join(random.choice(string.ascii_letters) for x in range(y))
    return '\''+randChar+'\''


def CPF(recordsToGenerate, dType):
    '''
    Gera o cadastro de pessoas físicas, com um valor validável
    '''
    dataList = []
    for i in range(recordsToGenerate):
        cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                    
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                    
            cpf.append(11 - val if val > 1 else 0)                                  

        dataList.append('%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf))
    return dataList

#def InitName(recordsToGenerate, dType, ValueDict):
#    dataList = []
#    for i in range(recordsToGenerate):
#        
#    return dataList

def FullName(recordsToGenerate, dType):
    """
    Gera uma lista de nomes completos a partir do arquivo FullNameBR.txt.
    """
    dataList = []
    lines = _get_datasource('FullNameBR.txt')
    for i in range(recordsToGenerate):
        myline = random.choice(lines).strip()
        dataList.append(f"'{myline}'")
    return dataList

def FirstName(recordsToGenerate, dType, ValueDict):
    """
    Gera uma lista de primeiros nomes a partir da lista de nomes completos.
    """
    dataList = []
    for i in range(recordsToGenerate):
        fullname = ValueDict[0][i]  # Assume que FullName é o primeiro no ValueDict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        firstname = fullname.split()[0].strip("'")
        dataList.append(f"'{firstname}'")
    return dataList


def LastName(recordsToGenerate, dType, ValueDict):
    """
    Gera uma lista de sobrenomes a partir da lista de nomes completos.
    """
    dataList = []
    for i in range(recordsToGenerate):
        fullname = ValueDict[0][i]  # Assume que FullName é o primeiro no ValueDict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        lastname = fullname.split()[-1].strip("'")
        dataList.append(f"'{lastname}'")
    return dataList


def UserName(recordsToGenerate, dType, ValueDict):
    """
    Gera uma lista de nomes de usuário a partir da lista de nomes completos.
    """
    dataList = []
    for i in range(recordsToGenerate):
        fullname = ValueDict[0][i]  # Assume que FullName é o primeiro no ValueDict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        fullname = fullname.strip("'")  # Remove aspas externas
        parts = fullname.split()
        username = (parts[0][0] + parts[-1]).lower()  # Primeiro caractere do primeiro nome + sobrenome
        if ":" in dType:
            if 'Num' in dType:
                number = str(randint(0, 999999)).rjust(6, "0")
                username = username + number
        dataList.append(f"'{username}'")
    return dataList


def Email(recordsToGenerate, dType, ValueDict):
    """
    Gera uma lista de emails a partir da lista de nomes completos.
    """
    dataList = []
    for i in range(recordsToGenerate):
        fullname = ValueDict[0][i]  # Assume que FullName é o primeiro no ValueDict
        parts = fullname.strip("'").split()
        email = (parts[0] + '.' + parts[-1]).lower() + "@example.com"  # Primeiro nome + ponto + sobrenome + @example.com
        dataList.append(f"'{email}'")
    return dataList

# TODO migrar listas para dicionarios
def InitName(recordsToGenerate, dType, ValueDict):
    dataList = []
    for i in range(recordsToGenerate):
        # recebemos o primeiro caracter do ultimo nome usado na lista
        myline = str(ValueDict[-1][i][1])
        myline = myline.split(",")[0]
        dataList.append('\''+myline+'\'')
    return dataList

def Sex(recordsToGenerate, dType):
    dataList = []
    lines = _get_datasource('Sex.txt')
    for i in range(recordsToGenerate):
        myline = random.choice(lines)
        dataList.append('\''+myline+'\'')
    return dataList

def Address(recordsToGenerate, dType):
    dataList = []
    address_lines = _get_datasource('AddressTypeBR.txt')
    name_lines = _get_datasource('FullNameBR.txt')

    for i in range(recordsToGenerate):
        myline = random.choice(address_lines)
        placeType = myline.split(",")[0]

        chosen_line = random.choice(name_lines)
        words = chosen_line.split()
        num_words_to_select = random.randint(1, 2)
        selected_words = random.sample(words, min(num_words_to_select, len(words)))
        myline = placeType+' '+' '.join(selected_words)
        
        if ":" in dType:
            if 'Num' in dType:
                number = str(randint(0, 999))
                myline = myline + ', ' + number
                
        dataList.append('\''+myline+'\'')
    return dataList

def City(recordsToGenerate, dType, ValueDict):
    ''' 
        USO: 
            caso queira definir uma cidade de estado específico
            adicione a sigla do estado desejado em maiusculo
                City:SP
            caso queira apenas uma cidade aleatória
                City
    '''
    dataList = []
    if ":" in dType:
        lines = _search_in_datasource('CityBR.txt', str(dType.split(":")[1]))
    else:
        lines = _get_datasource('CityBR.txt')

    for i in range(recordsToGenerate):
        myline = random.choice(lines)
        if ":" in dType:
            myline = myline.split(",")[2].replace("\n", "")
        else:
            myline = myline.split(",")[2]
        dataList.append('\''+myline+'\'')
    return dataList

def StateProvince(recordsToGenerate, dType, ValueDict):
    ''' 
        USO: 
            Caso queira apenas um estado aleatório
                StateProvince
            Caso queira um estado específico, use o tipo "Default",
            e adicione a sigla do estado desejado em maiusculo
                Default:SP
            Caso queira que o estado seja compatível com a cidade aleatória
                StateProvince:Find
            
            IMPORTANTE
            NUNCA USE O FIND COM recordsToGenerate > 50
            isso causa um estouro nos indices das listas usadas
            
    '''
    dataList = []

    # Pré-carrega linhas para modos que não dependem de ValueDict por registro
    if ":" in dType and 'Find' not in dType:
        lines = _search_in_datasource('CityBR.txt', str(dType.split(":")[1]))
    elif ":" not in dType:
        lines = _get_datasource('StateProvinceBR.txt')
    else:
        lines = None  # modo Find — depende de cada registro

    for i in range(recordsToGenerate):
        if ":" in dType:
            if 'Find' in dType:
                matched = _search_in_datasource('CityBR.txt', str(ValueDict[-1][i].replace("'", '')))
                myline = str(matched[0])
                myline = myline.split(",")[0].replace("\n", "")
            else:
                myline = random.choice(lines)
                myline = myline.split(",")[0].replace("\n", "")
        else:
            myline = random.choice(lines)
        dataList.append(str('\''+myline+'\''))
    return dataList

def Varchar(recordsToGenerate, dType):

    dataList = []
    for i in range(recordsToGenerate):
        dataList.append(random_char(int(dType.split(":")[1])))
    return dataList



# ---------------------------------------------------------------------------
# Novos geradores v2.1
# ---------------------------------------------------------------------------

import uuid as _uuid


def Phone(recordsToGenerate, dType):
    """
    Gera números de telefone brasileiros.
    USO:
        Phone         -> celular com DDD aleatório, formato (XX) 9XXXX-XXXX
        Phone:fixo    -> fixo com DDD aleatório, formato (XX) XXXX-XXXX
        Phone:XX      -> celular com DDD específico (ex: Phone:11)
    """
    dataList = []
    for _ in range(recordsToGenerate):
        if ":" in dType:
            param = dType.split(":")[1]
            if param == 'fixo':
                ddd = str(randint(11, 99))
                number = f"({ddd}) {randint(2000,5999)}-{randint(1000,9999)}"
            else:
                ddd = param
                number = f"({ddd}) 9{randint(1000,9999)}-{randint(1000,9999)}"
        else:
            ddd = str(randint(11, 99))
            number = f"({ddd}) 9{randint(1000,9999)}-{randint(1000,9999)}"
        dataList.append(f"'{number}'")
    return dataList


def CNPJ(recordsToGenerate, dType):
    """
    Gera CNPJs válidos (com dígitos verificadores corretos).
    Formato: XX.XXX.XXX/0001-XX
    """
    dataList = []
    for _ in range(recordsToGenerate):
        base = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]

        # Primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        val = sum(b * w for b, w in zip(base, weights1)) % 11
        base.append(0 if val < 2 else 11 - val)

        # Segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        val = sum(b * w for b, w in zip(base, weights2)) % 11
        base.append(0 if val < 2 else 11 - val)

        cnpj = '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(base)
        dataList.append(f"'{cnpj}'")
    return dataList


def CEP(recordsToGenerate, dType):
    """
    Gera CEPs aleatórios no formato XXXXX-XXX.
    USO:
        CEP       -> CEP totalmente aleatório
        CEP:SP    -> CEP com faixa de São Paulo (01000-19999)
    """
    # Faixas aproximadas por UF (primeiro dígito)
    uf_ranges = {
        'SP': (1000, 19999), 'RJ': (20000, 28999), 'ES': (29000, 29999),
        'MG': (30000, 39999), 'BA': (40000, 48999), 'SE': (49000, 49999),
        'PE': (50000, 56999), 'AL': (57000, 57999), 'PB': (58000, 58999),
        'RN': (59000, 59999), 'CE': (60000, 63999), 'PI': (64000, 64999),
        'MA': (65000, 65999), 'PA': (66000, 68899), 'AP': (68900, 68999),
        'AM': (69000, 69299), 'RR': (69300, 69399), 'AC': (69900, 69999),
        'DF': (70000, 72799), 'GO': (72800, 76799), 'TO': (77000, 77999),
        'MT': (78000, 78899), 'MS': (79000, 79999), 'PR': (80000, 87999),
        'SC': (88000, 89999), 'RS': (90000, 99999),
    }

    dataList = []
    for _ in range(recordsToGenerate):
        if ":" in dType:
            uf = dType.split(":")[1].upper()
            if uf in uf_ranges:
                prefix = randint(*uf_ranges[uf])
            else:
                prefix = randint(1000, 99999)
        else:
            prefix = randint(1000, 99999)

        suffix = randint(0, 999)
        cep = f"{prefix:05d}-{suffix:03d}"
        dataList.append(f"'{cep}'")
    return dataList


def UUID(recordsToGenerate, dType):
    """
    Gera UUIDs v4 aleatórios.
    """
    dataList = []
    for _ in range(recordsToGenerate):
        dataList.append(f"'{_uuid.uuid4()}'")
    return dataList


def Boolean(recordsToGenerate, dType):
    """
    Gera valores booleanos aleatórios.
    USO:
        Boolean          -> TRUE/FALSE
        Boolean:int      -> 1/0
        Boolean:bit      -> 1/0 (alias de int)
    """
    dataList = []
    for _ in range(recordsToGenerate):
        val = random.choice([True, False])
        if ":" in dType:
            param = dType.split(":")[1].lower()
            if param in ('int', 'bit'):
                dataList.append(1 if val else 0)
            else:
                dataList.append('TRUE' if val else 'FALSE')
        else:
            dataList.append('TRUE' if val else 'FALSE')
    return dataList
