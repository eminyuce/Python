from mcp import MCPServer, tool, resource
import smtplib
from email.message import EmailMessage


print(dir(MCPServer))

class MyServer(MCPServer):

    @tool(name="send_email", description="Send an email via SMTP")
    def send_email(self, to: str, subject: str, body: str) -> str:
        try:
            # E-posta ayarları
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "bizim.saglikli.urunlerimiz@gmail.com"
            sender_password = ""  # Gmail için uygulama şifresi

            # E-posta oluştur
            msg = EmailMessage()
            msg['From'] = sender_email
            msg['To'] = to
            msg['Subject'] = subject
            msg.set_content(body)

            # SMTP ile gönder
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            return f"Email sent to {to}"

        except Exception as e:
            return f"Failed to send email: {str(e)}"

    @resource(name="get_latest_report", description="Get latest sales report")
    def get_latest_report(self) -> str:
        return open("latest_report.txt").read()

if __name__ == "__main__":
    MyServer().run_stdio()
