import os
import hmac
import hashlib
from base64 import urlsafe_b64decode
from urllib.parse import parse_qs

from flask import request

from guardioesverdade import db, app
from guardioesverdade.models import User, Assinatura
from guardioesverdade.api.mercadopago.mp_config import PLANO_MAP
from datetime import datetime, timedelta

import mercadopago


TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
mp = mercadopago.SDK(TOKEN_MERCADOPAGO)



@app.before_request
def before_request_hook():
    """
    Hook executado antes de cada requisição.
    Verifica se a requisição é para o webhook do Mercado Pago e registra a tentativa de acesso.
    """
    if request.path == "/mercadopago/webhook":
        app.logger.info("Tentativa de acesso ao webhook do Mercado Pago.")


        # Lógica para recuperar o token de assinatura
        x_signature = request.headers.get("x-signature")

        if not x_signature:
            app.logger.warning("Acesso não autorizado ao webhook: 'x-signature' ausente.")
            return "Unauthorized", 401

        
        try:
            parts = parse_qs(x_signature.replace(',', '&'))
            client_id_assinatura = parts.get('id', [''])[0]
            timestamp = parts.get('ts', [''])[0]
            token = parts.get('v1', [''])[0]


            body = request.get.data().decode('utf-8')
            data_to_sign = f"id:{client_id_assinatura};ts:{timestamp};{body}"


            hmac_signature = hmac.new(
                CLIENT_SECRET.encode('utf-8'), 
                data_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()

            # Compara a assinatura recebida com a assinatura gerada
            if not hmac.compare_digest(urlsafe_b64decode(token), hmac_signature):
                app.logger.error("Assinatura do webhook inválida. Possível tentativa de falsificação.")
                return "Invalid Signature", 403
            
            
            app.logger.info("Assinatura de webhook validada com sucesso.")
        
        except Exception as e:
            app.logger.error(f"Erro na validação da assinatura: {e}")
            return "Internal Server Error during signature validation", 500




@app.route("/mercadopago/webhook", methods=["POST"])
def mercadopago_webhook():


    app.logger.info("Webhook do Mercado Pago recebido.")
    data = request.get_json()

    if not data or "data" not in data:
        return "Invalid data", 400
    
    topic = data.get("type", "")

    if topic == "payment":
        payment_id = data.get("data", {}).get("id")
        payment_info = mp.payment().get(payment_id)

        if payment_info["response"]["status"] == "approved":
            external_reference = payment_info["response"]["external_reference"]
            parts = external_reference.split("_")

            # Validação da external_reference
            if len(parts) >= 4 and parts[0] == "user" and parts[2] == "plano":
                user_id = parts[1]
                plano_nome = " ".join(parts[3:]).replace("_", " ")

                user = User.query.get(user_id)
                if user:
                    # Lógica para criar a nova assinatura
                    data_assinatura = datetime.now()
                    data_expiracao = data_assinatura + timedelta(days=33)

                    nova_assinatura = Assinatura(
                        nome_plano=plano_nome,
                        data_assinatura=data_assinatura,
                        data_expiracao=data_expiracao,
                        estado='ativo',
                        id_user=user.id
                    )
                    db.session.add(nova_assinatura)
                    db.session.commit()

                    # Atualiza o usuário com os dados da nova assinatura
                    user.plano = plano_nome
                    user.id_assinatura_ativa = nova_assinatura.id

                    # Lógica para verificar e atualizar o maior plano já assinado
                    PLANO_VALORES = {v: k for k, v in PLANO_MAP.items()}
                    maior_plano_valor_atual = PLANO_VALORES.get(user.maior_plano, 0)
                    novo_plano_valor = PLANO_VALORES.get(plano_nome, 0)
                    
                    if novo_plano_valor > maior_plano_valor_atual:
                        user.maior_plano = plano_nome

                    db.session.commit()
                    app.logger.info(f"Plano do usuário {user.id} atualizado para {plano_nome}.")
                else:
                    app.logger.warning(f"Usuário com ID {user_id} não encontrado.")
            else:
                app.logger.warning(f"Formato de external_reference inválido: {external_reference}")

    return "Webhook recebido", 200
