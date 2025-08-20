from flask import render_template
from flask_mail import Message
from app import app, mail


def enviar_email(assunto:str, destinatarios, template:str, **kwargs):
    """
    Função para enviar e-mails com templates HTML.
    """

    with app.app_context():
        try:
            html_body = render_template(f'pages/email/{template}', **kwargs)

            msg = Message(
                subject=assunto,
                recipients=destinatarios,
                html=html_body,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(msg)
            app.logger.info(f"E-mail enviado com sucesso para {destinatarios}")
        
        except Exception as e:
            app.logger.error(f"Falha ao enviar e-mail para {destinatarios}: {e}")