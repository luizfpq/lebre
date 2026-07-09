#!/usr/bin/env python3
"""Testes dos geradores individuais."""
import re
import pytest

from generators.NumericTypes import Serial, Integer
from generators.TextTypes import (
    FullName, FirstName, LastName, UserName, Email, CPF, CNPJ,
    Phone, CEP, UUID, Boolean, Varchar, Sex, Address, City, StateProvince,
)
from generators.DateTime import Date, DateTime


# ---------------------------------------------------------------------------
# NumericTypes
# ---------------------------------------------------------------------------

class TestSerial:
    def test_default_start(self):
        result = Serial(5, 'Serial')
        assert result == [0, 1, 2, 3, 4]

    def test_custom_start(self):
        result = Serial(3, 'Serial:100')
        assert result == [100, 101, 102]

    def test_length(self):
        result = Serial(50, 'Serial')
        assert len(result) == 50


class TestInteger:
    def test_range(self):
        result = Integer(100, 'Integer:5:10')
        assert all(5 <= v <= 10 for v in result)

    def test_length(self):
        result = Integer(20, 'Integer:0:100')
        assert len(result) == 20

    def test_single_value_range(self):
        result = Integer(10, 'Integer:7:7')
        assert all(v == 7 for v in result)


# ---------------------------------------------------------------------------
# TextTypes — CPF
# ---------------------------------------------------------------------------

class TestCPF:
    def _validate_cpf(self, cpf_str):
        """Valida CPF com algoritmo dos dígitos verificadores."""
        digits = [int(c) for c in cpf_str if c.isdigit()]
        if len(digits) != 11:
            return False
        # Primeiro dígito verificador
        val = sum((10 - i) * d for i, d in enumerate(digits[:9])) % 11
        d1 = 0 if val < 2 else 11 - val
        if digits[9] != d1:
            return False
        # Segundo dígito verificador
        val = sum((11 - i) * d for i, d in enumerate(digits[:10])) % 11
        d2 = 0 if val < 2 else 11 - val
        return digits[10] == d2

    def test_format(self):
        result = CPF(10, 'CPF')
        for cpf in result:
            assert re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf)

    def test_valid(self):
        result = CPF(50, 'CPF')
        for cpf in result:
            assert self._validate_cpf(cpf), f"CPF inválido: {cpf}"

    def test_length(self):
        result = CPF(25, 'CPF')
        assert len(result) == 25


# ---------------------------------------------------------------------------
# TextTypes — CNPJ
# ---------------------------------------------------------------------------

class TestCNPJ:
    def _validate_cnpj(self, cnpj_str):
        """Valida CNPJ com algoritmo dos dígitos verificadores."""
        digits = [int(c) for c in cnpj_str if c.isdigit()]
        if len(digits) != 14:
            return False
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        val = sum(d * w for d, w in zip(digits[:12], weights1)) % 11
        d1 = 0 if val < 2 else 11 - val
        if digits[12] != d1:
            return False
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        val = sum(d * w for d, w in zip(digits[:13], weights2)) % 11
        d2 = 0 if val < 2 else 11 - val
        return digits[13] == d2

    def test_format(self):
        result = CNPJ(10, 'CNPJ')
        for cnpj in result:
            # Remove aspas SQL
            cnpj_clean = cnpj.strip("'")
            assert re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', cnpj_clean)

    def test_valid(self):
        result = CNPJ(50, 'CNPJ')
        for cnpj in result:
            cnpj_clean = cnpj.strip("'")
            assert self._validate_cnpj(cnpj_clean), f"CNPJ inválido: {cnpj_clean}"


# ---------------------------------------------------------------------------
# TextTypes — Phone
# ---------------------------------------------------------------------------

class TestPhone:
    def test_celular_default(self):
        result = Phone(10, 'Phone')
        for phone in result:
            clean = phone.strip("'")
            assert re.match(r'^\(\d{2}\) 9\d{4}-\d{4}$', clean)

    def test_fixo(self):
        result = Phone(10, 'Phone:fixo')
        for phone in result:
            clean = phone.strip("'")
            assert re.match(r'^\(\d{2}\) \d{4}-\d{4}$', clean)

    def test_ddd_especifico(self):
        result = Phone(10, 'Phone:11')
        for phone in result:
            clean = phone.strip("'")
            assert clean.startswith('(11)')


# ---------------------------------------------------------------------------
# TextTypes — CEP
# ---------------------------------------------------------------------------

