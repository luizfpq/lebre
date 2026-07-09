# Tipos de Dados

> Referencia completa de cada tipo suportado pelo Lebre.

---

## Tipos numericos

### Serial

Gera sequencia auto-incremento (inteiros consecutivos).

| Sintaxe | Resultado |
|---------|-----------|
| `Serial` | 0, 1, 2, 3, ... |
| `Serial:100` | 100, 101, 102, ... |
| `Serial:1` | 1, 2, 3, ... |

O valor apos `:` define o inicio da sequencia.

**Formato de saida:** inteiro sem aspas (ex: `1`, `42`).

---

### Integer

Gera inteiros aleatorios dentro de um intervalo fechado [min, max].

| Sintaxe | Resultado |
|---------|-----------|
| `Integer:0:10` | Inteiros entre 0 e 10 |
| `Integer:1:100` | Inteiros entre 1 e 100 |
| `Integer:5:5` | Sempre 5 |

**Formato:** `Integer:min:max` — ambos obrigatorios.

**Formato de saida:** inteiro sem aspas.

**Erro se:** min > max, formato incorreto, valores nao-numericos.

---

## Tipos de nome

Esses tipos trabalham em conjunto. `FullName` deve ser definido (explicita ou implicitamente) antes de `FirstName`, `LastName`, `UserName` ou `Email`.

Se voce usa `FirstName` sem ter `FullName` na lista de tipos, o Lebre gera internamente um `FullName` oculto para derivar os outros campos. Porem, o nome completo nao aparecera na saida.

### FullName

Nome completo aleatorio do datasource (ex: `MARIA DA SILVA SANTOS`).

| Sintaxe | Descricao |
|---------|-----------|
| `FullName` | Nome completo |

**Fonte:** `datasources/FullNameBR.txt` (locale br) ou `datasources/en/FullNameEN.txt` (locale en).

**Formato de saida:** string com aspas SQL (ex: `'MARIA DA SILVA'`).

---

### FirstName

Primeiro nome extraido do `FullName` correspondente na mesma linha.

| Sintaxe | Exemplo de saida |
|---------|-----------------|
| `FirstName` | `'MARIA'` |

**Dependencia:** Requer `FullName` na mesma tabela (explicito ou implicito).

**Logica:** Pega a primeira palavra do nome completo.

---

### LastName

Sobrenome (ultima palavra) extraido do `FullName` correspondente.

| Sintaxe | Exemplo de saida |
|---------|-----------------|
| `LastName` | `'SANTOS'` |

**Logica:** Pega a ultima palavra do nome completo.

---

### UserName

Username derivado do nome completo: inicial do primeiro nome + sobrenome, tudo minusculo.

| Sintaxe | Exemplo de saida |
|---------|-----------------|
| `UserName` | `'msilva'` |
| `UserName:Num` | `'msilva042871'` |

A variante `:Num` adiciona 6 digitos aleatorios ao final.

---

### Email

Email derivado do nome completo: `nome.sobrenome@example.com`.

| Sintaxe | Exemplo de saida |
|---------|-----------------|
| `Email` | `'maria.santos@example.com'` |

**Logica:** primeiro_nome.ultimo_nome@example.com, tudo minusculo.

---

### InitName

Primeiro caractere do ultimo campo gerado antes dele na lista.

| Sintaxe | Descricao |
|---------|-----------|
| `InitName` | Inicial do campo anterior |

Uso tipico: gerar uma inicial de nome para campos tipo "nome_meio_inicial".

---

## Documentos brasileiros

### CPF

Gera CPFs validos com digitos verificadores corretos.

| Sintaxe | Formato | Exemplo |
|---------|---------|---------|
| `CPF` | XXX.XXX.XXX-XX | `347.891.025-60` |

**Algoritmo:** Gera 9 digitos aleatorios, calcula os 2 digitos verificadores usando pesos 10-2 e 11-2 (modulo 11). CPFs gerados passam em qualquer validador.

**Formato de saida:** string sem aspas SQL (ex: `347.891.025-60`).

---

### CNPJ

Gera CNPJs validos com digitos verificadores corretos.

| Sintaxe | Formato | Exemplo |
|---------|---------|---------|
| `CNPJ` | XX.XXX.XXX/0001-XX | `'12.345.678/0001-95'` |

**Algoritmo:** Gera 8 digitos aleatorios + sufixo fixo 0001, calcula os 2 digitos verificadores usando pesos 5-4-3-2-9-8-7-6-5-4-3-2 e 6-5-4-3-2-9-8-7-6-5-4-3-2.

**Formato de saida:** string com aspas SQL.

---

### Phone

Gera numeros de telefone brasileiros.

