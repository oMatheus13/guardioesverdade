import os

# Configurações das pastas
pastas = [
    {
        "caminho": "D:/Projetos13_/Web/guardioesverdade/assets/img/logo/coloridas",
        "sufixo": ""  # sem sufixo para coloridas
    },
    {
        "caminho": "D:/Projetos13_/Web/guardioesverdade/assets/img/logo/monocromaticas",
        "sufixo": "-mono"  # sufixo para monocromáticas
    }
]

# Nome da marca
nome_marca = "gv"  # Troque aqui

# Ordem das variações (8 pares = 16 arquivos)
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

# Processa cada pasta
for pasta_info in pastas:
    caminho = pasta_info["caminho"]
    sufixo = pasta_info["sufixo"]

    arquivos = sorted(os.listdir(caminho))

    if len(arquivos) != 16:
        print(f"Erro na pasta '{caminho}': esperados 16 arquivos, encontrados {len(arquivos)}.")
        continue

    for i in range(8):
        base = variacoes[i]
        preto = arquivos[i * 2]
        branco = arquivos[i * 2 + 1]

        ext_preto = os.path.splitext(preto)[1]
        ext_branco = os.path.splitext(branco)[1]

        novo_preto = f"{nome_marca}-{base}-preto{sufixo}{ext_preto}"
        novo_branco = f"{nome_marca}-{base}-branco{sufixo}{ext_branco}"

        os.rename(os.path.join(caminho, preto), os.path.join(caminho, novo_preto))
        os.rename(os.path.join(caminho, branco), os.path.join(caminho, novo_branco))

        print(f"[{caminho}] {preto} → {novo_preto}")
        print(f"[{caminho}] {branco} → {novo_branco}")
