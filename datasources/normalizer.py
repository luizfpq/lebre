#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "2.0.1"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"
import os

def normalize_files(folder_path, action='capitalize'):
    if not os.path.exists(folder_path):
        print(f"A pasta '{folder_path}' não existe.")
        return
    
    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    if not txt_files:
        print(f"Nenhum arquivo .txt encontrado em '{folder_path}'")
        return

    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if action == 'capitalize':
                    modified_content = ' '.join(word.capitalize() for word in content.split())
                elif action == 'uppercase':
                    modified_content = content.upper()
                elif action == 'lowercase':
                    modified_content = content.lower()
                else:
                    print(f"Ação inválida '{action}'. Pulando o arquivo '{file_name}'.")
                    continue

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

            print(f"Arquivo '{file_name}' processado com sucesso.")

        except IOError:
            print(f"Erro ao processar o arquivo '{file_name}'.")

folder_path = '.'  # Diretório atual (onde este script está localizado)
normalize_files(folder_path, action='capitalize')
