#!/usr/bin/env python3
"""Geradores de tipos textuais e documentos brasileiros."""

from __future__ import annotations

import os
import random
import string
import uuid as _uuid
from random import randint

__all__ = [
    "FullName", "FirstName", "LastName", "UserName", "Email", "InitName",
    "Sex", "CPF", "CNPJ", "Phone", "CEP", "UUID", "Boolean",
    "Varchar", "Address", "City", "StateProvince",
]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class GeneratorError(Exception):
    """Erro de configuração ou execução de um gerador."""


class DatasourceError(GeneratorError):
    """Erro ao carregar arquivo de datasource."""


# ---------------------------------------------------------------------------
# Cache de datasources
# ---------------------------------------------------------------------------

_datasource_cache: dict[str, list[str]] = {}
_DATASOURCES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datasources'
)


def _get_datasource(filename: str) -> list[str]:
    """
    Retorna linhas do datasource em cache.
    Carrega do disco apenas na primeira chamada.
    """
    if filename not in _datasource_cache:
        filepath = os.path.join(_DATASOURCES_DIR, filename)
        if not os.path.isfile(filepath):
            raise DatasourceError(
                f"Datasource não encontrado: '{filepath}'. "
                f"Verifique se o arquivo existe em datasources/"
            )
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except OSError as exc:
            raise DatasourceError(f"Erro ao ler datasource '{filename}': {exc}") from exc

        if not lines:
            raise DatasourceError(f"Datasource vazio: '{filename}'")

        _datasource_cache[filename] = lines
    return _datasource_cache[filename]


def _search_in_datasource(filename: str, search_term: str) -> list[str]:
    """Filtra linhas do datasource que contêm search_term."""
    lines = _get_datasource(filename)
    results = [line for line in lines if search_term in line]
    if not results:
        raise GeneratorError(
            f"Nenhum resultado para '{search_term}' em '{filename}'"
        )
    return results


def _validate_records(records_to_generate: int) -> None:
    """Valida que o número de registros é positivo."""
    if records_to_generate <= 0:
        raise GeneratorError(
            f"records_to_generate deve ser > 0, recebeu {records_to_generate}"
        )


# ---------------------------------------------------------------------------
# Documentos — CPF
# ---------------------------------------------------------------------------

def CPF(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera CPFs válidos com dígitos verificadores corretos.
    Formato: XXX.XXX.XXX-XX
    """
    _validate_records(records_to_generate)
    results = []
    for _ in range(records_to_generate):
        digits = [random.randint(0, 9) for _ in range(9)]

        # Primeiro dígito verificador
        val = sum((10 - i) * d for i, d in enumerate(digits)) % 11
        digits.append(0 if val < 2 else 11 - val)

        # Segundo dígito verificador
        val = sum((11 - i) * d for i, d in enumerate(digits)) % 11
        digits.append(0 if val < 2 else 11 - val)

        cpf_str = '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(digits)
        results.append(cpf_str)
    return results


# ---------------------------------------------------------------------------
# Documentos — CNPJ
# ---------------------------------------------------------------------------

def CNPJ(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera CNPJs válidos com dígitos verificadores corretos.
    Formato: XX.XXX.XXX/0001-XX
    """
    _validate_records(records_to_generate)
    weights1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    weights2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)

    results = []
    for _ in range(records_to_generate):
        base = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]

        val = sum(b * w for b, w in zip(base, weights1)) % 11
        base.append(0 if val < 2 else 11 - val)

        val = sum(b * w for b, w in zip(base, weights2)) % 11
        base.append(0 if val < 2 else 11 - val)

        cnpj_str = "'%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s'" % tuple(base)
        results.append(cnpj_str)
    return results


# ---------------------------------------------------------------------------
# Nomes
# ---------------------------------------------------------------------------

def FullName(records_to_generate: int, data_type: str) -> list[str]:
    """Gera nomes completos a partir do datasource FullNameBR.txt."""
    _validate_records(records_to_generate)
    lines = _get_datasource('FullNameBR.txt')
    return [f"'{random.choice(lines)}'" for _ in range(records_to_generate)]


