
import os
from flask import request
import mercadopago
from guardioesverdade import db, app
from guardioesverdade.models import User, Assinatura
from guardioesverdade.api.mercadopago.mp_api import PLANO_MAP
from datetime import datetime, timedelta


TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")
mp = mercadopago.SDK(TOKEN_MERCADOPAGO)


@app.route("/mercadopago/webhook", methods=["POST"])
def mercadopago_webhook():
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
                    print(f"Plano do usuário {user.id} atualizado para {plano_nome}.")
                else:
                    print(f"Usuário com ID {user_id} não encontrado.")
            else:
                print(f"Formato de external_reference inválido: {external_reference}")
    
    return "Webhook recebido", 200
