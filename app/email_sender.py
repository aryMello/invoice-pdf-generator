import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def send_email(to_email, subject, body, attachment_path, smtp_settings):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_settings["from_email"]
    msg["To"] = to_email
    msg.set_content(body)

    # Attach the PDF
    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(attachment_path)
        )

    # Load credentials from environment variables
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    if not username or not password:
        raise ValueError("Missing EMAIL_USERNAME or EMAIL_PASSWORD environment variables.")

    # Connect and send
    with smtplib.SMTP(smtp_settings["host"], smtp_settings["port"]) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
