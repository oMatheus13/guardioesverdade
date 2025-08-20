import os

from flask_login import current_user

from app.api.mercadopago.mp_config import PLANO_MAP, BACK_URLS_MAP

import mercadopago


TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")


def gera_link_pagamento(price):
    """
    Gera um link de pagamento para o plano selecionado.
    """
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
            "success": BACK_URLS_MAP["success"],
            "pending": BACK_URLS_MAP["pending"],
            "failure": BACK_URLS_MAP["failure"]  
        },
        "auto_return": "approved",
        "external_reference": f"user_{current_user.id}_plano_{plano_nome.replace(' ', '_')}",
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_pagamento = payment["init_point"]
    return link_pagamento

