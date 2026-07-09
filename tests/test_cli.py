#!/usr/bin/env python3
"""Testes end-to-end do CLI via subprocess."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

CLI = [sys.executable, "-m", "cli"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cli(*args, cwd=None, input_text=None):
    """Executa o CLI e retorna (returncode, stdout, stderr)."""
    result = subprocess.run(
        [*CLI, *args],
        capture_output=True,
        text=True,
        cwd=cwd or ROOT,
        input=input_text,
        timeout=30,
    )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# Testes de help e version
# ---------------------------------------------------------------------------

class TestCLIBasics:
    def test_help(self):
        rc, out, _ = run_cli('--help')
        assert rc == 0
        assert 'Lebre' in out

    def test_version(self):
        rc, out, _ = run_cli('--version')
        assert rc == 0
        assert '2.2.0' in out

    def test_no_command_shows_help(self):
        rc, out, _ = run_cli()
        assert rc == 0
        assert 'Lebre' in out or 'usage' in out.lower()

    def test_list_types(self):
        rc, out, _ = run_cli('list-types')
        assert rc == 0
        assert 'Serial' in out
        assert 'CPF' in out
        assert 'FullName' in out


# ---------------------------------------------------------------------------
# Testes de create-table
# ---------------------------------------------------------------------------

class TestCreateTable:
    def test_create_json(self, tmp_path):
        rc, out, err = run_cli(
            'create-table',
            '--name', 'tbl_users',
            '--fields', 'id,nome,email',
            '--types', 'Serial,FullName,Email',
            '--records', '10',
            '--tables-dir', str(tmp_path),
        )
        assert rc == 0
        assert 'Tabela salva' in out

        # Verifica que o arquivo foi criado e é JSON válido
        files = list(tmp_path.glob('*.json'))
        assert len(files) == 1
        with open(files[0]) as f:
            data = json.load(f)
        assert data[0]['TableName'] == 'tbl_users'
        assert data[0]['RecordsToGenerate'] == 10

    def test_create_toml(self, tmp_path):
        rc, out, err = run_cli(
            'create-table',
            '--name', 'tbl_x',
            '--fields', 'id,val',
            '--types', 'Serial,Integer:0:10',
            '--records', '5',
            '--tables-dir', str(tmp_path),
            '--table-format', 'toml',
        )
        assert rc == 0
        files = list(tmp_path.glob('*.toml'))
        assert len(files) == 1

    def test_fields_types_mismatch(self, tmp_path):
        rc, out, err = run_cli(
            'create-table',
            '--name', 'bad',
            '--fields', 'a,b,c',
            '--types', 'Serial,CPF',
            '--records', '5',
            '--tables-dir', str(tmp_path),
        )
        assert rc == 1
        assert 'difere' in err or 'número' in err


# ---------------------------------------------------------------------------
# Testes de populate
# ---------------------------------------------------------------------------

class TestPopulate:
    @pytest.fixture
    def table_dir(self, tmp_path):
        """Cria um diretório com uma tabela de teste."""
        table = [{
            "TableName": "tbl_test",
            "FieldList": "id,cpf,nome,email",
            "DataType": "Serial,CPF,FullName,Email",
            "RecordsToGenerate": 10,
        }]
        table_file = tmp_path / "00_tbl_test.json"
        table_file.write_text(json.dumps(table), encoding='utf-8')
        return tmp_path

    def test_populate_sql_stdout(self, table_dir):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--format', 'sql',
            '--stdout',
        )
        assert rc == 0
        assert 'INSERT INTO' in out
        assert 'VALUES' in out
        # Verifica que tem 10 linhas de valores
        value_lines = [l for l in out.splitlines() if l.strip().startswith('(')]
        assert len(value_lines) == 10

    def test_populate_csv_stdout(self, table_dir):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--format', 'csv',
            '--stdout',
        )
        assert rc == 0
        lines = [l for l in out.strip().splitlines() if l.strip()]
        assert lines[0] == 'id,cpf,nome,email'  # header
        assert len(lines) == 11  # header + 10 registros

    def test_populate_json_stdout(self, table_dir):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--format', 'json',
            '--stdout',
        )
        assert rc == 0
        data = json.loads(out)
        assert 'tbl_test' in data
        assert len(data['tbl_test']) == 10
        # Verifica que cada registro tem os campos corretos
        for row in data['tbl_test']:
            assert set(row.keys()) == {'id', 'cpf', 'nome', 'email'}

    def test_populate_to_file(self, table_dir, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--output-dir', str(output_dir),
            '--format', 'sql',
        )
        assert rc == 0
        assert 'Arquivo gerado' in out
        files = list(output_dir.glob('*.sql'))
        assert len(files) == 1

    def test_populate_mysql_dialect(self, table_dir):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--format', 'sql',
            '--dialect', 'mysql',
            '--stdout',
        )
        assert rc == 0
        assert '`tbl_test`' in out

    def test_populate_sqlite_dialect(self, table_dir):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(table_dir),
            '--format', 'sql',
            '--dialect', 'sqlite',
            '--stdout',
        )
        assert rc == 0
        assert 'tbl_test' in out
        # sqlite não usa quotes
        assert '`' not in out
        assert '"' not in out.replace('"tbl_test"', '')  # ignora possível no nome

    def test_populate_empty_dir(self, tmp_path):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', str(tmp_path),
            '--stdout',
        )
        assert rc == 1
        assert 'Nenhuma tabela' in err

    def test_populate_nonexistent_dir(self):
        rc, out, err = run_cli(
            'populate',
            '--tables-dir', '/tmp/naoexiste_xyz_lebre',
            '--stdout',
        )
        assert rc == 1
        assert 'não encontrado' in err or 'Erro' in err