| Sintaxe | Formato | Exemplo |
|---------|---------|---------|
| `Phone` | (XX) 9XXXX-XXXX | `'(11) 98765-4321'` |
| `Phone:fixo` | (XX) XXXX-XXXX | `'(21) 3456-7890'` |
| `Phone:11` | (11) 9XXXX-XXXX | `'(11) 91234-5678'` |

- Sem parametro: celular com DDD aleatorio (11-99)
- `:fixo`: telefone fixo com DDD aleatorio
- `:DDD`: celular com DDD especifico

---

### CEP

Gera CEPs brasileiros aleatorios.

| Sintaxe | Formato | Exemplo |
|---------|---------|---------|
| `CEP` | XXXXX-XXX | `'01310-100'` |
| `CEP:SP` | XXXXX-XXX (faixa SP) | `'04532-070'` |

UFs suportadas: AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO.

Cada UF tem uma faixa de prefixo definida (ex: SP = 01000-19999, RJ = 20000-28999).

---

## Endereco e localizacao

### Address

Gera enderecos ficticios combinando tipo de logradouro + palavras de nomes.

| Sintaxe | Exemplo |
|---------|---------|
| `Address` | `'RUA Santos'` |
| `Address:Num` | `'RUA Santos, 127'` |

A variante `:Num` adiciona numero aleatorio (0-999).

**Fonte:** `AddressTypeBR.txt` (ou `en/AddressTypeEN.txt`) + `FullNameBR.txt`.

---

### City

Gera nome de cidade a partir do datasource.

| Sintaxe | Descricao |
|---------|-----------|
| `City` | Cidade aleatoria de qualquer estado |
| `City:SP` | Cidade aleatoria de Sao Paulo |
| `City:CA` | Cidade aleatoria da California (locale en) |

O parametro apos `:` e a sigla do estado/UF.

**Performance:** Index pre-computado com lookup O(1) por UF.

---

### StateProvince

Gera estado/provincia.

| Sintaxe | Descricao |
|---------|-----------|
| `StateProvince` | Estado aleatorio (nome completo) |
| `StateProvince:SP` | Filtra por UF (retorna nome do estado) |
| `StateProvince:Find` | Busca estado compativel com a cidade anterior |

A variante `:Find` requer que `City` tenha sido gerado antes na mesma tabela. Usa o index para encontrar o estado correto da cidade gerada.

---

## Tipos de data/hora

### Date

Gera datas aleatorias no formato dd/mm/yyyy.

| Sintaxe | Descricao |
|---------|-----------|
| `Date` | Entre 01/01/1970 e 01/01/2000 |
| `Date:01/01/2020:31/12/2024` | Intervalo customizado |

**Formato do intervalo:** `Date:dd/mm/yyyy:dd/mm/yyyy`

---

### DateTime

Gera datas com hora no formato dd/mm/yyyy HH:MM AM/PM.

| Sintaxe | Descricao |
|---------|-----------|
| `DateTime` | Entre 01/01/1970 e 01/01/2000 |

Intervalo fixo. Formato de saida: `'15/03/1985 02:30 PM'`.

---

## Tipos genericos

### UUID

Gera UUIDs v4 aleatorios (128 bits, formato padrao).

| Sintaxe | Exemplo |
|---------|---------|
| `UUID` | `'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d'` |

Garantia de unicidade por geracao (colisao estatisticamente impossivel).

---

### Boolean

Gera valores booleanos aleatorios.

| Sintaxe | Valores possiveis |
|---------|------------------|
| `Boolean` | `TRUE` ou `FALSE` |
| `Boolean:int` | `1` ou `0` |
| `Boolean:bit` | `1` ou `0` |

---

### Varchar

Gera string aleatoria de comprimento fixo (apenas letras ASCII).

| Sintaxe | Exemplo |
|---------|---------|
| `Varchar:5` | `'aBcDe'` |
| `Varchar:20` | `'xYzAbCdEfGhIjKlMnOpQ'` |

O numero apos `:` define o comprimento exato.

**Erro se:** formato invalido, comprimento <= 0.

---

### Default

Valor fixo para todos os registros.

| Sintaxe | Resultado |
|---------|-----------|
| `Default:'ativo'` | `'ativo'` em todas as linhas |
| `Default:0` | `0` em todas as linhas |
| `Default:NULL` | `NULL` em todas as linhas |

O valor apos `:` e usado literalmente.

---

### Sex

Valor aleatorio de sexo/genero do datasource.

| Sintaxe | Valores (br) | Valores (en) |
|---------|-------------|-------------|
| `Sex` | `MASCULINO`, `FEMININO` | `MALE`, `FEMALE` |

---

### ForeignKey

Referencia a coluna de outra tabela. Ver [documentacao dedicada](foreign-keys.md).

| Sintaxe | Descricao |
|---------|-----------|
| `ForeignKey:tbl_deps:id` | Valor aleatorio da coluna `id` de `tbl_deps` |
