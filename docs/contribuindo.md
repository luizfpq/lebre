# Contribuindo

> Guia para adicionar novos tipos de dados, locales e datasources ao Lebre.

---

## Setup do ambiente

```bash
git clone https://github.com/luizfpq/lebre.git
cd lebre
uv venv && source .venv/bin/activate
uv pip install -e ".[yaml,dev]"
pytest -v  # confirma que tudo funciona
```

---

## Adicionando um novo tipo de dado

### 1. Escolher o modulo

| Tipo | Modulo |
|------|--------|
| Numerico puro | `generators/NumericTypes.py` |
| Texto, documentos, localizacao | `generators/TextTypes.py` |
| Data/hora | `generators/DateTime.py` |

### 2. Implementar a funcao

Assinatura padrao para tipos independentes:

```python
def MeuTipo(records_to_generate: int, data_type: str) -> list:
    """Descricao do tipo."""
    _validate_records(records_to_generate)
    # ... logica ...
    return [valor for _ in range(records_to_generate)]
```

Assinatura para tipos dependentes (que precisam de campos anteriores):

```python
def MeuTipo(records_to_generate: int, data_type: str, value_dict: list) -> list:
    """Descricao do tipo."""
    _validate_records(records_to_generate)
    # value_dict contem os campos ja gerados
    return [...]
```

### 3. Registrar no dispatch table

Em `generators/DataLoader.py`, adicionar a entrada na `_DISPATCH_ORDER`:

```python
_DISPATCH_ORDER: list[tuple[str, callable, bool]] = [
    ...
    ('MeuTipo', MeuTipo, False),  # (prefixo, funcao, requer_value_dict)
    ...
]
```

Cuidado com a ordem — tipos mais especificos devem vir antes de substrings (ex: `DateTime` antes de `Date`).

### 4. Adicionar ao import

Em `generators/DataLoader.py`:

```python
from generators.TextTypes import (
    ..., MeuTipo,
)
```

E no `__all__` de `TextTypes.py`:

```python
__all__ = [..., "MeuTipo"]
```

### 5. Documentar no CLI

Em `cli.py`, adicionar a `AVAILABLE_TYPES`:

```python
AVAILABLE_TYPES = [
    ...,
    "MeuTipo[:parametro]",
]
```

### 6. Escrever testes

Em `tests/test_generators.py`:

```python
class TestMeuTipo:
    def test_formato(self):
        result = MeuTipo(10, 'MeuTipo')
        assert len(result) == 10
        # validar formato

    def test_parametro(self):
        result = MeuTipo(5, 'MeuTipo:param')
        # validar parametro
```

### 7. Rodar testes

```bash
pytest -v
```

---

## Adicionando um novo locale

Ver detalhes completos em [locales.md](locales.md).

Resumo:

1. Criar `datasources/<locale>/` com os 5 arquivos obrigatorios
2. Registrar em `_LOCALE_FILES` no `TextTypes.py`
3. Adicionar choice no argparse em `cli.py`
4. Testar: `lebre populate --locale <novo> --stdout`

---

## Adicionando novos datasources

### Formato de nomes (FullName)

Um nome completo por linha, uppercase:

```
NOME SOBRENOME
NOME MEIO SOBRENOME
```

### Formato de cidades (City)

CSV sem header: `ESTADO,SIGLA,CIDADE`

```
SAO PAULO,SP,CAMPINAS
SAO PAULO,SP,SANTOS
RIO DE JANEIRO,RJ,NITEROI
```

### Formato de estados (StateProvince)

CSV sem header: `ESTADO,SIGLA`

```
SAO PAULO,SP
RIO DE JANEIRO,RJ
```

### Formato de enderecos (AddressType)

Um tipo por linha, uppercase:

```
RUA
AVENIDA
TRAVESSA
```

---

## Convencoes de codigo

- Type hints em todas as funcoes publicas
- Docstrings com descricao + "Uso:" para tipos com parametros
- Exceptions claras com `GeneratorError` (nunca levantar `ValueError` ou `KeyError` diretamente)
- Validacao de records com `_validate_records()` no inicio de cada gerador
- Valores string retornados com aspas SQL: `f"'{valor}'"`
- Valores numericos retornados sem aspas: `42`, `0`

---

## Workflow de PR

1. Criar branch a partir de `master`: `git checkout -b feat/meu-tipo`
2. Implementar + testar
3. Rodar `pytest -v` — todos os testes devem passar
4. Commit com mensagem padrao: `feat: descricao curta (#issue)`
5. Push e abrir PR contra `master`
6. CI roda automaticamente (Python 3.11/3.12/3.13)

---

## Estrutura de commits

```
feat: nova funcionalidade (#N)
fix: correcao de bug (#N)
refactor: refatoracao sem mudanca funcional
docs: documentacao
chore: manutenção (deps, CI, limpeza)
test: adicao/ajuste de testes
```