class TestCEP:
    def test_format(self):
        result = CEP(10, 'CEP')
        for cep in result:
            clean = cep.strip("'")
            assert re.match(r'^\d{5}-\d{3}$', clean)

    def test_uf_filter(self):
        result = CEP(20, 'CEP:SP')
        for cep in result:
            clean = cep.strip("'")
            prefix = int(clean.split('-')[0])
            assert 1000 <= prefix <= 19999


# ---------------------------------------------------------------------------
# TextTypes — UUID
# ---------------------------------------------------------------------------

class TestUUID:
    def test_format(self):
        result = UUID(10, 'UUID')
        for u in result:
            clean = u.strip("'")
            assert re.match(
                r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
                clean
            )

    def test_unique(self):
        result = UUID(100, 'UUID')
        cleaned = [u.strip("'") for u in result]
        assert len(set(cleaned)) == 100


# ---------------------------------------------------------------------------
# TextTypes — Boolean
# ---------------------------------------------------------------------------

class TestBoolean:
    def test_text_mode(self):
        result = Boolean(50, 'Boolean')
        assert all(v in ('TRUE', 'FALSE') for v in result)

    def test_int_mode(self):
        result = Boolean(50, 'Boolean:int')
        assert all(v in (0, 1) for v in result)

    def test_bit_mode(self):
        result = Boolean(50, 'Boolean:bit')
        assert all(v in (0, 1) for v in result)


# ---------------------------------------------------------------------------
# TextTypes — Varchar
# ---------------------------------------------------------------------------

class TestVarchar:
    def test_length(self):
        result = Varchar(10, 'Varchar:8')
        for v in result:
            # Remove aspas SQL externas
            clean = v.strip("'")
            assert len(clean) == 8

    def test_alpha_only(self):
        result = Varchar(20, 'Varchar:5')
        for v in result:
            clean = v.strip("'")
            assert clean.isalpha()


# ---------------------------------------------------------------------------
# TextTypes — FullName, FirstName, LastName, UserName, Email
# ---------------------------------------------------------------------------

class TestNameGenerators:
    def test_fullname_returns_quoted(self):
        result = FullName(10, 'FullName')
        for name in result:
            assert name.startswith("'") and name.endswith("'")
            inner = name.strip("'")
            assert len(inner.split()) >= 2  # pelo menos nome + sobrenome

    def test_firstname_from_fullname(self):
        fullnames = FullName(10, 'FullName')
        result = FirstName(10, 'FirstName', [fullnames])
        for i, fn in enumerate(result):
            clean = fn.strip("'")
            full_clean = fullnames[i].strip("'")
            assert clean == full_clean.split()[0]

    def test_lastname_from_fullname(self):
        fullnames = FullName(10, 'FullName')
        result = LastName(10, 'LastName', [fullnames])
        for i, ln in enumerate(result):
            clean = ln.strip("'")
            full_clean = fullnames[i].strip("'")
            assert clean == full_clean.split()[-1]

    def test_username(self):
        fullnames = FullName(10, 'FullName')
        result = UserName(10, 'UserName', [fullnames])
        for u in result:
            clean = u.strip("'")
            assert clean.islower()
            assert len(clean) >= 2

    def test_username_with_number(self):
        fullnames = FullName(10, 'FullName')
        result = UserName(10, 'UserName:Num', [fullnames])
        for u in result:
            clean = u.strip("'")
            assert re.search(r'\d{6}$', clean)

    def test_email_format(self):
        fullnames = FullName(10, 'FullName')
        result = Email(10, 'Email', [fullnames])
        for e in result:
            clean = e.strip("'")
            assert '@example.com' in clean
            assert '.' in clean.split('@')[0]


# ---------------------------------------------------------------------------
# TextTypes — Sex
# ---------------------------------------------------------------------------

class TestSex:
    def test_returns_values(self):
        result = Sex(20, 'Sex')
        for s in result:
            clean = s.strip("'")
            assert len(clean) > 0


# ---------------------------------------------------------------------------
# DateTime
# ---------------------------------------------------------------------------

class TestDate:
    def test_default_format(self):
        result = Date(10, 'Date')
        for d in result:
            clean = d.strip("'")
            assert re.match(r'^\d{2}/\d{2}/\d{4}$', clean)

    def test_custom_range(self):
        result = Date(10, 'Date:01/01/2020:31/12/2020')
        for d in result:
            clean = d.strip("'")
            year = int(clean.split('/')[2])
            assert year == 2020

    def test_length(self):
        result = Date(30, 'Date')
        assert len(result) == 30


class TestDateTime:
    def test_format(self):
        result = DateTime(10, 'DateTime')
        for dt in result:
            clean = dt.strip("'")
            # Formato: dd/mm/yyyy HH:MM AM/PM
            assert re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2} [AP]M$', clean)
