import os
from datetime import datetime, timedelta

from flask import request

from guardioesverdade import app, db
from guardioesverdade.models import User, Assinatura





def verifica_assinaturas_expiradas():
    """
    FUNÇÃO CHAMADA POR UM CRON JOB.
    Verifica se assinaturas estão em período de carência ou
    se expiraram e atualiza o estado delas e do usuário.
    """

    with app.app_context():

        data_limite_carencia = datetime.now() - timedelta(days=7)


        # 1. Encontra assinaturas ativas, mas que expiraram e as coloca em estado de carência
        assinaturas_ativas_expiradas = Assinatura.query.filter(
            Assinatura.estado == "ativo",
            Assinatura.data_expiracao < datetime.now()
        ).all()

        for assinatura in assinaturas_ativas_expiradas:
            try:
                assinatura.estado = "aguardando renovação"
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Erro ao atualizar assinatura ({assinatura.id}) para estado de carencia: {e}")

        
        # 2. Encontra assinaturas em estado de carência, com prazo esgotado e as desativa
        assinaturas_carencia_expiradas = Assinatura.query.filter(
            Assinatura.estado == "aguardando renovação",
            Assinatura.data_expiracao < data_limite_carencia
        ).all()

        for assinatura in assinaturas_carencia_expiradas:
            """
            Tenta desativar assinaturas expiradas e remover suas referencias dos usuarios. 
            """
            try:
                assinatura.estado = "inativo"
                
                user = User.query.get(assinatura.id_user)
                if user and user.id_assinatura_ativa == assinatura.id:
                    user.plano = "gratuito"
                    user.id_assinatura_ativa = None
                
                db.session.commit()
                app.logger.info(f"Assinatura {assinatura.id} desativada com sucesso.")
            
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Erro ao desativar assinatura {assinatura.id}: {e}")


        # 3. TODO: Implementar lógica para verificar planos consecutivos

        app.logger.info(f"Verificação de {datetime.now().day}/{datetime.now().month}/{datetime.now().year} 
                        de assinaturas encerrada!")



@app.route("/api/cron/verifica-assinaturas")
def cron_verifica_assinaturas():
    """
    Endpoint chamado por Cron Job para verificação de assinaturas expiradas.
    Verifica se o token de autorização está presente na requisição.
    """

    token = request.headers.get("Authorization")
    cron_secret = os.getenv("CRON_SECRET")

    if not token or token != f"Bearer {cron_secret}":
        return "Unauthorized", 401

    verifica_assinaturas_expiradas()
    return "OK", 200