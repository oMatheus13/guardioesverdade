from flask import render_template, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

from guardioesverdade import app
from guardioesverdade.forms import UserForm, LoginForm
from guardioesverdade.api.mercadopago.mp_api import gera_link_pagamento
from guardioesverdade.api.contato.whatsapp_link import gerar_link_whatsapp


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
        user = form.save()
        if user:
            login_user(user, remember=True)
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
    """
    Garante que o link de pagamento para o plano selecionado
    só seja gerado se o usuário estiver autenticado.
    """
    try:
        link_pagamento = gera_link_pagamento(price)
        return redirect(link_pagamento)
    except ValueError as e:
        # TODO: Mostrar mensagem de erro ao usuário e capturar log.
        return str(e), 400


@app.route("/pagamento/aprovado")
def pagamento_aprovado():
    """
    Rota para exibir a página de pagamento aprovado.
    Lê os dados da sessão e renderiza a página de confirmação.
    """

    assinatura_confirmada = session.get('assinatura_confirmada')
    if not assinatura_confirmada:
        return redirect(url_for("homepage"))

    session.pop('assinatura_confirmada', None)  # Limpa os dados da sessão após uso

    return render_template(
        "pages/pagamento_aprovado.html",
        assinatura=assinatura_confirmada
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
    """
    Rota para contato e lógica para envio de mensagem dinâmica via api do whatsapp.
    """
    
    nome = current_user.nome if current_user.is_authenticated else None
    sobrenome = current_user.sobrenome if current_user.is_authenticated else None
    email = current_user.email if current_user.is_authenticated else None

    link_whatsapp = gerar_link_whatsapp(nome, sobrenome, email)

    return render_template("pages/contato.html", link_whatsapp=link_whatsapp)

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
