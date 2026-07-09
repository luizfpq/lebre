# Normalizer

> Utilitario para processar e normalizar os arquivos `.txt` de datasource.

---

## O que faz

O `normalizer.py` aplica transformacoes de case em todos os arquivos `.txt` do diretorio de datasources. Suporta tres acoes:

| Acao | Descricao | Exemplo |
|------|-----------|---------|
| `uppercase` | Todas as letras maiusculas | `maria da silva` → `MARIA DA SILVA` |
| `lowercase` | Todas as letras minusculas | `MARIA DA SILVA` → `maria da silva` |
| `capitalize` | Title Case inteligente (PT-BR) | `MARIA DA SILVA` → `Maria da Silva` |

---

## Uso

```bash
cd datasources/
python normalizer.py uppercase
python normalizer.py lowercase
python normalizer.py capitalize
```

Processa todos os `.txt` no diretorio atual. Alteracoes sao feitas in-place (sobrescreve os arquivos).

---

## Capitalize inteligente

A acao `capitalize` e mais complexa que um simples `.title()`. Implementa regras especificas para PT-BR:

### Preposicoes e artigos (ficam minusculos)

```
de, da, do, das, dos, e, em, no, na, nos, nas, por, para, com, sem
```

Excecao: ficam maiusculos se forem a primeira palavra da linha.

### Siglas (ficam maiusculas)

```
AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI,
RJ, RN, RS, RO, RR, SC, SP, SE, TO, BR, II, III, IV, VI, VII, VIII, IX, X
```

### Apostrofos (tratamento especial)

```
D'AGUA → d'Agua
D'OESTE → d'Oeste
```

### Formato CSV preservado

Linhas com virgula (como `CityBR.txt`) sao tratadas campo a campo:

```
MINAS GERAIS,MG,BELO HORIZONTE → Minas Gerais,MG,Belo Horizonte
```

A sigla `MG` permanece maiuscula por ser reconhecida como UF.

---

## Exemplos de transformacao

| Entrada | Saida (capitalize) |
|---------|-------------------|
| `MARIA DA SILVA` | `Maria da Silva` |
| `SAO PAULO,SP,CAMPINAS` | `Sao Paulo,SP,Campinas` |
| `RIO DE JANEIRO,RJ,NITEROI` | `Rio de Janeiro,RJ,Niteroi` |
| `OLHO D'AGUA DO CASADO` | `Olho d'Agua do Casado` |
| `MATO GROSSO DO SUL,MS` | `Mato Grosso do Sul,MS` |
| `RUA` | `Rua` |

---

## Quando usar

- Apos adicionar novos datasources em UPPERCASE e quiser normalizar para Title Case
- Para preparar datasources de fontes externas (IBGE, Correios)
- Para alternar entre formatos conforme necessidade do projeto

---

## Funcoes exportadas (para uso programatico)

```python
from datasources.normalizer import capitalize_line, capitalize_word

capitalize_line("MINAS GERAIS,MG,BELO HORIZONTE")
# → "Minas Gerais,MG,Belo Horizonte"

capitalize_word("SILVA", is_first=False)
# → "Silva"

capitalize_word("de", is_first=False)
# → "de"

capitalize_word("de", is_first=True)
# → "De"
```

---

## Notas

- O normalizer nao altera arquivos fora do diretorio de datasources
- Linhas em branco sao preservadas
- Encoding UTF-8 e mantido
- Nao afeta o locale `en/` automaticamente — rode separadamente se necessario:

```bash
cd datasources/en/
python ../normalizer.py capitalize
```
