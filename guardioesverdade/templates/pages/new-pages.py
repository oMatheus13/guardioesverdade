# script.py
import os

def criar_estrutura():
    caminho_base = r"D:\Projetos13_\Web\guardioesverdade\guardioesverdade\templates\pages\pagamentos"
    os.makedirs(caminho_base, exist_ok=True)

    arquivos = ["aprovado.html", "recusado.html", "pendente.html", "erro.html", "cancelado.html", "reembolsado.html", "em_analise.html"]
    for arquivo in arquivos:
        caminho_completo = os.path.join(caminho_base, arquivo)
        with open(caminho_completo, "w") as f:
            pass  # Cria o arquivo vazio

if __name__ == "__main__":
    criar_estrutura()