def FirstName(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """Extrai primeiro nome a partir da lista de nomes completos."""
    _validate_records(records_to_generate)
    if not value_dict or not value_dict[0]:
        raise GeneratorError("FirstName requer FullName gerado previamente no value_dict")

    fullnames = value_dict[0]
    results = []
    for i in range(records_to_generate):
        name = fullnames[i].strip("'")
        parts = name.split()
        results.append(f"'{parts[0]}'")
    return results


def LastName(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """Extrai sobrenome a partir da lista de nomes completos."""
    _validate_records(records_to_generate)
    if not value_dict or not value_dict[0]:
        raise GeneratorError("LastName requer FullName gerado previamente no value_dict")

    fullnames = value_dict[0]
    results = []
    for i in range(records_to_generate):
        name = fullnames[i].strip("'")
        parts = name.split()
        results.append(f"'{parts[-1]}'")
    return results


def UserName(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """
    Gera username a partir do nome completo (inicial + sobrenome).

    Uso:
        UserName      -> ex: 'jsilva'
        UserName:Num  -> ex: 'jsilva042871'
    """
    _validate_records(records_to_generate)
    if not value_dict or not value_dict[0]:
        raise GeneratorError("UserName requer FullName gerado previamente no value_dict")

    add_number = ":" in data_type and "Num" in data_type
    fullnames = value_dict[0]
    results = []
    for i in range(records_to_generate):
        name = fullnames[i].strip("'")
        parts = name.split()
        username = (parts[0][0] + parts[-1]).lower()
        if add_number:
            username += str(randint(0, 999999)).rjust(6, "0")
        results.append(f"'{username}'")
    return results


def Email(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """Gera email a partir do nome completo (nome.sobrenome@example.com)."""
    _validate_records(records_to_generate)
    if not value_dict or not value_dict[0]:
        raise GeneratorError("Email requer FullName gerado previamente no value_dict")

    fullnames = value_dict[0]
    results = []
    for i in range(records_to_generate):
        name = fullnames[i].strip("'")
        parts = name.split()
        email = f"{parts[0].lower()}.{parts[-1].lower()}@example.com"
        results.append(f"'{email}'")
    return results


def InitName(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """Retorna o primeiro caractere do último campo gerado."""
    _validate_records(records_to_generate)
    if not value_dict:
        raise GeneratorError("InitName requer pelo menos um campo gerado previamente")

    last_field = value_dict[-1]
    results = []
    for i in range(records_to_generate):
        char = str(last_field[i])[1]  # pula a aspa inicial
        results.append(f"'{char}'")
    return results


# ---------------------------------------------------------------------------
# Gênero
# ---------------------------------------------------------------------------

def Sex(records_to_generate: int, data_type: str) -> list[str]:
    """Gera valor aleatório de sexo/gênero do datasource."""
    _validate_records(records_to_generate)
    lines = _get_datasource('Sex.txt')
    return [f"'{random.choice(lines)}'" for _ in range(records_to_generate)]


# ---------------------------------------------------------------------------
# Endereço / Localização
# ---------------------------------------------------------------------------

def Address(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera endereços brasileiros aleatórios.

    Uso:
        Address      -> ex: 'Rua Santos'
        Address:Num  -> ex: 'Rua Santos, 127'
    """
    _validate_records(records_to_generate)
    address_lines = _get_datasource('AddressTypeBR.txt')
    name_lines = _get_datasource('FullNameBR.txt')
    add_number = ":" in data_type and "Num" in data_type

    results = []
    for _ in range(records_to_generate):
        place_type = random.choice(address_lines).split(",")[0]
        chosen_name = random.choice(name_lines)
        words = chosen_name.split()
        num_words = random.randint(1, min(2, len(words)))
        selected = random.sample(words, num_words)
        line = f"{place_type} {' '.join(selected)}"
        if add_number:
            line += f", {randint(0, 999)}"
        results.append(f"'{line}'")
    return results


def City(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """
    Gera cidades brasileiras.

    Uso:
        City     -> cidade aleatória
        City:SP  -> cidade do estado especificado
    """
    _validate_records(records_to_generate)

    if ":" in data_type:
        uf = data_type.split(":")[1]
        lines = _search_in_datasource('CityBR.txt', uf)
    else:
        lines = _get_datasource('CityBR.txt')

    results = []
    for _ in range(records_to_generate):
        line = random.choice(lines)
        parts = line.split(",")
        city = parts[2].strip() if len(parts) > 2 else line.strip()
        results.append(f"'{city}'")
    return results


def StateProvince(records_to_generate: int, data_type: str, value_dict: list) -> list[str]:
    """
    Gera estados/províncias brasileiros.

    Uso:
        StateProvince        -> estado aleatório
        StateProvince:SP     -> filtra por UF (retorna nome do estado)
        StateProvince:Find   -> busca estado compatível com a cidade anterior
    """
    _validate_records(records_to_generate)

    if ":" in data_type:
        param = data_type.split(":")[1]
        if param == "Find":
            # Busca estado compatível com a última cidade gerada
            if not value_dict:
                raise GeneratorError(
                    "StateProvince:Find requer City gerado previamente"
                )
            last_field = value_dict[-1]
            results = []
            for i in range(records_to_generate):
                city_name = str(last_field[i]).replace("'", "")
                matched = _search_in_datasource('CityBR.txt', city_name)
                state = matched[0].split(",")[0].strip()
                results.append(f"'{state}'")
            return results
        else:
            lines = _search_in_datasource('CityBR.txt', param)
    else:
        lines = _get_datasource('StateProvinceBR.txt')

    results = []
    for _ in range(records_to_generate):
        line = random.choice(lines)
        if ":" in data_type:
            state = line.split(",")[0].strip()
        else:
            state = line.strip()
        results.append(f"'{state}'")
    return results


# ---------------------------------------------------------------------------
# Texto genérico
# ---------------------------------------------------------------------------

def Varchar(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera strings aleatórias de comprimento fixo.

    Uso:
        Varchar:N  (ex: Varchar:10)
    """
    _validate_records(records_to_generate)

    parts = data_type.split(":")
    if len(parts) != 2 or not parts[1].isdigit():
        raise GeneratorError(
            f"Formato inválido para Varchar: '{data_type}'. "
            "Esperado: Varchar:N (ex: Varchar:10)"
        )

    length = int(parts[1])
    if length <= 0:
        raise GeneratorError(f"Varchar: comprimento deve ser > 0, recebeu {length}")

    letters = string.ascii_letters
    return [
        "'" + ''.join(random.choices(letters, k=length)) + "'"
        for _ in range(records_to_generate)
    ]


# ---------------------------------------------------------------------------
# Telefone
# ---------------------------------------------------------------------------

def Phone(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera números de telefone brasileiros.

    Uso:
        Phone         -> celular com DDD aleatório: (XX) 9XXXX-XXXX
        Phone:fixo    -> fixo com DDD aleatório: (XX) XXXX-XXXX
        Phone:XX      -> celular com DDD específico (ex: Phone:11)
    """
    _validate_records(records_to_generate)

    results = []
    if ":" in data_type:
        param = data_type.split(":")[1]
        is_fixo = param == "fixo"
        ddd_fixo = None if is_fixo else param
    else:
        is_fixo = False
        ddd_fixo = None

    for _ in range(records_to_generate):
        ddd = ddd_fixo or str(randint(11, 99))
        if is_fixo:
            number = f"({ddd}) {randint(2000, 5999)}-{randint(1000, 9999)}"
        else:
            number = f"({ddd}) 9{randint(1000, 9999)}-{randint(1000, 9999)}"
        results.append(f"'{number}'")
    return results


# ---------------------------------------------------------------------------
# CEP
# ---------------------------------------------------------------------------

_UF_CEP_RANGES: dict[str, tuple[int, int]] = {
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


def CEP(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera CEPs brasileiros aleatórios no formato XXXXX-XXX.

    Uso:
        CEP       -> CEP totalmente aleatório
        CEP:SP    -> CEP na faixa do estado especificado
    """
    _validate_records(records_to_generate)

    uf = None
    if ":" in data_type:
        uf = data_type.split(":")[1].upper()
        if uf not in _UF_CEP_RANGES:
            raise GeneratorError(
                f"UF desconhecida para CEP: '{uf}'. "
                f"Válidas: {', '.join(sorted(_UF_CEP_RANGES.keys()))}"
            )

    results = []
    for _ in range(records_to_generate):
        if uf:
            prefix = randint(*_UF_CEP_RANGES[uf])
        else:
            prefix = randint(1000, 99999)
        suffix = randint(0, 999)
        results.append(f"'{prefix:05d}-{suffix:03d}'")
    return results


# ---------------------------------------------------------------------------
# UUID
# ---------------------------------------------------------------------------

def UUID(records_to_generate: int, data_type: str) -> list[str]:
    """Gera UUIDs v4 aleatórios."""
    _validate_records(records_to_generate)
    return [f"'{_uuid.uuid4()}'" for _ in range(records_to_generate)]


# ---------------------------------------------------------------------------
# Boolean
# ---------------------------------------------------------------------------

def Boolean(records_to_generate: int, data_type: str) -> list:
    """
    Gera valores booleanos aleatórios.

    Uso:
        Boolean          -> TRUE/FALSE
        Boolean:int      -> 1/0
        Boolean:bit      -> 1/0
    """
    _validate_records(records_to_generate)

    use_int = False
    if ":" in data_type:
        param = data_type.split(":")[1].lower()
        use_int = param in ('int', 'bit')

    if use_int:
        return [random.choice((1, 0)) for _ in range(records_to_generate)]
    else:
        return [random.choice(('TRUE', 'FALSE')) for _ in range(records_to_generate)]
