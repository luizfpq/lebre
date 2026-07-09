#!/usr/bin/env python3
"""
Normalizer — utilitário para processar arquivos de datasource.

Suporta: uppercase, lowercase, capitalize (Title Case inteligente).
"""

from __future__ import annotations

import os
import sys


# Preposições e artigos que permanecem minúsculos em Title Case brasileiro
_LOWERCASE_WORDS = frozenset({
    'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'no', 'na', 'nos', 'nas',
    'por', 'para', 'com', 'sem',
})

# Siglas conhecidas que devem permanecer em maiúsculo
_UPPERCASE_WORDS = frozenset({
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
    'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
    'SP', 'SE', 'TO', 'BR', 'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'IX', 'X',
})


def capitalize_word(word: str, is_first: bool = False) -> str:
    """
    Aplica Title Case inteligente a uma palavra.

    - Siglas (UF, numerais romanos) permanecem em maiúsculo.
    - Preposições/artigos ficam em minúsculo (exceto se primeira palavra).
    - Palavras com apóstrofo são tratadas como compostas.
    - Palavras com 2 letras ou menos que são siglas ficam em maiúsculo.
    """
    upper = word.upper()

    if upper in _UPPERCASE_WORDS:
        return upper

    lower = word.lower()

    if not is_first and lower in _LOWERCASE_WORDS:
        return lower

    # Palavras com apóstrofo (D'ÁGUA → d'Água)
    if "'" in word:
        parts = word.split("'", 1)
        return parts[0].lower() + "'" + parts[1].capitalize()

    return word.capitalize()


def capitalize_line(line: str) -> str:
    """
    Aplica Title Case inteligente a uma linha inteira.
    Preserva campos separados por vírgula (formato CSV dos datasources).
    """
    if ',' in line:
        fields = line.split(',')
        result_fields = []
        for field in fields:
            field = field.strip()
            # Se é uma sigla de UF (2 chars), manter como está
            if field.upper() in _UPPERCASE_WORDS:
                result_fields.append(field.upper())
            else:
                words = field.split()
                capitalized = [
                    capitalize_word(w, is_first=(i == 0))
                    for i, w in enumerate(words)
                ]
                result_fields.append(' '.join(capitalized))
        return ','.join(result_fields)
    else:
        words = line.split()
        capitalized = [
            capitalize_word(w, is_first=(i == 0))
            for i, w in enumerate(words)
        ]
        return ' '.join(capitalized)


def process_files_in_folder(folder_path: str, action: str) -> None:
    """
    Processa todos os .txt de um diretório com a ação especificada.

    Actions: 'uppercase', 'lowercase', 'capitalize'
    """
    if not os.path.exists(folder_path):
        print(f"Erro: pasta '{folder_path}' não existe.", file=sys.stderr)
        sys.exit(1)

    txt_files = sorted(f for f in os.listdir(folder_path) if f.endswith(".txt"))

    if not txt_files:
        print(f"Nenhum arquivo .txt encontrado em '{folder_path}'.", file=sys.stderr)
        sys.exit(1)

    valid_actions = ('uppercase', 'lowercase', 'capitalize')
    if action not in valid_actions:
        print(
            f"Erro: ação '{action}' inválida. Use: {', '.join(valid_actions)}",
            file=sys.stderr
        )
        sys.exit(1)

    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if action == 'uppercase':
                modified = [line.upper() for line in lines]
            elif action == 'lowercase':
                modified = [line.lower() for line in lines]
            elif action == 'capitalize':
                modified = []
                for line in lines:
                    stripped = line.rstrip('\n')
                    if stripped:
                        modified.append(capitalize_line(stripped) + '\n')
                    else:
                        modified.append(line)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(modified)

            print(f"  ✓ {file_name}")

        except OSError as exc:
            print(f"  ✗ {file_name}: {exc}", file=sys.stderr)

    print(f"\n{len(txt_files)} arquivo(s) processado(s) com '{action}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python normalizer.py [uppercase|lowercase|capitalize]")
        print("  Processa todos os .txt no diretório atual.")
        sys.exit(0)

    action = sys.argv[1].lower()
    folder_path = os.path.dirname(os.path.abspath(__file__))
    process_files_in_folder(folder_path, action)
