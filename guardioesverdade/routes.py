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


@app.route("/socio-guardiao")
def socioguardiao():
    
    return render_template(
        "pages/socio-guardiao.html"
    )
@app.route("/socio-guardiao/<string:plano>/<int:price>")
@login_required
def assinar_plano(plano, price):
    try:
        link_pagamento = gera_link_pagamento(price)
        return redirect(link_pagamento)
    except ValueError as e:
        # TODO: Mostrar mensagem de erro ao usuário e capturar log.
        return str(e), 400

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
        payment_info = mp.get(f"/v1/payments/{payment_id}")

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
