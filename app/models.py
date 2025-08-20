from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)  # TODO: Tornar False ao resetar banco de dados
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    plano = db.Column(db.String(50), nullable=False, default='gratuito')
    maior_plano = db.Column(db.String(50), nullable=False, default='gratuito')
    
    # Chave estrangeira que aponta para o id da assinatura ativa. Pode ser nula.
    id_assinatura_ativa = db.Column(db.Integer, db.ForeignKey('assinaturas.id'), nullable=True)

    role = db.Column(db.String(20), nullable=False, default='user')
    data_criacao = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    # Relação para todas as assinaturas do usuário.
    # Usamos o `foreign_keys` para indicar qual coluna usar na tabela Assinatura.
    assinaturas = db.relationship(
        'Assinatura', back_populates='user', foreign_keys='Assinatura.id_user'
    )
    
    # Adicionamos uma nova relação para a assinatura ativa, usando a coluna id_assinatura_ativa.
    assinatura_ativa = db.relationship(
        'Assinatura', foreign_keys=[id_assinatura_ativa], post_update=True
    )

    def get_cpf(self):
        cpf = self.cpf
        if cpf and len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return None
    
    def get_plano(self):
        if self.id_assinatura_ativa:
            return self.assinatura_ativa
        return None


class Assinatura(db.Model):
    __tablename__ = 'assinaturas'

    id = db.Column(db.Integer, primary_key=True)
    nome_plano = db.Column(db.String(50), nullable=False)
    data_assinatura = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    data_expiracao = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='ativo')

    # Chave estrangeira que aponta para o id do usuário
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meses_consecutivos = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', back_populates='assinaturas', foreign_keys=[id_user])


    def __repr__(self):
        return (f'<Assinatura: {self.nome_plano}, User ID: {self.id_user}, '
                f'Data de Assinatura: {self.data_assinatura}, '
                f'Estado: {self.estado}, Expira em: {self.data_expiracao}>')

