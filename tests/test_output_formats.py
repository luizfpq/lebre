#!/usr/bin/env python3
"""Testes de validação dos formatos de saída (SQL, CSV, JSON)."""

import csv
import io
import json
import re
import sys
import os

import pytest

# Garante que o projeto é importável
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import _load_table_file, _generate_values, _populate_sql, _populate_csv, _populate_json
from generators.DataLoader import DataLoad


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_table(tmp_path):
    """Cria uma definição de tabela simples."""
    table = [{
        "TableName": "tbl_produtos",
        "FieldList": "id,codigo,nome,ativo",
        "DataType": "Serial,UUID,Varchar:20,Boolean",
        "RecordsToGenerate": 25,
    }]
    filepath = tmp_path / "produtos.json"
    filepath.write_text(json.dumps(table), encoding='utf-8')
    return str(filepath)


@pytest.fixture
def name_table(tmp_path):
    """Cria tabela com tipos dependentes de FullName."""
    table = [{
        "TableName": "tbl_pessoas",
        "FieldList": "id,nome,sobrenome,usuario,email",
        "DataType": "Serial,FullName,LastName,UserName,Email",
        "RecordsToGenerate": 15,
    }]
    filepath = tmp_path / "pessoas.json"
    filepath.write_text(json.dumps(table), encoding='utf-8')
    return str(filepath)


# ---------------------------------------------------------------------------
# Testes SQL
# ---------------------------------------------------------------------------

class TestSQLOutput:
    def test_valid_sql_structure(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output), dialect='postgresql')
        content = output.read_text()

        assert content.startswith('INSERT INTO')
        assert 'VALUES' in content
        assert content.strip().endswith(';')

    def test_postgresql_quoting(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output), dialect='postgresql')
        content = output.read_text()

        assert '"tbl_produtos"' in content
        assert '"id"' in content

    def test_mysql_quoting(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output), dialect='mysql')
        content = output.read_text()

        assert '`tbl_produtos`' in content
        assert '`id`' in content

    def test_sqlite_no_quoting(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output), dialect='sqlite')
        content = output.read_text()

        # sqlite: sem aspas
        first_line = content.splitlines()[1]  # linha com nome da tabela
        assert '`' not in first_line
        assert '"' not in first_line

    def test_correct_row_count(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output))
        content = output.read_text()

        # Conta linhas que começam com tab + (
        value_lines = [l for l in content.splitlines() if l.strip().startswith('(')]
        assert len(value_lines) == 25

    def test_last_row_ends_with_semicolon(self, simple_table, tmp_path):
        output = tmp_path / "out.sql"
        _populate_sql([simple_table], str(output))
        content = output.read_text()

        value_lines = [l for l in content.splitlines() if l.strip().startswith('(')]
        assert value_lines[-1].strip().endswith(';')
        # Todas as outras terminam com vírgula
        for line in value_lines[:-1]:
            assert line.strip().endswith(',')


# ---------------------------------------------------------------------------
# Testes CSV
# ---------------------------------------------------------------------------

class TestCSVOutput:
    def test_parseable_csv(self, simple_table, tmp_path):
        output = tmp_path / "out.csv"
        _populate_csv([simple_table], str(output))
        content = output.read_text()

        reader = csv.reader(io.StringIO(content.strip()))
        rows = list(reader)
        assert rows[0] == ['id', 'codigo', 'nome', 'ativo']
        assert len(rows) == 26  # header + 25

    def test_no_sql_quotes_in_csv(self, simple_table, tmp_path):
        output = tmp_path / "out.csv"
        _populate_csv([simple_table], str(output))
        content = output.read_text()

        # Valores não devem ter aspas SQL simples
        lines = content.strip().splitlines()[1:]  # pula header
        for line in lines:
            # Valores UUID e Varchar não devem estar entre aspas simples
            assert not re.search(r",'[^']*'", line) or "'" not in line


# ---------------------------------------------------------------------------
# Testes JSON
# ---------------------------------------------------------------------------

class TestJSONOutput:
    def test_valid_json(self, simple_table, tmp_path):
        output = tmp_path / "out.json"
        _populate_json([simple_table], str(output))
        content = output.read_text()

        data = json.loads(content)
        assert isinstance(data, dict)
        assert 'tbl_produtos' in data

    def test_correct_structure(self, simple_table, tmp_path):
        output = tmp_path / "out.json"
        _populate_json([simple_table], str(output))
        data = json.loads(output.read_text())

        rows = data['tbl_produtos']
        assert len(rows) == 25
        for row in rows:
            assert set(row.keys()) == {'id', 'codigo', 'nome', 'ativo'}

    def test_no_sql_quotes_in_json(self, simple_table, tmp_path):
        output = tmp_path / "out.json"
        _populate_json([simple_table], str(output))
        data = json.loads(output.read_text())

        for row in data['tbl_produtos']:
            for val in row.values():
                if isinstance(val, str):
                    assert not (val.startswith("'") and val.endswith("'"))

    def test_serial_is_int(self, simple_table, tmp_path):
        output = tmp_path / "out.json"
        _populate_json([simple_table], str(output))
        data = json.loads(output.read_text())

        for row in data['tbl_produtos']:
            assert isinstance(row['id'], int)

    def test_name_dependent_fields(self, name_table, tmp_path):
        output = tmp_path / "out.json"
        _populate_json([name_table], str(output))
        data = json.loads(output.read_text())

        for row in data['tbl_pessoas']:
            assert '@example.com' in row['email']
            assert len(row['usuario']) >= 2
            # Sobrenome deve ser parte do nome completo
            full_parts = row['nome'].split()
            assert row['sobrenome'] == full_parts[-1]


# ---------------------------------------------------------------------------
# Testes de error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_invalid_json_file(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{ invalid json", encoding='utf-8')

        from cli import TableFileError
        with pytest.raises(TableFileError, match="Erro de parse"):
            _load_table_file(str(bad_file))

    def test_missing_fields(self, tmp_path):
        incomplete = tmp_path / "incomplete.json"
        incomplete.write_text(json.dumps([{"TableName": "x"}]), encoding='utf-8')

        from cli import TableFileError
        with pytest.raises(TableFileError, match="obrigatórios ausentes"):
            _load_table_file(str(incomplete))

    def test_fields_types_count_mismatch(self, tmp_path):
        bad_table = tmp_path / "mismatch.json"
        bad_table.write_text(json.dumps([{
            "TableName": "x",
            "FieldList": "a,b,c",
            "DataType": "Serial,CPF",
            "RecordsToGenerate": 5,
        }]), encoding='utf-8')

        from cli import TableFileError
        with pytest.raises(TableFileError, match="Inconsistência"):
            _load_table_file(str(bad_table))

    def test_nonexistent_file(self):
        from cli import TableFileError
        with pytest.raises(TableFileError, match="não encontrado"):
            _load_table_file("/tmp/arquivo_que_nao_existe_xyz.json")

    def test_unknown_data_type(self, tmp_path):
        bad_table = tmp_path / "unknown.json"
        bad_table.write_text(json.dumps([{
            "TableName": "x",
            "FieldList": "a",
            "DataType": "TipoInexistente",
            "RecordsToGenerate": 5,
        }]), encoding='utf-8')

        from generators.DataLoader import GeneratorError
        table_dict = _load_table_file(str(bad_table))
        with pytest.raises(GeneratorError, match="desconhecido"):
            _generate_values(table_dict)
