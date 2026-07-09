#!/usr/bin/env python3
"""
Dispatcher de tipos de dados — roteia para o gerador correto conforme data_type.
"""

from __future__ import annotations

from generators.TextTypes import (
    FullName, FirstName, LastName, UserName, Email, InitName,
    Sex, CPF, CNPJ, Phone, CEP, UUID, Boolean,
    Varchar, Address, City, StateProvince, ForeignKey,
    GeneratorError, set_locale,
)
from generators.DateTime import Date, DateTime
from generators.NumericTypes import Serial, Integer

__all__ = ["DataLoad", "GeneratorError", "set_locale"]


# ---------------------------------------------------------------------------
# Dispatch table — mapeia prefixo do tipo para (função, aceita_value_dict)
# ---------------------------------------------------------------------------

# Geradores que NÃO recebem value_dict (independentes)
_INDEPENDENT_GENERATORS: dict[str, callable] = {
    'Serial': Serial,
    'Integer': Integer,
    'FullName': FullName,
    'CPF': CPF,
    'CNPJ': CNPJ,
    'Phone': Phone,
    'CEP': CEP,
    'UUID': UUID,
    'Boolean': Boolean,
    'Varchar': Varchar,
    'Sex': Sex,
    'Address': Address,
    'Date': Date,
    'DateTime': DateTime,
}

# Geradores que RECEBEM value_dict (dependem de campos anteriores)
_DEPENDENT_GENERATORS: dict[str, callable] = {
    'FirstName': FirstName,
    'LastName': LastName,
    'UserName': UserName,
    'Email': Email,
    'InitName': InitName,
    'City': City,
    'StateProvince': StateProvince,
}

# Ordem de resolução — tipos mais específicos primeiro para evitar match parcial
# (ex: "DateTime" antes de "Date", "StateProvince" antes de qualquer substring)
_DISPATCH_ORDER: list[tuple[str, callable, bool]] = [
    # (prefixo, função, requer_value_dict)
    ('DateTime', DateTime, False),
    ('Date', Date, False),
    ('StateProvince', StateProvince, True),
    ('FirstName', FirstName, True),
    ('LastName', LastName, True),
    ('FullName', FullName, False),
    ('UserName', UserName, True),
    ('Email', Email, True),
    ('InitName', InitName, True),
    ('Serial', Serial, False),
    ('Integer', Integer, False),
    ('CPF', CPF, False),
    ('CNPJ', CNPJ, False),
    ('Phone', Phone, False),
    ('CEP', CEP, False),
    ('UUID', UUID, False),
    ('Boolean', Boolean, False),
    ('Varchar', Varchar, False),
    ('Sex', Sex, False),
    ('Address', Address, False),
    ('City', City, True),
    ('ForeignKey', None, False),  # tratado separadamente
    ('Default', None, False),
]


def DataLoad(records_to_generate: int, data_type: str, value_dict: list,
             context: dict | None = None) -> list:
    """
    Dispatcher principal — roteia para o gerador correto conforme data_type.

    Args:
        records_to_generate: Número de registros a gerar.
        data_type: Tipo de dado (ex: 'Serial', 'CPF', 'FullName', 'Integer:0:100').
        value_dict: Lista de campos já gerados (para tipos dependentes).
        context: Dict com dados inter-tabela (para ForeignKey).

    Returns:
        Lista com os valores gerados.

    Raises:
        GeneratorError: Se o tipo não for reconhecido ou houver erro de configuração.
    """
    if records_to_generate <= 0:
        raise GeneratorError(
            f"records_to_generate deve ser > 0, recebeu {records_to_generate}"
        )

    data_type = data_type.strip()

    for prefix, generator_fn, needs_value_dict in _DISPATCH_ORDER:
        if prefix in data_type:
            # Caso especial: ForeignKey precisa de context inter-tabela
            if prefix == 'ForeignKey':
                return ForeignKey(records_to_generate, data_type, context or {})

            # Caso especial: Default retorna valor fixo
            if prefix == 'Default':
                parts = data_type.split(":", 1)
                if len(parts) < 2:
                    raise GeneratorError(
                        f"Formato inválido para Default: '{data_type}'. "
                        "Esperado: Default:valor (ex: Default:'ativo')"
                    )
                value = parts[1]
                return [value] * records_to_generate

            if needs_value_dict:
                return generator_fn(records_to_generate, data_type, value_dict)
            else:
                return generator_fn(records_to_generate, data_type)

    raise GeneratorError(
        f"Tipo de dado desconhecido: '{data_type}'. "
        f"Use 'lebre list-types' para ver os tipos disponíveis."
    )
