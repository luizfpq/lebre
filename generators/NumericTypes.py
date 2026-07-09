#!/usr/bin/env python3
"""Geradores de tipos numéricos."""

from __future__ import annotations

import random

__all__ = ["Serial", "Integer"]


class GeneratorError(Exception):
    """Erro de configuração ou execução de um gerador."""


def _parse_int(value: str, field_name: str) -> int:
    """Converte string para int com mensagem de erro clara."""
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise GeneratorError(
            f"Valor inválido para '{field_name}': esperado inteiro, recebeu '{value}'"
        ) from exc


def Serial(records_to_generate: int, data_type: str) -> list[int]:
    """
    Gera sequência auto-incremento.

    Uso:
        Serial      -> [0, 1, 2, ...]
        Serial:N    -> [N, N+1, N+2, ...]
    """
    if records_to_generate <= 0:
        raise GeneratorError(f"records_to_generate deve ser > 0, recebeu {records_to_generate}")

    start = 0
    if ":" in data_type:
        parts = data_type.split(":", 1)
        start = _parse_int(parts[1], "Serial:start")

    return list(range(start, start + records_to_generate))


def Integer(records_to_generate: int, data_type: str) -> list[int]:
    """
    Gera inteiros aleatórios em um intervalo.

    Uso:
        Integer:min:max  (ex: Integer:0:10)
    """
    if records_to_generate <= 0:
        raise GeneratorError(f"records_to_generate deve ser > 0, recebeu {records_to_generate}")

    parts = data_type.split(":")
    if len(parts) != 3:
        raise GeneratorError(
            f"Formato inválido para Integer: '{data_type}'. "
            "Esperado: Integer:min:max (ex: Integer:0:100)"
        )

    min_val = _parse_int(parts[1], "Integer:min")
    max_val = _parse_int(parts[2], "Integer:max")

    if min_val > max_val:
        raise GeneratorError(
            f"Integer: min ({min_val}) não pode ser maior que max ({max_val})"
        )

    return [random.randint(min_val, max_val) for _ in range(records_to_generate)]
