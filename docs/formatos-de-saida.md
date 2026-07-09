# Formatos de Saida

> O Lebre suporta tres formatos de saida: SQL, CSV e JSON.

---

## SQL

Formato padrao. Gera statements `INSERT INTO ... VALUES` em batch.

### Dialetos

| Dialeto | Quoting | Exemplo |
|---------|---------|---------|
| `postgresql` (default) | Aspas duplas | `"tbl_users" ("id", "nome")` |
| `mysql` | Backticks | `` `tbl_users` (`id`, `nome`) `` |
| `sqlite` | Sem quoting | `tbl_users (id, nome)` |

### Estrutura da saida

```sql
INSERT INTO
    "tbl_users" ("id", "nome", "email", "ativo")
VALUES
    (0, 'MARIA SILVA', 'maria.silva@example.com', TRUE),
    (1, 'JOAO SANTOS', 'joao.santos@example.com', FALSE),
    (2, 'ANA OLIVEIRA', 'ana.oliveira@example.com', TRUE);
```

Caracteristicas:
- Uma statement por tabela (INSERT unico com multiplas tuplas)
- Virgulas separando tuplas, ponto-e-virgula no final
- Strings com aspas simples, numeros e booleanos sem aspas
- Tabelas processadas em ordem — saida sequencial

### Uso em pipeline

```bash
# PostgreSQL
lebre populate --stdout --dialect postgresql | psql -d mydb

# MySQL
lebre populate --stdout --dialect mysql | mysql mydb

# SQLite
lebre populate --stdout --dialect sqlite | sqlite3 mydb.sqlite
```

### Multiplas tabelas

Quando ha multiplas tabelas, cada uma gera um INSERT separado na saida:

```sql
INSERT INTO
    "tbl_departamentos" ("id", "nome")
VALUES
    (1, 'TI'),
    (2, 'RH');
INSERT INTO
    "tbl_funcionarios" ("id", "nome", "dept_id")
VALUES
    (1, 'Maria', 2),
    (2, 'Joao', 1);
```

---

## CSV

Gera arquivo CSV (sem delimitador customizado — sempre virgula).

### Estrutura

```
id,nome,email,ativo
0,MARIA SILVA,maria.silva@example.com,TRUE
1,JOAO SANTOS,joao.santos@example.com,FALSE
2,ANA OLIVEIRA,ana.oliveira@example.com,TRUE
```

Caracteristicas:
- Header com nomes dos campos
- Aspas SQL removidas dos valores (strings limpas)
- Uma linha em branco entre tabelas diferentes
- Sem delimitador customizavel (sempre `,`)

### Multiplas tabelas

```
id,nome
1,TI
2,RH

id,nome,dept_id
1,MARIA SILVA,2
2,JOAO SANTOS,1

```

Cada tabela gera um bloco com header + dados + linha em branco.

### Uso

```bash
lebre populate --format csv --stdout > dados.csv
lebre populate --format csv --output-dir ./seeds
```

---

## JSON

Gera JSON estruturado com array de objetos por tabela.

### Estrutura

```json
{
  "tbl_departamentos": [
    {
      "id": 1,
      "nome": "TI"
    },
    {
      "id": 2,
      "nome": "RH"
    }
  ],
  "tbl_funcionarios": [
    {
      "id": 1,
      "nome": "MARIA SILVA",
      "dept_id": 2
    }
  ]
}
```

Caracteristicas:
- Objeto raiz com chave = nome da tabela
- Cada tabela contem array de objetos
- Aspas SQL removidas (strings limpas)
- Tipos preservados: inteiros como `int`, strings como `string`
- Indentacao com 2 espacos
- Encoding UTF-8 com `ensure_ascii=False`

### Uso

```bash
# Stdout
lebre populate --format json --stdout

# Para arquivo
lebre populate --format json --output-dir ./seeds

# Filtrar com jq
lebre populate --format json --stdout | jq '.tbl_users[:5]'

# Pretty print de uma tabela
lebre populate --format json --stdout | jq '.tbl_funcionarios'
```

---

## Saida para arquivo vs stdout

| Flag | Comportamento |
|------|--------------|
| Sem `--stdout` | Salva em `results/NN_saida.ext` (auto-incremento) |
| Com `--stdout` | Imprime no terminal (nao cria arquivo) |

Quando salva em arquivo:
- O diretorio e criado automaticamente se nao existir
- Nomeacao: `00_saida.sql`, `01_saida.sql`, `02_saida.sql`, ...
- Mensagem de confirmacao vai para stdout: `Arquivo gerado: 'results/00_saida.sql'.`

Quando usa `--stdout`:
- Dados vao para stdout (pipe-friendly)
- Erros vao para stderr
- Nenhum arquivo e criado
