import os

import mercadopago

TOKEN_MERCADOPAGO = os.getenv("TOKEN_MERCADOPAGO")

def gera_link_pagamento(price):
    sdk = mercadopago.SDK(TOKEN_MERCADOPAGO)

    payment_data = {
        "items": [
            {
                "id": "1", "title": "doacao", "quantity": 1,
                "currency_id": "BRL", "unit_price": price
            }
        ],
        # TODO: ATUALIZAR BACK_URLS
        "back_urls": {
            "success": "https://guardioesverdade.vercel.app",
            "pending": "https://guardioesverdade.vercel.app/events",
            "failure": "https://guardioesverdade.vercel.app/events" 
        },
        "auto_return": "approved",
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_pagamento = payment["init_point"]
    print("Link gerado")
    return link_pagamento