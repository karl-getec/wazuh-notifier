import smtplib
from email.message import EmailMessage

class MailClient:

    def __init__(self, config):

        self.config = config

    def send(self, subject: str, body: str):

        smtp = self.config.smtp

        if not smtp["enabled"]:
            print("SMTP desabilitado.")
            return

        message = EmailMessage()

        message["From"] = smtp["sender"]
        message["To"] = ", ".join(smtp["recipients"])
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(smtp["host"], smtp["port"]) as server:

            server.starttls()

            server.login(
                smtp["username"],
                smtp["password"]
            )

            server.send_message(message)

        print("E-mail enviado com sucesso.")