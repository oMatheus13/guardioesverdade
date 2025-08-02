from flask import render_template

from guardioesverdade import app, db
from guardioesverdade.models import User
from guardioesverdade.mercadopago.api_mp import gera_link_pagamento


@app.route("/")
def homepage():

    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login/login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("login/cadastro.html")


@app.route("/socio-guardiao")
def socioguardiao():
    d_15 = gera_link_pagamento(15)
    d_30 = gera_link_pagamento(30)
    d_50 = gera_link_pagamento(50)
    d_100 = gera_link_pagamento(100)
    # d_livre = gerar_link_pagamento(donate_livre)
    
    return render_template(
        "pages/socio-guardiao.html", d15 = d_15, d30 =d_30, d50 = d_50, d100 = d_100,
        # dlivre = d_livre
    )

@app.route("/sobre")
def sobre():
    return render_template("pages/sobre.html")


@app.route("/album")
def album():
    return render_template("pages/album.html")


@app.route("/classes")
def classes():
    return render_template("pages/classes.html")

    
@app.route("/contato")
def contato():
    return render_template("pages/contato.html")

@app.route("/dracmas")
def dracmas():
    return render_template("pages/dracmas.html")

@app.route("/eventos")
def eventos():
    return render_template("pages/eventos.html")

@app.route("/arearestrita")
def arearestrita():
    return render_template("pages/arearestrita.html")

@app.route("/unidades")
def unidades():
    return render_template("pages/unidades.html")


# @app.route("/doacoes")
# def donate():
#     d_1 = gera_link_pagamento(1)
#     d_15 = gera_link_pagamento(15)
#     d_30 = gera_link_pagamento(30)
#     d_50 = gera_link_pagamento(50)
#     # d_livre = gerar_link_pagamento(donate_livre)
    
#     return render_template(
#         "mercado-pago/doacao.html", d1 = d_1, d15 = d_15, d30 =d_30, d50 = d_50,
#         # dlivre = d_livre
#     )
