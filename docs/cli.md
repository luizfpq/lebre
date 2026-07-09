# Referencia do CLI

> Todos os comandos sao acessados via `lebre <comando> [opcoes]`.

---

## Visao geral

```
lebre --version              Mostra a versao
lebre --help                 Ajuda geral
lebre create-table           Cria definicao de tabela
lebre populate               Gera dados a partir das definicoes
lebre list-types             Lista tipos de dados disponiveis
```

---

## create-table

Cria um arquivo de definicao de tabela no formato especificado.

### Sintaxe

```bash
lebre create-table --name <nome> --fields <campos> --types <tipos> --records <n> \
  [--tables-dir <dir>] [--table-format <formato>]
```

### Flags

| Flag | Obrigatoria | Descricao |
|------|:-----------:|-----------|
| `--name` | Sim | Nome da tabela (ex: `tbl_users`) |
| `--fields` | Sim | Campos separados por virgula (ex: `id,nome,email`) |
| `--types` | Sim | Tipos separados por virgula (ex: `Serial,FullName,Email`) |
| `--records` | Sim | Numero de registros a gerar (inteiro > 0) |
| `--tables-dir` | Nao | Diretorio destino (default: `tables`) |
| `--table-format` | Nao | Formato: `json`, `yaml`, `toml` (default: `json`) |

### Validacoes

- Numero de campos deve ser igual ao numero de tipos. Se divergir, erro com exit code 1.
- `--records` deve ser inteiro positivo.

### Exemplos

```bash
# Tabela basica em JSON
lebre create-table --name tbl_alunos \
  --fields "id,cpf,nome,email" \
  --types "Serial,CPF,FullName,Email" \
  --records 200

# Tabela em TOML
lebre create-table --name tbl_produtos \
  --fields "id,codigo,preco,ativo" \
  --types "Serial:1,UUID,Integer:10:500,Boolean" \
  --records 50 \
  --table-format toml

# Diretorio customizado
lebre create-table --name tbl_log \
  --fields "id,timestamp,msg" \
  --types "Serial,DateTime,Varchar:50" \
  --records 1000 \
  --tables-dir ./seeds
```

### Nomeacao dos arquivos

Arquivos sao nomeados sequencialmente: `00_nome.json`, `01_nome.json`, etc. Isso garante ordem previsivel de processamento (importante para ForeignKey).

---

## populate

Gera dados a partir de todas as definicoes de tabela encontradas no diretorio.

### Sintaxe

```bash
lebre populate [--tables-dir <dir>] [--output-dir <dir>] [--format <fmt>] \
  [--dialect <sql>] [--locale <lc>] [--stdout]
```

### Flags

| Flag | Default | Descricao |
|------|---------|-----------|
| `--tables-dir` | `tables` | Diretorio com definicoes |
| `--output-dir` | `results` | Diretorio de saida |
| `--format` | `sql` | Formato: `sql`, `csv`, `json` |
| `--dialect` | `postgresql` | Dialeto SQL: `postgresql`, `mysql`, `sqlite` |
| `--locale` | `br` | Locale: `br`, `en` |
| `--stdout` | — | Imprime no terminal (nao salva arquivo) |

### Comportamento

1. Busca todos os arquivos `.json`, `.yaml`, `.yml`, `.toml` no `--tables-dir`
2. Ordena alfabeticamente (garante ordem para ForeignKey)
3. Para cada tabela: gera valores, registra no contexto inter-tabela
4. Escreve no formato escolhido

### Exemplos

```bash
# SQL para PostgreSQL (padrao)
lebre populate --stdout

# MySQL com dados em ingles
lebre populate --format sql --dialect mysql --locale en --stdout

# JSON para arquivo
lebre populate --format json --output-dir ./seeds

# CSV direto para stdout
lebre populate --format csv --stdout > data.csv

# Pipeline para banco
lebre populate --stdout --dialect postgresql | psql -d myapp
lebre populate --stdout --dialect mysql | mysql myapp
```

### Exit codes

| Codigo | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Erro (diretorio inexistente, tipo invalido, formato incorreto) |

Mensagens de erro vao para stderr; dados vao para stdout.

---

## list-types

Lista todos os tipos de dados disponiveis com sintaxe.

```bash
lebre list-types
```

Saida:

```
Tipos de dados disponiveis:

  - Serial[:start]
  - Integer:min:max
  - FullName
  - FirstName
  - LastName
  - UserName[:Num]
  - Email
  - InitName
  - CPF
  - CNPJ
  - Phone[:fixo|DDD]
  - CEP[:UF]
  - Sex
  - Varchar:size
  - Address[:Num]
  - City[:UF]
  - StateProvince[:Find|UF]
  - Date[:dd/mm/yyyy:dd/mm/yyyy]
  - DateTime
  - UUID
  - Boolean[:int|bit]
  - ForeignKey:table:field
  - Default:value
```
