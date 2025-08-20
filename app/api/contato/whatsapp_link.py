# Criptografia de URL
from urllib.parse import quote

def gerar_link_whatsapp(nome=None, sobrenome=None, email=None):
    if nome and sobrenome and email:
        msg_inicial = f"Olá, meu nome é {nome} {sobrenome}, meu email é {email}. Gostaria de saber mais sobre o Clube de Desbravadores Guardiões da Verdade."
    else:
        msg_inicial = f"Olá, gostaria de saber mais sobre o Clube de Desbravadores Guardiões da Verdade."
    
    msg_codificada = quote(msg_inicial)
    link_whatsapp = f"https://wa.me/5587981366161?text={msg_codificada}"
    return link_whatsapp

def link_whatsapp_usuario(usuario):
    nome = usuario.nome
    sobrenome = usuario.sobrenome
    telefone = usuario.telefone

    msg_inicial = f"Olá, {nome} {sobrenome}, somos do Clube de Desbravadores Guardiões da Verdade. Tem um momento?"
    msg_codificada = quote(msg_inicial)
    link_whatsapp = f"https://wa.me/{telefone}?text={msg_codificada}"

    return link_whatsapp
