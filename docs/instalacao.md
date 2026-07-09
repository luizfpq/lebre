# Instalacao

> **Requisito minimo:** Python 3.11+

---

## Instalacao padrao

```bash
git clone https://github.com/luizfpq/lebre.git
cd lebre
pip install -e .
```

Apos a instalacao, o comando `lebre` fica disponivel globalmente no terminal.

## Dependencias opcionais

### YAML/TOML como formato de tabela

TOML e suportado nativamente (Python 3.11+ inclui `tomllib`). Para YAML:

```bash
pip install -e ".[yaml]"
```

### Ambiente de desenvolvimento (testes)

```bash
pip install -e ".[dev]"
```

Instala `pytest` para rodar a suite de testes.

### Tudo junto

```bash
pip install -e ".[yaml,dev]"
```

## Instalacao com uv (alternativa)

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[yaml,dev]"
```

## Verificacao

```bash
lebre --version
# lebre 2.2.0

lebre list-types
# Mostra todos os tipos de dados disponiveis
```

## Rodando testes

```bash
pytest -v
```

Resultado esperado: 67 testes passando.

## Estrutura de diretorios de trabalho

O Lebre usa dois diretorios em tempo de execucao:

| Diretorio | Proposito | Criado automaticamente |
|-----------|-----------|----------------------|
| `tables/` | Definicoes de tabela (JSON/YAML/TOML) | Sim |
| `results/` | Arquivos de saida gerados | Sim |

Ambos sao relativos ao diretorio de trabalho atual. Podem ser customizados via `--tables-dir` e `--output-dir`.

## Desinstalacao

```bash
pip uninstall lebre
```
