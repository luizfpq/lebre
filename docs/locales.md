# Locales

> O sistema de locales permite gerar dados em diferentes idiomas/paises.

---

## Locales disponiveis

| Locale | Descricao | Dados inclusos |
|--------|-----------|---------------|
| `br` | Brasil (padrao) | Nomes, cidades, estados, enderecos, genero brasileiros |
| `en` | English/US | Nomes, cidades, estados, enderecos, genero americanos |

---

## Uso

```bash
# Dados brasileiros (padrao)
lebre populate --locale br --format json --stdout

# Dados americanos
lebre populate --locale en --format json --stdout
```

---

## O que muda com locale

| Tipo | Locale br | Locale en |
|------|-----------|-----------|
| `FullName` | MARIA DA SILVA SANTOS | James Smith |
| `City` | MANAUS, SAO PAULO | CHICAGO, LOS ANGELES |
| `City:SP` | Cidades de Sao Paulo | — |
| `City:CA` | — | Cidades da California |
| `StateProvince` | MINAS GERAIS,MG | CALIFORNIA,CA |
| `Address` | RUA Santos, 127 | BOULEVARD Hill, 42 |
| `Sex` | MASCULINO/FEMININO | MALE/FEMALE |

---

## O que NAO muda com locale

Tipos especificos do Brasil permanecem inalterados:

- `CPF` — sempre formato brasileiro
- `CNPJ` — sempre formato brasileiro
- `Phone` — sempre formato brasileiro (DDD)
- `CEP` — sempre faixas brasileiras

Tipos genericos tambem nao sao afetados:

- `Serial`, `Integer`, `UUID`, `Boolean`, `Varchar`, `Date`, `DateTime`, `Default`, `ForeignKey`

---

## Estrutura dos datasources

```
datasources/
  FullNameBR.txt           # locale br (padrao)
  CityBR.txt
  StateProvinceBR.txt
  AddressTypeBR.txt
  Sex.txt
  en/                      # locale en
    FullNameEN.txt
    CityEN.txt
    StateProvinceEN.txt
    AddressTypeEN.txt
    Sex.txt
```

---

## Formato dos arquivos de datasource

### FullName (um nome por linha)

```
James Smith
Mary Johnson
Robert Williams
```

### City (formato: ESTADO,SIGLA,CIDADE)

```
CALIFORNIA,CA,LOS ANGELES
CALIFORNIA,CA,SAN FRANCISCO
TEXAS,TX,HOUSTON
```

### StateProvince (formato: ESTADO,SIGLA)

```
CALIFORNIA,CA
TEXAS,TX
NEW YORK,NY
```

### AddressType (um tipo por linha)

```
STREET
AVENUE
BOULEVARD
```

### Sex (um valor por linha)

```
MALE
FEMALE
```

---

## Adicionando um novo locale

Para adicionar, por exemplo, locale `es` (espanhol):

1. Criar diretorio `datasources/es/`

2. Criar os arquivos obrigatorios:
   - `datasources/es/FullNameES.txt`
   - `datasources/es/CityES.txt`
   - `datasources/es/StateProvinceES.txt`
   - `datasources/es/AddressTypeES.txt`
   - `datasources/es/Sex.txt`

3. Registrar no mapeamento em `generators/TextTypes.py`:

```python
_LOCALE_FILES: dict[str, dict[str, str]] = {
    'br': { ... },
    'en': { ... },
    'es': {
        'FullName': 'es/FullNameES.txt',
        'City': 'es/CityES.txt',
        'StateProvince': 'es/StateProvinceES.txt',
        'AddressType': 'es/AddressTypeES.txt',
        'Sex': 'es/Sex.txt',
    },
}
```

4. Adicionar a opcao no argparse em `cli.py`:

```python
pop.add_argument('--locale', choices=['br', 'en', 'es'], default='br', ...)
```

5. Rodar os testes para garantir que nao quebrou nada.

---

## Notas tecnicas

- O cache de datasources e compartilhado entre locales (cada arquivo e cacheado pelo path)
- Ao trocar de locale, o index de cidades e invalidado e reconstruido
- O locale e definido uma vez antes de processar as tabelas — nao pode mudar no meio
