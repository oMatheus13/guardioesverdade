import os

from flask import request

from guardioesverdade import db, app
from guardioesverdade.models import User

import mercadopago


TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")
mp = mercadopago.MP(TOKEN_MERCADOPAGO)



@app.route("/mercadopago/webhook", methods=["POST"])
def mercadopago_webhook():
    data = request.get_json()

    if not data or "data" not in data:
        return "Invalid data", 400
    
    topic = data.get("type", "")

    if topic == "payment":
        payment_id = data.get("data", {}).get("id")

        payment_info = mp.get(f"/v1/payments/{payment_id}")

        if payment_info["response"]["status"] == "approved":
            external_reference = payment_info["response"]["external_reference"]

            parts = external_reference.split("_")

            if len(parts) >= 4 and parts[0] == "user" and parts[2] == "plano":
                user_id = parts[1]
                plano_nome = " ".join(parts[3:]).replace("_", " ")


                user = User.query.get(user_id)
                if user:
                    user.plano = plano_nome
                    db.session.commit()
                    print(f"Plano do usuário {user.id} atualizado para {plano_nome}.")
                else:
                    print(f"Usuário com ID {user_id} não encontrado.")

    return "Webhook recebido", 200
