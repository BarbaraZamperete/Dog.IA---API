import os

# Diretório onde as imagens estão localizadas
directory = r"C:/Users/barbarazamperete/Desktop/dogia-imgs/Banco de Dados Novo/Salsicha/Dachshund"

# Lista todos os arquivos no diretório
files = os.listdir(directory)

# Filtra apenas os arquivos JPEG
jpeg_files = [f for f in files if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')]

# Inicializa o contador
counter = 1

# Renomeia cada arquivo
for file in jpeg_files:
    # Define o novo nome do arquivo
    new_name = f"dachshund.{counter}.jpg"
    
    # Define o caminho completo do arquivo antigo e do novo
    old_path = os.path.join(directory, file)
    new_path = os.path.join(directory, new_name)
    
    # Renomeia o arquivo
    os.rename(old_path, new_path)
    
    # Incrementa o contador
    counter += 1

print("Renomeação concluída com sucesso!")
