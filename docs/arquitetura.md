# Arquitetura Interna

> Como o Lebre funciona por dentro. Documento para contribuidores e mantenedores.

---

## Visao geral do fluxo

```
Usuario
  |
  v
cli.py (argparse)
  |
  ├── cmd_create_table()   --> escreve JSON/YAML/TOML em tables/
  |
  └── cmd_populate()
        |
        ├── set_locale()           --> configura locale global
        ├── _find_table_files()    --> lista arquivos em tables/
        |
        └── Para cada tabela:
              |
              ├── _load_table_file()   --> parse + validacao
              ├── _generate_values()   --> gera dados
              |     |
              |     └── DataLoad() [DataLoader.py]
              |           |
              |           └── Dispatch table --> gerador correto
              |                                   |
              |                                   ├── NumericTypes.py
              |                                   ├── TextTypes.py
              |                                   └── DateTime.py
              |
              ├── _register_context()  --> salva dados para FK
              └── Escreve saida (SQL/CSV/JSON)
```

---

## Modulos

### cli.py

Entry point. Responsabilidades:
- Parse de argumentos com argparse
- Validacao de definicoes de tabela
- Orquestracao da geracao (ordem, contexto, saida)
- Formatacao de saida (SQL, CSV, JSON)

Exports: `main()` (entry point do pacote)

### generators/DataLoader.py

Dispatcher. Recebe um `data_type` string e roteia para a funcao geradora correta.

**Dispatch table:** Lista ordenada de tuplas `(prefixo, funcao, requer_value_dict)`. A ordem importa — tipos mais especificos vem primeiro (ex: `DateTime` antes de `Date`, pois `Date` e substring de `DateTime`).

Casos especiais tratados inline:
- `Default` — retorna valor fixo
- `ForeignKey` — chama `ForeignKey()` com context inter-tabela

### generators/NumericTypes.py

Geradores puramente numericos:
- `Serial()` — `list(range(start, start + n))`
- `Integer()` — `random.randint` em loop

### generators/TextTypes.py

Maior modulo. Contem:
- Sistema de cache de datasources
- Sistema de locale
- Index de cidades (O(1) lookup)
- Geradores de texto, documentos, enderecos
- ForeignKey

### generators/DateTime.py

Geradores de data/hora. Usa `time.mktime` + `time.strftime` com timestamps aleatorios.

### generators/Getters.py

Helpers triviais para extrair metadados de definicoes de tabela:
- `get_table_name()`
- `get_count_records_to_generate()`
- `get_count_field_list()`

---

## Sistema de cache

Datasources sao carregados do disco uma unica vez e mantidos em `_datasource_cache`:

```python
_datasource_cache: dict[str, list[str]] = {}
```

Chave: nome do arquivo relativo a `datasources/`. Valor: lista de linhas (stripped).

O cache nunca expira durante uma execucao. Se o locale muda, o index de cidades e invalidado mas os arquivos base permanecem em cache.

---

## Index de cidades

Estrutura indexada construida na primeira chamada a `City` ou `StateProvince`:

```python
_city_index = {
    'by_uf': {
        'SP': [{'state': 'SAO PAULO', 'uf': 'SP', 'city': 'CAMPINAS'}, ...],
        'RJ': [...],
    },
    'by_city': {
        'CAMPINAS': {'state': 'SAO PAULO', 'uf': 'SP', 'city': 'CAMPINAS'},
        'MANAUS': {...},
    },
    'all': [...]  # lista flat de todas as entradas
}
```

Beneficio: lookup O(1) por UF ou por nome de cidade. Elimina scans lineares repetidos.

---

## Context inter-tabela (ForeignKey)

Dict mantido durante o `populate`, passado para `_generate_values()`:

```python
context = {
    'tbl_departamentos': {
        'id': [1, 2, 3, 4, 5],
        'nome': ["'TI'", "'RH'", "'FIN'", "'MKT'", "'OPS'"],
    },
    'tbl_funcionarios': {
        'id': [1, 2, ..., 20],
        'nome': [...],
        'dept_id': [3, 1, 5, ...],
    },
}
```

Apos gerar cada tabela, `_register_context()` salva o `value_dict` indexado por campo.

---

## Dependencias entre tipos

Alguns tipos dependem de outros:

```
FullName (gerado primeiro, mesmo se implicito)
  ├── FirstName
  ├── LastName
  ├── UserName
  └── Email

City
  └── StateProvince:Find

Tabela anterior (via context)
  └── ForeignKey
```

A logica em `_generate_values()` garante que `FullName` e gerado antes de qualquer tipo dependente, independente da ordem na lista de tipos.

---

## Tratamento de erros

Hierarquia de exceptions:

```
Exception
  └── GeneratorError (generators/)
        └── DatasourceError (arquivo nao encontrado/vazio)

  └── LebreError (cli.py)
        └── TableFileError (parse/validacao de tabelas)
```

Todas as exceptions sao capturadas em `cmd_populate()` e convertidas em mensagens de erro no stderr com exit code 1.

---

## Convencoes de saida dos geradores

| Tipo de valor | Formato retornado | Exemplo |
|---------------|------------------|---------|
| String | Com aspas SQL | `"'valor'"` |
| Inteiro | Sem aspas | `42` |
| Boolean (texto) | Sem aspas | `'TRUE'` ou `TRUE` |
| Boolean (int) | Sem aspas | `1` ou `0` |
| CPF | Sem aspas SQL | `'347.891.025-60'` → formatado |

No formato JSON e CSV, aspas SQL sao removidas antes de escrever.

---

## Testes

Suite com 67 testes divididos em:

| Arquivo | Escopo | Quantidade |
|---------|--------|-----------|
| `test_generators.py` | Cada gerador individual | 34 |
| `test_cli.py` | CLI end-to-end via subprocess | 15 |
| `test_output_formats.py` | Formatos + error handling | 18 |

Testes rodam em ~1.2s.
