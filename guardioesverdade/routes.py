from flask import render_template

from guardioesverdade import app
from guardioesverdade.mercadopago.api_mp import gera_link_pagamento

@app.route("/")
def homepage():

    return render_template("index.html")


@app.route("/doacoes")
def donate():
    d_15 = gera_link_pagamento(15)
    d_30 = gera_link_pagamento(30)
    d_50 = gera_link_pagamento(50)
    # d_livre = gerar_link_pagamento(donate_livre)
    
    return render_template(
        "mercado-pago/doacao.html", d15 = d_15,
        d30 =d_30, d50 = d_50,
        # dlivre = d_livre
        )