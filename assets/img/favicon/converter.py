from PIL import Image
import os

print("Arquivos na pasta:", os.listdir())

# Caminho do seu .jpg
arquivo = "D:/Projetos13_/Web/guardioesverdade/assets/img/favicon/favicon.jpg"

# Abre e converte
img = Image.open(arquivo)

# Converte pra RGBA se necessário
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Salva como .ico
img.save("favicon.ico", format='ICO', sizes=[(128, 128)])  # Você pode usar (16,16), (32,32), etc.
