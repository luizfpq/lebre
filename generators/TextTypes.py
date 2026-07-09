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


def CPF(records_to_generate, data_type):
    '''
    Gera o cadastro de pessoas físicas, com um valor validável
    '''
    data_list = []
    for i in range(records_to_generate):
        cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                    
        for _ in range(2):                                                          
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                    
            cpf.append(11 - val if val > 1 else 0)                                  

        data_list.append('%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf))
    return data_list

#def InitName(records_to_generate, data_type, value_dict):
#    data_list = []
#    for i in range(records_to_generate):
#        
#    return data_list

def FullName(records_to_generate, data_type):
    """
    Gera uma lista de nomes completos a partir do arquivo FullNameBR.txt.
    """
    data_list = []
    lines = _get_datasource('FullNameBR.txt')
    for i in range(records_to_generate):
        line = random.choice(lines).strip()
        data_list.append(f"'{line}'")
    return data_list

def FirstName(records_to_generate, data_type, value_dict):
    """
    Gera uma lista de primeiros nomes a partir da lista de nomes completos.
    """
    data_list = []
    for i in range(records_to_generate):
        fullname = value_dict[0][i]  # Assume que FullName é o primeiro no value_dict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        firstname = fullname.split()[0].strip("'")
        data_list.append(f"'{firstname}'")
    return data_list


def LastName(records_to_generate, data_type, value_dict):
    """
    Gera uma lista de sobrenomes a partir da lista de nomes completos.
    """
    data_list = []
    for i in range(records_to_generate):
        fullname = value_dict[0][i]  # Assume que FullName é o primeiro no value_dict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        lastname = fullname.split()[-1].strip("'")
        data_list.append(f"'{lastname}'")
    return data_list


def UserName(records_to_generate, data_type, value_dict):
    """
    Gera uma lista de nomes de usuário a partir da lista de nomes completos.
    """
    data_list = []
    for i in range(records_to_generate):
        fullname = value_dict[0][i]  # Assume que FullName é o primeiro no value_dict
        if not fullname:
            continue  # Ignore se fullname for None ou vazio

        fullname = fullname.strip("'")  # Remove aspas externas
        parts = fullname.split()
        username = (parts[0][0] + parts[-1]).lower()  # Primeiro caractere do primeiro nome + sobrenome
        if ":" in data_type:
            if 'Num' in data_type:
                number = str(randint(0, 999999)).rjust(6, "0")
                username = username + number
        data_list.append(f"'{username}'")
    return data_list


def Email(records_to_generate, data_type, value_dict):
    """
    Gera uma lista de emails a partir da lista de nomes completos.
    """
    data_list = []
    for i in range(records_to_generate):
        fullname = value_dict[0][i]  # Assume que FullName é o primeiro no value_dict
        parts = fullname.strip("'").split()
        email = (parts[0] + '.' + parts[-1]).lower() + "@example.com"  # Primeiro nome + ponto + sobrenome + @example.com
        data_list.append(f"'{email}'")
    return data_list

# TODO migrar listas para dicionarios
def InitName(records_to_generate, data_type, value_dict):
    data_list = []
    for i in range(records_to_generate):
        # recebemos o primeiro caracter do ultimo nome usado na lista
        line = str(value_dict[-1][i][1])
        line = line.split(",")[0]
        data_list.append('\''+line+'\'')
    return data_list

def Sex(records_to_generate, data_type):
    data_list = []
    lines = _get_datasource('Sex.txt')
    for i in range(records_to_generate):
        line = random.choice(lines)
        data_list.append('\''+line+'\'')
    return data_list

def Address(records_to_generate, data_type):
    data_list = []
    address_lines = _get_datasource('AddressTypeBR.txt')
    name_lines = _get_datasource('FullNameBR.txt')

    for i in range(records_to_generate):
        line = random.choice(address_lines)
        place_type = line.split(",")[0]

        chosen_line = random.choice(name_lines)
        words = chosen_line.split()
        num_words_to_select = random.randint(1, 2)
        selected_words = random.sample(words, min(num_words_to_select, len(words)))
        line = place_type+' '+' '.join(selected_words)
        
        if ":" in data_type:
            if 'Num' in data_type:
                number = str(randint(0, 999))
                line = line + ', ' + number
                
        data_list.append('\''+line+'\'')
    return data_list

def City(records_to_generate, data_type, value_dict):
    ''' 
        USO: 
            caso queira definir uma cidade de estado específico
            adicione a sigla do estado desejado em maiusculo
                City:SP
            caso queira apenas uma cidade aleatória
                City
    '''
    data_list = []
    if ":" in data_type:
        lines = _search_in_datasource('CityBR.txt', str(data_type.split(":")[1]))
    else:
        lines = _get_datasource('CityBR.txt')

    for i in range(records_to_generate):
        line = random.choice(lines)
        if ":" in data_type:
            line = line.split(",")[2].replace("\n", "")
        else:
            line = line.split(",")[2]
        data_list.append('\''+line+'\'')
    return data_list

def StateProvince(records_to_generate, data_type, value_dict):
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
            NUNCA USE O FIND COM records_to_generate > 50
            isso causa um estouro nos indices das listas usadas
            
    '''
    data_list = []

    # Pré-carrega linhas para modos que não dependem de value_dict por registro
    if ":" in data_type and 'Find' not in data_type:
        lines = _search_in_datasource('CityBR.txt', str(data_type.split(":")[1]))
    elif ":" not in data_type:
        lines = _get_datasource('StateProvinceBR.txt')
    else:
        lines = None  # modo Find — depende de cada registro

    for i in range(records_to_generate):
        if ":" in data_type:
            if 'Find' in data_type:
                matched = _search_in_datasource('CityBR.txt', str(value_dict[-1][i].replace("'", '')))
                line = str(matched[0])
                line = line.split(",")[0].replace("\n", "")
            else:
                line = random.choice(lines)
                line = line.split(",")[0].replace("\n", "")
        else:
            line = random.choice(lines)
        data_list.append(str('\''+line+'\''))
    return data_list

def Varchar(records_to_generate, data_type):

    data_list = []
    for i in range(records_to_generate):
        data_list.append(random_char(int(data_type.split(":")[1])))
    return data_list



# ---------------------------------------------------------------------------
# Novos geradores v2.1
# ---------------------------------------------------------------------------

import uuid as _uuid


def Phone(records_to_generate, data_type):
    """
    Gera números de telefone brasileiros.
    USO:
        Phone         -> celular com DDD aleatório, formato (XX) 9XXXX-XXXX
        Phone:fixo    -> fixo com DDD aleatório, formato (XX) XXXX-XXXX
        Phone:XX      -> celular com DDD específico (ex: Phone:11)
    """
    data_list = []
    for _ in range(records_to_generate):
        if ":" in data_type:
            param = data_type.split(":")[1]
            if param == 'fixo':
                ddd = str(randint(11, 99))
                number = f"({ddd}) {randint(2000,5999)}-{randint(1000,9999)}"
            else:
                ddd = param
                number = f"({ddd}) 9{randint(1000,9999)}-{randint(1000,9999)}"
        else:
            ddd = str(randint(11, 99))
            number = f"({ddd}) 9{randint(1000,9999)}-{randint(1000,9999)}"
        data_list.append(f"'{number}'")
    return data_list


def CNPJ(records_to_generate, data_type):
    """
    Gera CNPJs válidos (com dígitos verificadores corretos).
    Formato: XX.XXX.XXX/0001-XX
    """
    data_list = []
    for _ in range(records_to_generate):
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
        data_list.append(f"'{cnpj}'")
    return data_list


def CEP(records_to_generate, data_type):
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

    data_list = []
    for _ in range(records_to_generate):
        if ":" in data_type:
            uf = data_type.split(":")[1].upper()
            if uf in uf_ranges:
                prefix = randint(*uf_ranges[uf])
            else:
                prefix = randint(1000, 99999)
        else:
            prefix = randint(1000, 99999)

        suffix = randint(0, 999)
        cep = f"{prefix:05d}-{suffix:03d}"
        data_list.append(f"'{cep}'")
    return data_list


def UUID(records_to_generate, data_type):
    """
    Gera UUIDs v4 aleatórios.
    """
    data_list = []
    for _ in range(records_to_generate):
        data_list.append(f"'{_uuid.uuid4()}'")
    return data_list


def Boolean(records_to_generate, data_type):
    """
    Gera valores booleanos aleatórios.
    USO:
        Boolean          -> TRUE/FALSE
        Boolean:int      -> 1/0
        Boolean:bit      -> 1/0 (alias de int)
    """
    data_list = []
    for _ in range(records_to_generate):
        val = random.choice([True, False])
        if ":" in data_type:
            param = data_type.split(":")[1].lower()
            if param in ('int', 'bit'):
                data_list.append(1 if val else 0)
            else:
                data_list.append('TRUE' if val else 'FALSE')
        else:
            data_list.append('TRUE' if val else 'FALSE')
    return data_list
