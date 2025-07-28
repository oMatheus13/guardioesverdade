from deep_translator import GoogleTranslator
import os
import re

def traduzir_nome_arquivo(nome_arquivo, idioma_destino='pt'):
    nome_base, extensao = os.path.splitext(nome_arquivo)

    try:
        nome_traduzido = GoogleTranslator(source='auto', target=idioma_destino).translate(nome_base)

        # Limpeza
        nome_traduzido = re.sub(r'[^\w\s\-]', '', nome_traduzido).strip()
        nome_traduzido = re.sub(r'\s+', '-', nome_traduzido).lower()

        return f"{nome_traduzido}{extensao}"

    except Exception as e:
        print(f"Erro ao traduzir '{nome_arquivo}': {e}")
        return None

def renomear_arquivos_html(diretorio, idioma_destino='pt'):
    for nome in os.listdir(diretorio):
        if nome.endswith('.html'):
            antigo = os.path.join(diretorio, nome)
            novo = traduzir_nome_arquivo(nome, idioma_destino)
            if novo:
                novo_caminho = os.path.join(diretorio, novo)
                os.rename(antigo, novo_caminho)
                print(f"Renomeado: {nome} → {novo}")

# Teste
diretorio = r'D:\Projetos13_\Web\guardioesverdade\guardioesverdade\templates\pages'
renomear_arquivos_html(diretorio)
