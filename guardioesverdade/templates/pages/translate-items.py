import os
from googletrans import Translator
import re

def traduzir_nome_arquivo(nome_arquivo, idioma_destino='pt-br'):
    """
    Traduz o nome de um arquivo usando o Google Translate e o formata para pt-br.

    Args:
        nome_arquivo (str): O nome do arquivo a ser traduzido.
        idioma_destino (str): O código do idioma para o qual traduzir (padrão: 'pt-br').

    Returns:
        str: O nome do arquivo traduzido e formatado.
    """
    translator = Translator()

    # Extrai o nome base e a extensão do arquivo
    nome_base, extensao = os.path.splitext(nome_arquivo)

    try:
        # Traduz o nome base do arquivo
        traducao = translator.translate(nome_base, dest=idioma_destino.split('-')[0])  # Pega apenas 'pt' de 'pt-br'
        nome_traduzido = traducao.text

        # Remove caracteres inválidos e espaços extras
        nome_traduzido = re.sub(r'[^\w\s-', '', nome_traduzido).strip()
        nome_traduzido = re.sub(r'\s+', '-', nome_traduzido) # Substitui espaços por hífens

        # Formata para minúsculas
        nome_traduzido = nome_traduzido.lower()

        # Adiciona a extensão original
        novo_nome_arquivo = f"{nome_traduzido}{extensao}"

        return novo_nome_arquivo

    except Exception as e:
        print(f"Erro ao traduzir o nome do arquivo '{nome_arquivo}': {e}")
        return None

def renomear_arquivos_html(diretorio, idioma_destino='pt-br'):
    """
    Renomeia todos os arquivos HTML em um diretório, traduzindo seus nomes para o idioma de destino.

    Args:
        diretorio (str): O caminho para o diretório contendo os arquivos HTML.
        idioma_destino (str): O código do idioma para o qual traduzir (padrão: 'pt-br').
    """
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.endswith('.html'):
            caminho_antigo = os.path.join(diretorio, nome_arquivo)
            novo_nome_arquivo = traduzir_nome_arquivo(nome_arquivo, idioma_destino)

            if novo_nome_arquivo:
                caminho_novo = os.path.join(diretorio, novo_nome_arquivo)
                try:
                    os.rename(caminho_antigo, caminho_novo)
                    print(f"Arquivo '{nome_arquivo}' renomeado para '{novo_nome_arquivo}'")
                except Exception as e:
                    print(f"Erro ao renomear o arquivo '{nome_arquivo}': {e}")

# Exemplo de uso:
diretorio_dos_arquivos = r'D:\Projetos13_\Web\guardioesverdade\guardioesverdade\templates\pages'
renomear_arquivos_html(diretorio_dos_arquivos, idioma_destino='pt-br')