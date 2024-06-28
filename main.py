#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    A Database Populator is a tool which helps you to populate your projects' database tables
    with randomly generated content. With this tool you no longer need to write queries or to
    compile forms by yourself wasting a lot of time before to start to work on your applications.
"""
__author__ = "Luiz F. P. Quirino"
__copyright__ = "Copyleft 2020, Planet Earth"
__credits__ = ["LuizQuirino"]
__license__ = "GPL v3"
__version__ = "2.0.0"
__maintainer__ = "LuizQuirino"
__email__ = "luizfpq@gmail.com"
__status__ = "Dev"
import os
import subprocess

def mostrar_menu():
    print("\nMenu Principal")
    print("1. Inserir uma nova tabela (table_maker.py)")
    print("2. Criar arquivo de população (table_populator.py)")
    print("3. Sair")

def executar_opcao(opcao):
    if opcao == '1':
        print("Executando table_maker.py...")
        subprocess.run(["python", "table_maker.py"])
    elif opcao == '2':
        print("Executando table_populator.py...")
        subprocess.run(["python", "table_populator.py"])
    elif opcao == '3':
        print("Saindo do programa.")
        exit()
    else:
        print("Opção inválida. Tente novamente.")

def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")
        executar_opcao(opcao)

if __name__ == "__main__":
    main()
