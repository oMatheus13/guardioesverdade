from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    EmailField,
    PasswordField,
    BooleanField,
    DateField,
    DateTimeField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from app import app, db, bcrypt, eventos_storage
from app.models import User, Evento


class UserForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    cpf = StringField("CPF", validators=[DataRequired()])
    data_nascimento = DateField("Data de Nascimento", format="%Y-%m-%d", validators=[DataRequired()])
    telefone = StringField("Telefone", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmar_senha = PasswordField(
        "Confirmar Senha",
        validators=[DataRequired(), EqualTo('senha', message='As senhas devem coincidir.')]
    )
    submit = SubmitField("Cadastrar")


    # Funções validate_<campo> são usadas para validação personalizada e evocadas automaticamente pelo Flask-WTF
    def validate_email(self, email):
        """
        Verifica se o email já está cadastrado e levanta o erro ValidationError se já existir.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email já cadastrado.")

        
        
    
    def save(self):
        # Criptografa senhas
        senha = bcrypt.generate_password_hash(self.senha.data).decode("utf-8")
        if not str(senha).startswith("$2b$"):
            raise ValidationError("Senha criptografada incorretamente.")
        
        # Sanitiza CPF
        cpf = self.cpf.data.replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValidationError("CPF inválido. Deve conter 11 dígitos numéricos.")
        
        # Lógica para padronizar numeros de telefone no modelo (5587987654321)
        telefone = "".join(filter(str.isdigit, self.telefone.data))

        # Remove o DDI se ele já estiver presente
        if telefone.startswith("55"):
            telefone = telefone[2:]
            
        # Remove o 0 se ele for o primeiro dígito de um DDD
        if len(telefone) >= 11 and telefone[0] == '0' and telefone[1:3].isdigit():
            telefone = telefone[1:]

        # Verifica o tamanho do número (apenas DDD e número)
        if len(telefone) == 10:  # Ex: 1187654321
            # Adiciona nono dígito
            telefone = f"{telefone[:1]}9{telefone[1:]}"
        elif len(telefone) == 11 and telefone[2] == '9':  # Ex: 11987654321
            # É um número de celular de 9 dígitos
            pass
        else:
            raise ValidationError("Telefone inválido. Formato esperado: (DDD) 9XXXX-XXXX ou (DDD) XXXX-XXXX.")

        # Adiciona o DDI +55 padronizado
        telefone = f"+55{telefone}"
        

        try:
            user = User(
                nome = self.nome.data,
                sobrenome = self.sobrenome.data,
                cpf = cpf,
                data_nascimento = self.data_nascimento.data,
                telefone = telefone,
                email = self.email.data,
                senha = senha
            )
            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            print("Erro ao salvar usuário:", e)
            raise ValidationError("Erro ao salvar o usuário. Verifique os dados e tente novamente.")
        

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, self.senha.data):
            return user
        else:
            raise ValidationError("Email ou senha inválidos.")



class EventoForm(FlaskForm):
    titulo = StringField("Título do Evento*", validators=[DataRequired(), Length(min=3, max=120)])
    imagem_capa = FileField("Imagem de Capa (Banner)",
                            validators=[FileAllowed(['jpg', 'jpeg', 'png'],
                                                    'Apenas imagens .jpg, .jpeg ou .png são permitidas!'
    )])

    descricao_breve = TextAreaField("Descrição Breve* (Cards)", validators=[DataRequired(), Length(max=255)])
    roteiro_publico = TextAreaField("Roteiro Público*", validators=[DataRequired()])
    roteiro_privado = TextAreaField("Roteiro Privado (Opcional)")

    data_evento = DateTimeField("Data e Hora do Evento*", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    local = StringField("Local do Evento*", validators=[DataRequired(), Length(min=3, max=200)])
    is_publico = BooleanField("Evento público (Visível para todos)", default=True)

    submit = SubmitField("Salvar Evento")


    def save(self, admin):
        # Faz upload da imagem e obtém a URL
        imagem_url = eventos_storage.upload(self.imagem_capa.data)

        try:
            evento = Evento(
                id_admin = admin.id,
                titulo = self.titulo.data,
                imagem_capa_url = imagem_url,
                descricao_breve = self.descricao_breve.data,
                roteiro_publico = self.roteiro_publico.data,
                roteiro_privado = self.roteiro_privado.data or None,
                data_evento = self.data_evento.data,
                local = self.local.data,
                is_publico = self.is_publico.data
            )

            db.session.add(evento)
            db.session.commit()
            flash(f"Evento criado com sucesso!", "success")
            app.logger.info(
                f"Evento '{evento.titulo}' criado por Admin ID: {admin.id}, Nome: {admin.nome}"
            )
            return evento
        except Exception as e:
            db.session.rollback()
            # Se o save falhar, deleta a imagem que já foi enviada
            if imagem_url:
                eventos_storage.delete(imagem_url)
            flash("Erro ao salvar o evento. Verifique os dados e tente novamente.", "danger")
            app.logger.error(f"Erro ao salvar evento: {e}")
            return None  # Retorna None em caso de falha
    
    
    def update(self, evento, admin):
        # Atualiza a imagem (deleta a antiga, envia a nova)
        nova_imagem_url = eventos_storage.update(evento.imagem_capa_url, self.imagem_capa.data)

        try:
            evento.titulo = self.titulo.data
            evento.imagem_capa_url = nova_imagem_url # Atualiza a URL da imagem
            evento.descricao_breve = self.descricao_breve.data
            evento.roteiro_publico = self.roteiro_publico.data
            evento.roteiro_privado = self.roteiro_privado.data or None
            evento.data_evento = self.data_evento.data
            evento.local = self.local.data
            evento.is_publico = self.is_publico.data


            db.session.commit()
            flash(f"Evento atualizado com sucesso!", "success")
            app.logger.info(f"Evento '{evento.titulo}' atualizado por Admin ID: {admin.id}, Nome: {admin.nome}")
            return evento
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar o evento. Verifique os dados e tente novamente.", "danger")
            app.logger.error(f"Erro ao atualizar evento: {e}")
            return None
        
        
    def delete(self, evento, admin):
        imagem_url = evento.imagem_capa_url

        try:
            db.session.delete(evento)
            db.session.commit()

            if imagem_url:
                eventos_storage.delete(imagem_url)

            
            flash(f"Evento excluído com sucesso!", "success")
            app.logger.info(f"Evento '{evento.titulo}' excluído por Admin ID: {admin.id}, Nome: {admin.nome}")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao excluir o evento. Tente novamente.", "danger")
            app.logger.error(f"Erro ao excluir evento: {e}")
            raise ValidationError("Erro ao excluir o evento. Tente novamente.")
