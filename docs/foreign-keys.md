# Chaves Estrangeiras (ForeignKey)

> Permite que uma coluna referencie valores gerados em outra tabela, garantindo integridade referencial.

---

## Sintaxe

```
ForeignKey:nome_da_tabela:nome_do_campo
```

Exemplos:
- `ForeignKey:tbl_departamentos:id`
- `ForeignKey:tbl_categorias:codigo`
- `ForeignKey:tbl_users:id`

---

## Como funciona

1. O Lebre processa tabelas em ordem alfabetica de arquivo
2. Apos gerar cada tabela, armazena todos os valores num contexto interno
3. Quando encontra `ForeignKey:X:Y`, busca os valores da coluna `Y` da tabela `X` no contexto
4. Seleciona aleatoriamente entre os valores disponiveis

Isso garante que a coluna FK contera apenas valores validos da tabela referenciada.

---

## Regra de ordenacao

A tabela referenciada **deve ser processada antes** da tabela que a referencia. Como o processamento segue ordem alfabetica dos nomes de arquivo, use prefixos numericos:

```
tables/
  00_tbl_departamentos.json    <-- processada primeiro
  01_tbl_funcionarios.json     <-- pode referenciar tbl_departamentos
  02_tbl_projetos.json         <-- pode referenciar ambas
```

---

## Exemplo completo

### Passo 1: criar tabela referenciada

```bash
lebre create-table --name tbl_departamentos \
  --fields "id,nome,sigla" \
  --types "Serial:1,Varchar:15,Varchar:3" \
  --records 5
```

Gera `tables/00_tbl_departamentos.json`.

### Passo 2: criar tabela com FK

```bash
lebre create-table --name tbl_funcionarios \
  --fields "id,nome,email,salario,dept_id" \
  --types "Serial:1,FullName,Email,Integer:3000:15000,ForeignKey:tbl_departamentos:id" \
  --records 20
```

Gera `tables/01_tbl_funcionarios.json`.

### Passo 3: gerar dados

```bash
lebre populate --format sql --stdout
```

Saida:

```sql
INSERT INTO
    "tbl_departamentos" ("id", "nome", "sigla")
VALUES
    (1, 'ABcDeFgHiJkLmNo', 'XyZ'),
    (2, 'PqRsTuVwXyZaBcD', 'AbC'),
    (3, 'EfGhIjKlMnOpQrS', 'DeF'),
    (4, 'TuVwXyZaBcDeFgH', 'GhI'),
    (5, 'IjKlMnOpQrStUvW', 'JkL');
INSERT INTO
    "tbl_funcionarios" ("id", "nome", "email", "salario", "dept_id")
VALUES
    (1, 'MARIA DA SILVA', 'maria.silva@example.com', 7832, 3),
    (2, 'JOAO SANTOS', 'joao.santos@example.com', 12450, 1),
    ...
```

Note que `dept_id` contem apenas valores 1-5 (IDs validos dos departamentos).

---

## Multiplas FKs na mesma tabela

```bash
lebre create-table --name tbl_matriculas \
  --fields "id,aluno_id,curso_id,data" \
  --types "Serial:1,ForeignKey:tbl_alunos:id,ForeignKey:tbl_cursos:id,Date:01/01/2024:30/06/2024" \
  --records 100
```

---

## FK referenciando campos nao-Serial

ForeignKey funciona com qualquer tipo de campo, nao apenas Serial:

```bash
# Tabela de categorias com UUID como PK
lebre create-table --name tbl_categorias \
  --fields "uuid,nome" \
  --types "UUID,Varchar:10" \
  --records 8

# Produtos referenciando UUID
lebre create-table --name tbl_produtos \
  --fields "id,nome,categoria_uuid" \
  --types "Serial:1,Varchar:20,ForeignKey:tbl_categorias:uuid" \
  --records 50
```

---

## Tratamento de erros

| Situacao | Mensagem |
|----------|----------|
| Tabela referenciada nao existe | `ForeignKey: tabela 'X' nao encontrada no contexto` |
| Campo referenciado nao existe | `ForeignKey: campo 'Y' nao encontrado na tabela 'X'` |
| Formato invalido | `Formato invalido para ForeignKey: esperado ForeignKey:tabela:campo` |
| Tabela processada depois | `Tabelas disponiveis: ...` (lista o que ja foi processado) |

---

## Limitacoes

- Nao suporta FK circular (tabela A referencia B que referencia A)
- A ordem e determinada pelo nome do arquivo, nao por analise de dependencias
- Todos os valores da coluna referenciada sao tratados como pool uniforme (sem pesos)
