import os

def process_files_in_folder(folder_path, action):
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

                if action == 'uppercase':
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

folder_path = '.'  # Diretório atual
process_files_in_folder(folder_path, 'uppercase')
