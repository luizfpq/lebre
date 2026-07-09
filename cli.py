#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Lebre CLI — command-line interface for the database populator.

    Usage:
        lebre create-table --name tbl_users --fields "id,nome,email" \
                           --types "Serial,FullName,Email" --records 100
        lebre populate [--tables-dir tables] [--output-dir results] [--format sql]
        lebre list-types
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__license__ = "GPL v3"
__version__ = "2.1.0"

import argparse
import json
import os
import sys
import glob
import tomllib

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from generators.DataLoader import DataLoad
from generators.Getters import get_table_name, get_count_records_to_generate, get_count_field_list


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_next_number(directory, extension):
    """Determina o próximo número sequencial para arquivos no formato NN_nome.ext"""
    if not os.path.exists(directory):
        os.makedirs(directory)

    files = glob.glob(os.path.join(directory, f'*.{extension}'))
    numbers = []
    for f in files:
        basename = os.path.basename(f)
        try:
            numbers.append(int(basename.split('_')[0]))
        except (ValueError, IndexError):
            continue
    return max(numbers) + 1 if numbers else 0


def _load_table_file(filepath):
    """Carrega definição de tabela de JSON, YAML ou TOML. Retorna lista de dicts."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.json':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif ext in ('.yaml', '.yml'):
        if not HAS_YAML:
            print("Erro: pacote 'pyyaml' não instalado. Instale com: pip install pyyaml",
                  file=sys.stderr)
            sys.exit(1)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    elif ext == '.toml':
        with open(filepath, 'rb') as f:
            data = tomllib.load(f)
        # TOML retorna dict; normalizar para lista
        if isinstance(data, dict) and 'TableName' in data:
            data = [data]
        elif isinstance(data, dict) and 'table' in data:
            # suporte a [table] como seção
            data = [data['table']]
    else:
        print(f"Formato não suportado: '{ext}'. Use .json, .yaml ou .toml.", file=sys.stderr)
        sys.exit(1)

    # Normalizar: se veio dict solto, envelopar em lista
    if isinstance(data, dict):
        data = [data]

    return data


def _find_table_files(tables_dir):
    """Busca todos os arquivos de tabela suportados no diretório, ordenados."""
    patterns = ['*.json', '*.yaml', '*.yml', '*.toml']
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(tables_dir, pat)))
    return sorted(set(files))


AVAILABLE_TYPES = [
    "Serial[:start]", "Integer:min:max",
    "FullName", "FirstName", "LastName", "UserName[:Num]", "Email", "InitName",
    "CPF", "CNPJ", "Phone[:fixo|DDD]", "CEP[:UF]",
    "Sex", "Varchar:size",
    "Address[:Num]", "City[:UF]", "StateProvince[:Find|UF]",
    "Date[:dd/mm/yyyy:dd/mm/yyyy]", "DateTime",
    "UUID", "Boolean[:int|bit]",
    "Default:value",
]


# ---------------------------------------------------------------------------
# create-table
# ---------------------------------------------------------------------------

def cmd_create_table(args):
    """Cria um arquivo de definição de tabela (JSON, YAML ou TOML)."""
    tables_dir = args.tables_dir
    table_format = args.table_format

    table = {
        "TableName": args.name,
        "FieldList": args.fields,
        "DataType": args.types,
        "RecordsToGenerate": args.records,
    }

    num = get_next_number(tables_dir, table_format)
    filename = os.path.join(tables_dir, f"{num:02d}_{args.name}.{table_format}")

    if table_format == 'json':
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([table], f, indent=4, ensure_ascii=False)
    elif table_format in ('yaml', 'yml'):
        if not HAS_YAML:
            print("Erro: pacote 'pyyaml' não instalado. Instale com: pip install pyyaml",
                  file=sys.stderr)
            sys.exit(1)
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(table, f, default_flow_style=False, allow_unicode=True)
    elif table_format == 'toml':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('[table]\n')
            f.write(f'TableName = "{table["TableName"]}"\n')
            f.write(f'FieldList = "{table["FieldList"]}"\n')
            f.write(f'DataType = "{table["DataType"]}"\n')
            f.write(f'RecordsToGenerate = {table["RecordsToGenerate"]}\n')

    print(f"Tabela salva em '{filename}'.")


# ---------------------------------------------------------------------------
# populate
# ---------------------------------------------------------------------------

def cmd_populate(args):
    """Gera arquivo de saída a partir das definições em tables_dir."""
    tables_dir = args.tables_dir
    output_dir = args.output_dir
    output_format = args.format
    use_stdout = args.stdout

    table_files = _find_table_files(tables_dir)
    if not table_files:
        print(f"Nenhuma tabela encontrada em '{tables_dir}/'.", file=sys.stderr)
        sys.exit(1)

    if use_stdout:
        output_file = None
    else:
        num = get_next_number(output_dir, output_format)
        output_file = os.path.join(output_dir, f"{num:02d}_saida.{output_format}")

    if output_format == 'sql':
        _populate_sql(table_files, output_file, dialect=args.dialect)
    elif output_format == 'csv':
        _populate_csv(table_files, output_file)
    elif output_format == 'json':
        _populate_json(table_files, output_file)
    else:
        print(f"Formato '{output_format}' não suportado.", file=sys.stderr)
        sys.exit(1)

    if not use_stdout:
        print(f"Arquivo gerado: '{output_file}'.")


def _generate_values(table_dict):
    """Gera value_dict para uma definição de tabela (lógica extraída do table_populator)."""
    records = get_count_records_to_generate(table_dict)
    field_count = get_count_field_list(table_dict)
    data_list = [item.strip() for item in table_dict[0]['DataType'].split(",")]

    value_dict = []
    fullname_values = []

    # Gera FullName primeiro (necessário para FirstName, LastName, UserName, Email)
    has_fullname_field = any('FullName' in item for item in data_list)
    needs_fullname = any(k in item for item in data_list for k in ['FirstName', 'LastName', 'UserName', 'Email'])

    if has_fullname_field or needs_fullname:
        for item in data_list:
            if 'FullName' in item:
                fullname_values = DataLoad(records, item.strip(), value_dict)
                break
        else:
            fullname_values = DataLoad(records, 'FullName', value_dict)

    # Gera os outros campos
    for item in data_list:
        if 'FullName' not in item:
            if any(k in item for k in ['FirstName', 'LastName', 'UserName', 'Email']):
                values = DataLoad(records, item.strip(), [fullname_values])
            else:
                values = DataLoad(records, item.strip(), value_dict)
            value_dict.append(values)

    # Insere FullName na posição correta se estava no DataType
    for i, item in enumerate(data_list):
        if 'FullName' in item:
            value_dict.insert(i, [f"{name}" for name in fullname_values])
            break

    return value_dict, records, field_count


def _quote_identifier(name, dialect):
    """Aplica quoting ao nome de tabela/coluna conforme o dialeto SQL."""
    if dialect == 'mysql':
        return f'`{name}`'
    elif dialect == 'postgresql':
        return f'"{name}"'
    else:  # sqlite
        return name


def _populate_sql(table_files, output_file, dialect='postgresql'):
    """Gera saída no formato SQL INSERT."""
    fh = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    try:
        for tf in table_files:
            table_dict = _load_table_file(tf)

            table_name = get_table_name(table_dict)
            value_dict, records, field_count = _generate_values(table_dict)

            # Quoting do nome da tabela e campos
            quoted_table = _quote_identifier(table_name, dialect)
            fields = [f.strip() for f in table_dict[0]['FieldList'].split(',')]
            quoted_fields = ', '.join(_quote_identifier(f, dialect) for f in fields)

            fh.write(f'INSERT INTO\n\t{quoted_table} ({quoted_fields})\nVALUES\n')

            for i in range(records):
                values = ', '.join(str(value_dict[col][i]) for col in range(field_count))
                separator = ';' if i == records - 1 else ','
                fh.write(f"\t({values}){separator}\n")
    finally:
        if output_file:
            fh.close()


def _populate_csv(table_files, output_file):
    """Gera saída no formato CSV (uma tabela por seção, separadas por linha em branco)."""
    fh = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    try:
        for tf in table_files:
            table_dict = _load_table_file(tf)

            fields = [field.strip() for field in table_dict[0]['FieldList'].split(',')]
            value_dict, records, field_count = _generate_values(table_dict)

            # Header
            fh.write(','.join(fields) + '\n')

            # Rows
            for i in range(records):
                row = []
                for col in range(field_count):
                    val = str(value_dict[col][i])
                    # Remove aspas SQL simples para CSV
                    if val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    row.append(val)
                fh.write(','.join(row) + '\n')

            fh.write('\n')
    finally:
        if output_file:
            fh.close()


def _populate_json(table_files, output_file):
    """Gera saída no formato JSON (array de objetos por tabela)."""
    output = {}

    for tf in table_files:
        table_dict = _load_table_file(tf)

        table_name = get_table_name(table_dict)
        fields = [field.strip() for field in table_dict[0]['FieldList'].split(',')]
        value_dict, records, field_count = _generate_values(table_dict)

        rows = []
        for i in range(records):
            row = {}
            for col in range(field_count):
                val = value_dict[col][i]
                # Remove aspas SQL simples para JSON
                if isinstance(val, str) and val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                row[fields[col]] = val
            rows.append(row)

        output[table_name] = rows

    fh = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    try:
        json.dump(output, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    finally:
        if output_file:
            fh.close()


# ---------------------------------------------------------------------------
# list-types
# ---------------------------------------------------------------------------

def cmd_list_types(args):
    """Lista os tipos de dados disponíveis."""
    print("Tipos de dados disponíveis:\n")
    for t in AVAILABLE_TYPES:
        print(f"  - {t}")
    print("\nExemplo de uso:")
    print('  lebre create-table --name tbl_users \\')
    print('    --fields "id,cpf,nome,sobrenome,email" \\')
    print('    --types "Serial,CPF,FirstName,LastName,Email" \\')
    print('    --records 100')


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog='lebre',
        description='Lebre — Database Populator. Gera dados fictícios para popular tabelas.',
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # create-table
    ct = subparsers.add_parser('create-table', help='Cria definição de tabela (JSON, YAML ou TOML)')
    ct.add_argument('--name', required=True, help='Nome da tabela')
    ct.add_argument('--fields', required=True, help='Campos separados por vírgula')
    ct.add_argument('--types', required=True, help='Tipos de dados separados por vírgula (use list-types para ver)')
    ct.add_argument('--records', type=int, required=True, help='Número de registros a gerar')
    ct.add_argument('--tables-dir', default='tables', help='Diretório para salvar (default: tables)')
    ct.add_argument('--table-format', choices=['json', 'yaml', 'toml'], default='json',
                     help='Formato do arquivo de tabela (default: json)')
    ct.set_defaults(func=cmd_create_table)

    # populate
    pop = subparsers.add_parser('populate', help='Gera dados a partir das tabelas definidas')
    pop.add_argument('--tables-dir', default='tables', help='Diretório com JSONs de tabela (default: tables)')
    pop.add_argument('--output-dir', default='results', help='Diretório de saída (default: results)')
    pop.add_argument('--format', choices=['sql', 'csv', 'json'], default='sql',
                     help='Formato de saída (default: sql)')
    pop.add_argument('--dialect', choices=['postgresql', 'mysql', 'sqlite'], default='postgresql',
                     help='Dialeto SQL para quoting (default: postgresql)')
    pop.add_argument('--stdout', action='store_true',
                     help='Imprime no terminal em vez de salvar em arquivo')
    pop.set_defaults(func=cmd_populate)

    # list-types
    lt = subparsers.add_parser('list-types', help='Lista tipos de dados disponíveis')
    lt.set_defaults(func=cmd_list_types)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == '__main__':
    main()
