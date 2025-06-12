import requests
import smtplib
from email.message import EmailMessage
from app.config_manager import load_config

def send_to_discord(file_path):
    config = load_config()
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(config['discord_webhook_url'], files=files)
    print("Discord webhook response:", response.status_code)

def send_email(file_path):
    config = load_config()
    if not config['email_enabled']:
        return
    msg = EmailMessage()
    msg['Subject'] = 'New Voicemail'
    msg['From'] = config['email_user']
    msg['To'] = config['email_recipient']
    msg.set_content("New voicemail attached.")
    with open(file_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='audio', subtype='wav', filename='voicemail.wav')
    with smtplib.SMTP_SSL(config['email_smtp_server'], 465) as server:
        server.login(config['email_user'], config['email_pass'])
        server.send_message(msg)
    print("Email sent successfully.")
