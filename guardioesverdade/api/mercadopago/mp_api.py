import os

from flask_login import current_user

import mercadopago


TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")


PLANO_MAP = {
    15: "Guardião Base",
    30: "Guardião Fiel",
    50: "Guardião De Elite",
    100: "Guardião Da Aliança"
}

def gera_link_pagamento(price):

    if price not in PLANO_MAP:
        raise ValueError("Plano inválido. Escolha entre 15, 30, 50 ou 100.")

    plano_nome = PLANO_MAP[price]

    sdk = mercadopago.SDK(TOKEN_MERCADOPAGO)

    payment_data = {
        "items": [
            {
                "id": str(price),
                "title": f"{plano_nome}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": price
            }
        ],
        # TODO: ATUALIZAR BACK_URLS
        "back_urls": {
            "success": "https://guardioesverdade.vercel.app",
            "pending": "https://guardioesverdade.vercel.app/events",
            "failure": "https://guardioesverdade.vercel.app/events" 
        },
        "auto_return": "approved",
        "external_reference": f"user_{current_user.id}_plano_{plano_nome.replace(' ', '_')}",
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_pagamento = payment["init_point"]
    return link_pagamento

