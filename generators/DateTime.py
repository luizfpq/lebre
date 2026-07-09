#!/usr/bin/env python3
"""Geradores de tipos de data e hora."""

from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING

__all__ = ["Date", "DateTime"]


class GeneratorError(Exception):
    """Erro de configuração ou execução de um gerador."""


def _random_timestamp(start_ts: float, end_ts: float) -> float:
    """Retorna timestamp aleatório entre start_ts e end_ts."""
    return start_ts + random.random() * (end_ts - start_ts)


def _parse_date_range(data_type: str, fmt: str, default_start: str, default_end: str) -> tuple[float, float]:
    """
    Extrai e valida intervalo de datas do data_type.
    Retorna (start_timestamp, end_timestamp).
    """
    if ":" in data_type:
        parts = data_type.split(":", 2)
        if len(parts) < 3:
            raise GeneratorError(
                f"Formato inválido: '{data_type}'. "
                f"Esperado: Tipo:inicio:fim (ex: Date:01/01/2020:31/12/2020)"
            )
        start_str, end_str = parts[1], parts[2]
    else:
        start_str, end_str = default_start, default_end

    try:
        start_ts = time.mktime(time.strptime(start_str, fmt))
    except (ValueError, OverflowError) as exc:
        raise GeneratorError(
            f"Data de início inválida: '{start_str}'. Formato esperado: {fmt}"
        ) from exc

    try:
        end_ts = time.mktime(time.strptime(end_str, fmt))
    except (ValueError, OverflowError) as exc:
        raise GeneratorError(
            f"Data de fim inválida: '{end_str}'. Formato esperado: {fmt}"
        ) from exc

    if start_ts > end_ts:
        raise GeneratorError(
            f"Data de início ({start_str}) é posterior à data de fim ({end_str})"
        )

    return start_ts, end_ts


def Date(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera datas aleatórias no formato dd/mm/yyyy.

    Uso:
        Date                        -> entre 01/01/1970 e 01/01/2000
        Date:01/01/1990:31/12/2020  -> intervalo especificado
    """
    if records_to_generate <= 0:
        raise GeneratorError(f"records_to_generate deve ser > 0, recebeu {records_to_generate}")

    fmt = '%d/%m/%Y'
    start_ts, end_ts = _parse_date_range(data_type, fmt, "01/01/1970", "01/01/2000")

    results = []
    for _ in range(records_to_generate):
        ts = _random_timestamp(start_ts, end_ts)
        results.append("'" + time.strftime(fmt, time.localtime(ts)) + "'")
    return results


def DateTime(records_to_generate: int, data_type: str) -> list[str]:
    """
    Gera datas com hora aleatórias no formato dd/mm/yyyy HH:MM AM/PM.

    Uso:
        DateTime  -> entre 01/01/1970 e 01/01/2000
    """
    if records_to_generate <= 0:
        raise GeneratorError(f"records_to_generate deve ser > 0, recebeu {records_to_generate}")

    fmt = '%d/%m/%Y %I:%M %p'
    start_ts = time.mktime(time.strptime("01/01/1970 12:00 AM", fmt))
    end_ts = time.mktime(time.strptime("01/01/2000 11:59 PM", fmt))

    results = []
    for _ in range(records_to_generate):
        ts = _random_timestamp(start_ts, end_ts)
        results.append("'" + time.strftime(fmt, time.localtime(ts)) + "'")
    return results
