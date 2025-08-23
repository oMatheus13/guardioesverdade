import os

# Nome da marca
nome_marca = "gv"  # Troque aqui

# Caminho da pasta dos SVGs
pasta_svg = "D:/Projetos13_/Web/guardioesverdade/assets/img/logo/svg"

# Variações
variacoes = [
    "logo-principal",
    "simbolo",
    "logo-horizontal",
    "logo-vertical",
    "tipografia",
    "simbolo-com-tag",
    "logo-com-tag",
    "logo-vertical-com-tag"
]

# Coleta e ordena os arquivos
arquivos = sorted(os.listdir(pasta_svg))

if len(arquivos) != 8:
    print(f"Erro: esperados 8 arquivos SVG, encontrados {len(arquivos)}.")
    exit()

for i in range(8):
    original = arquivos[i]
    base = variacoes[i]
    ext = os.path.splitext(original)[1]

    novo_nome = f"{nome_marca}-{base}{ext}"

    os.rename(os.path.join(pasta_svg, original), os.path.join(pasta_svg, novo_nome))
    print(f"[SVG] {original} → {novo_nome}")
