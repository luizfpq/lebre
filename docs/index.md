# Documentacao do Lebre

> **Versao:** 2.2.0
> **Autor:** Luiz Fernando P. Quirino
> **Licenca:** GPL v3

---

Lebre e um gerador de dados ficticios para popular bancos de dados. Produz SQL, CSV ou JSON a partir de definicoes de tabela, com suporte a dados brasileiros e americanos, chaves estrangeiras e multiplos dialetos SQL.

## Indice

1. [Instalacao](instalacao.md) — Requisitos, instalacao, dependencias opcionais
2. [Referencia do CLI](cli.md) — Comandos, flags e exemplos de uso
3. [Tipos de Dados](tipos-de-dados.md) — Referencia completa de cada tipo com sintaxe e exemplos
4. [Chaves Estrangeiras](foreign-keys.md) — Relacionamentos entre tabelas
5. [Locales](locales.md) — Sistema de internacionalizacao (br, en)
6. [Formatos de Saida](formatos-de-saida.md) — SQL, CSV, JSON com exemplos detalhados
7. [Arquitetura Interna](arquitetura.md) — Como o codigo funciona (para contribuidores)
8. [Normalizer](normalizer.md) — Utilitario de normalizacao de datasources
9. [Contribuindo](contribuindo.md) — Como adicionar tipos, locales, datasources

---

## Inicio rapido

```bash
git clone https://github.com/luizfpq/lebre.git
cd lebre
pip install -e .

lebre create-table --name tbl_users \
  --fields "id,cpf,nome,email" \
  --types "Serial,CPF,FullName,Email" \
  --records 100

lebre populate --format sql --stdout | psql mydb
```

## Estrutura do projeto

```
lebre/
  cli.py                  # Entry point — interface de linha de comando
  generators/
    DataLoader.py         # Dispatcher (roteia tipo -> gerador)
    NumericTypes.py       # Serial, Integer
    TextTypes.py          # Nomes, documentos, enderecos, FK, UUID, Boolean
    DateTime.py           # Date, DateTime
    Getters.py            # Helpers para extrair metadados das tabelas
  datasources/
    FullNameBR.txt        # Nomes brasileiros
    CityBR.txt            # Cidades (ESTADO,UF,CIDADE)
    StateProvinceBR.txt   # Estados brasileiros
    AddressTypeBR.txt     # Tipos de logradouro
    Sex.txt               # Genero
    normalizer.py         # Utilitario de normalizacao
    en/                   # Datasources em ingles
      FullNameEN.txt
      CityEN.txt
      StateProvinceEN.txt
      AddressTypeEN.txt
      Sex.txt
  tests/
    test_generators.py    # Testes unitarios dos geradores
    test_cli.py           # Testes end-to-end do CLI
    test_output_formats.py # Testes de formato de saida
  docs/                   # Esta documentacao
```
