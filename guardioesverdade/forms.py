from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    SubmitField,
    PasswordField,
    DateField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from guardioesverdade import db, bcrypt
from guardioesverdade.models import User


class UserForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    cpf = StringField("CPF", validators=[DataRequired()])
    data_nascimento = DateField("Data de Nascimento", format="%Y-%m-%d", validators=[DataRequired()])
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
        senha = bcrypt.generate_password_hash(self.senha.data).decode("utf-8")
        if not str(senha).startswith("$2b$"):
            raise ValidationError("Senha criptografada incorretamente.")
        cpf = self.cpf.data.replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValidationError("CPF inválido. Deve conter 11 dígitos numéricos.")


        try:
            user = User(
                nome = self.nome.data,
                sobrenome = self.sobrenome.data,
                cpf = cpf,
                data_nascimento = self.data_nascimento.data,
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
