from flask import (
    render_template, redirect, url_for, session, flash, request, jsonify
)
from flask_login import login_required, login_user, logout_user, current_user
from functools import wraps

from app import app, db, eventos_storage
from app.models import User, Evento
from app.forms import UserForm, LoginForm, EventoForm
from app.api.mercadopago.mp_api import gera_link_pagamento
from app.api.contato.whatsapp_link import gerar_link_whatsapp, link_whatsapp_usuario

import datetime


def admin_required(f):
    """
    Decorator para garantir que apenas usuários com papel de 'admin' possam acessar certas rotas.
    Redireciona para a homepage com uma mensagem flash se o usuário não for admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Acesso negado. É necessário ser admin para obter acesso.')
            return redirect(url_for("homepage"))
        return f(*args, **kwargs)
    return decorated_function
        


# Rotas públicas
@app.route("/new/")
def new_homepage():

    return render_template("newpages/index.html", user=current_user)

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
    
    return render_template("pages/login/login.html", form=form)

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

    return render_template("pages/login/cadastro.html", form=form)


# Rotas para Sócio Guardião
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
        "pages/email/payment/aprovado.html",
        assinatura=assinatura_confirmada
    )


# Outras rotas
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
    agora = datetime.datetime.now()

    # Lista os 3 proximos eventos marcados como publicos
    proximos_eventos = Evento.query.filter(
        Evento.is_publico == True,
        Evento.data_evento >= agora
    ).order_by(Evento.data_evento.asc()).limit(3).all()

    return render_template("pages/eventos.html", proximos_eventos=proximos_eventos)


@app.route("/unidades")
def unidades():
    return render_template("pages/unidades.html")


# Rotas administrativas
    
@app.route("/admin/eventos")
@login_required
@admin_required
def admin_eventos_dashboard():
    # Todos os eventos ordenados pela data mais recente
    eventos = Evento.query.order_by(Evento.data_evento.desc()).all()

    return render_template("pages/admin/eventos/eventos_dashboard.html", eventos=eventos)

@app.route("/admin/eventos/novo", methods=["GET", "POST"])
@login_required
@admin_required
def admin_eventos_create():
    form = EventoForm()
    admin = current_user

    if form.validate_on_submit():
        evento = form.save(admin)
        if evento:
            return redirect(url_for('admin_eventos_dashboard'))

    return render_template("pages/admin/eventos/eventos_novo.html", form=form)

@app.route("/admin/eventos/edit/<int:evento_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_eventos_edit(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        flash("Evento não encontrado.", "danger")
        return redirect(url_for('admin_eventos_dashboard'))
    
    admin = current_user
    form = EventoForm(obj=evento)

    if form.validate_on_submit():
        form.update(evento, admin)
        return redirect(url_for('admin_eventos_dashboard'))


    return render_template("pages/admin/eventos/eventos_edit.html", form=form, evento=evento)


@app.route("/admin/eventos/excluir/<int:evento_id>", methods=["POST"])
@login_required
@admin_required
def admin_eventos_delete(evento_id):
    evento = Evento.query.get(evento_id)
    if not evento:
        flash("Evento não encontrado.", "danger")
        return redirect(url_for('admin_eventos_dashboard'))

    admin = current_user
    form = EventoForm(obj=evento)
    form.delete(evento, admin)
    
    return redirect(url_for('admin_eventos_dashboard'))


@app.route("/area-restrita")
def area_restrita():
    users =  User.query.all()
    return render_template("pages/admin/area-restrita.html", users=users, link_whatsapp_usuario=link_whatsapp_usuario)




# ------ Rota para a API

@app.route("/api/upload-image-ckeditor", methods=["POST"])
@login_required
@admin_required
def upload_image_ckeditor():
    """
    Endpoint de API para o CKEditor fazer upload de imagens.
    """
    
    file = request.files.get("upload")

    if not file:
        return jsonify({"error": "Nenhum ficheiro enviado."}), 400
    
    image_url = eventos_storage.upload(file)

    if image_url:
        return jsonify({"url": image_url})
    else:
        return jsonify({"error": "Ocorreu um erro durante o upload"}), 500


# Rotas para testes
@app.route("/admin/new-admin/<int:user_id>")
@login_required
@admin_required
def tornar_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.role = 'admin'
        db.session.commit()
        return redirect(url_for('area_restrita'))
    else:
        return "Usuário não encontrado", 404


# Rotas para Doações - desativadas temporariamente

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
