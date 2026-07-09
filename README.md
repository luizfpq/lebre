<img src="/assets/icon-lebre.png" alt="Lebre Icon" width="100px" align="right">

# Lebre

A Database Populator — generates random data to fill your project's database tables. No more writing queries or filling forms manually before you can start working on your application.

## Installation

```bash
git clone https://github.com/luizfpq/lebre.git
cd lebre
pip install -e .
```

After installation the `lebre` command is available globally.

For YAML table support and dev tools:

```bash
pip install -e ".[yaml]"      # YAML/TOML table definitions
pip install -e ".[dev]"       # pytest
```

## Quick start

```bash
# Define a table
lebre create-table --name tbl_users \
  --fields "id,cpf,nome,email,telefone" \
  --types "Serial,CPF,FullName,Email,Phone" \
  --records 100

# Generate SQL
lebre populate --format sql

# Print to stdout (pipe to psql, mysql, etc.)
lebre populate --stdout --format sql | psql mydb

# Generate CSV or JSON
lebre populate --format csv
lebre populate --format json --stdout

# Generate with English data
lebre populate --locale en --format json --stdout
```

## CLI reference

```
lebre create-table   Create a table definition file
lebre populate       Generate data from existing table definitions
lebre list-types     Show all available data types
```

### create-table

| Flag | Description |
|------|-------------|
| `--name` | Table name (required) |
| `--fields` | Comma-separated field names (required) |
| `--types` | Comma-separated data types (required) |
| `--records` | Number of records to generate (required) |
| `--tables-dir` | Directory to save definitions (default: `tables`) |
| `--table-format` | Output format: `json`, `yaml`, `toml` (default: `json`) |

### populate

| Flag | Description |
|------|-------------|
| `--tables-dir` | Directory with table definitions (default: `tables`) |
| `--output-dir` | Output directory (default: `results`) |
| `--format` | Output format: `sql`, `csv`, `json` (default: `sql`) |
| `--dialect` | SQL quoting style: `postgresql`, `mysql`, `sqlite` (default: `postgresql`) |
| `--locale` | Data locale: `br`, `en` (default: `br`) |
| `--stdout` | Print to terminal instead of writing a file |

## Available data types

| Type | Description | Example |
|------|-------------|---------|
| `Serial` | Auto-increment integer | `Serial` or `Serial:100` |
| `Integer:min:max` | Random integer in range | `Integer:0:10` |
| `FullName` | Full name from datasource | `FullName` |
| `FirstName` | First name (derived from FullName) | `FirstName` |
| `LastName` | Last name (derived from FullName) | `LastName` |
| `UserName` | Username from full name | `UserName` or `UserName:Num` |
| `Email` | Email from full name | `Email` |
| `InitName` | First character of previous name field | `InitName` |
| `CPF` | Valid Brazilian CPF | `CPF` |
| `CNPJ` | Valid Brazilian CNPJ | `CNPJ` |
| `Phone` | Brazilian phone number | `Phone`, `Phone:fixo`, `Phone:11` |
| `CEP` | Brazilian postal code | `CEP` or `CEP:SP` |
| `Sex` | Random sex from datasource | `Sex` |
| `Address` | Street address | `Address` or `Address:Num` |
| `City` | City name | `City` or `City:SP` |
| `StateProvince` | State/province | `StateProvince` or `StateProvince:Find` |
| `Date` | Random date | `Date` or `Date:01/01/1990:31/12/2020` |
| `DateTime` | Random date + time | `DateTime` |
| `UUID` | UUID v4 | `UUID` |
| `Boolean` | TRUE/FALSE or 1/0 | `Boolean` or `Boolean:int` |
| `Varchar:N` | Random string of length N | `Varchar:10` |
| `ForeignKey:table:field` | Reference to another table's field | `ForeignKey:tbl_deps:id` |
| `Default:value` | Fixed value for all rows | `Default:'active'` |

## Foreign keys

Define relationships between tables. The referenced table must be processed first (alphabetical file order):

```bash
# 00_departments.json — processed first
lebre create-table --name tbl_departments \
  --fields "id,name" --types "Serial:1,Varchar:15" --records 5

# 01_employees.json — references departments
lebre create-table --name tbl_employees \
  --fields "id,name,dept_id" \
  --types "Serial:1,FullName,ForeignKey:tbl_departments:id" \
  --records 50

lebre populate --format sql --stdout
```

The `dept_id` column will only contain valid IDs (1-5) from the departments table.

## Locales

```bash
lebre populate --locale br --format sql --stdout   # Brazilian data (default)
lebre populate --locale en --format sql --stdout   # English/US data
```

Locale affects: FullName, City, StateProvince, Address, Sex. Document-specific types (CPF, CNPJ, CEP, Phone) always generate Brazilian formats.

## Table definition formats

Tables can be defined in JSON, YAML or TOML:

```json
[{
    "TableName": "tbl_users",
    "FieldList": "id,nome,email",
    "DataType": "Serial,FullName,Email",
    "RecordsToGenerate": 50
}]
```

```yaml
TableName: tbl_users
FieldList: id,nome,email
DataType: Serial,FullName,Email
RecordsToGenerate: 50
```

```toml
[table]
TableName = "tbl_users"
FieldList = "id,nome,email"
DataType = "Serial,FullName,Email"
RecordsToGenerate = 50
```

## SQL dialects

```bash
lebre populate --format sql --dialect postgresql   # "table" ("col")
lebre populate --format sql --dialect mysql        # `table` (`col`)
lebre populate --format sql --dialect sqlite       # table (col)
```

## Pipeline examples

```bash
# Seed a PostgreSQL database
lebre populate --stdout --dialect postgresql | psql -d myapp

# Seed MySQL
lebre populate --stdout --dialect mysql | mysql myapp

# Generate CSV for data analysis
lebre populate --format csv --stdout > dataset.csv

# Generate JSON for API mocking
lebre populate --format json --stdout | jq '.tbl_users[:5]'

# English data for international projects
lebre populate --locale en --format json --stdout > seed.json
```

## Running tests

```bash
pip install -e ".[dev]"
pytest -v
```

## Why Lebre?

Lebres (Hares) are animals that represent fertility in several folk traditions. There is nothing more fitting to populate your database than a Lebre.

## License

GPL v3

---

<a href="https://icons8.com/icon/95136/owl">Lebre icon by Icons8</a>
