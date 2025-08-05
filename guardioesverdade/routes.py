from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from guardioesverdade import app
from guardioesverdade.forms import UserForm, LoginForm
from guardioesverdade.api.mercadopago.mp_api import gera_link_pagamento


@app.route("/")
def homepage():

    return render_template("index.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()

        if user:
            login_user(user, remember=True)
            return redirect(url_for("homepage"))
    
    return render_template("login/login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for("homepage"))
    
    return render_template("login/cadastro.html", form=form)


@login_required
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



import os

from flask import request

from guardioesverdade import db, app
from guardioesverdade.models import User

import mercadopago


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
