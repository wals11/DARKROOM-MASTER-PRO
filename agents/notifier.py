import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def send_notification(
    run_id: str,
    strategy: dict,
    captions: dict,
    drive_url: str | None,
    image_path: str,
) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_to = os.getenv("NOTIFICATION_EMAIL_TO")
    email_from = os.getenv("NOTIFICATION_EMAIL_FROM") or smtp_user

    if not all([smtp_host, smtp_user, smtp_password, email_to]):
        return False

    msg = MIMEMultipart("related")
    msg["Subject"] = f"Darkroom Master Pro — Post Ready: {strategy.get('topic', 'New Content')}"
    msg["From"] = email_from
    msg["To"] = email_to

    drive_link = (
        f'<p><a href="{drive_url}" style="color:#4a90e2;">View on Google Drive →</a></p>'
        if drive_url
        else ""
    )

    def _caption_block(platform: str) -> str:
        text = captions.get(platform, "").replace("\n", "<br>")
        return (
            f'<h4 style="margin:16px 0 4px;color:#555;">{platform.upper()}</h4>'
            f'<pre style="background:#f8f8f8;padding:12px;border-radius:6px;'
            f'font-size:13px;white-space:pre-wrap;">{text}</pre>'
        )

    html = f"""
<html>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;color:#1a1a1a;">
  <h2 style="border-bottom:2px solid #1a1a1a;padding-bottom:8px;">
    Darkroom Master Pro — Post Ready
  </h2>
  <p><strong>Run ID:</strong> {run_id}</p>
  <p><strong>Topic:</strong> {strategy.get('topic','')}</p>
  <p><strong>Angle:</strong> {strategy.get('angle','')}</p>
  <p><strong>Key message:</strong> {strategy.get('key_message','')}</p>
  <p><strong>Audience:</strong> {strategy.get('target_audience','')}</p>
  {drive_link}
  <p><img src="cid:post_image" style="max-width:480px;border-radius:8px;margin:12px 0;" /></p>
  <h3>Captions</h3>
  {"".join(_caption_block(p) for p in ("instagram", "facebook", "twitter", "linkedin"))}
</body>
</html>
"""

    msg.attach(MIMEText(html, "html"))

    img_file = Path(image_path)
    if img_file.exists():
        img_part = MIMEImage(img_file.read_bytes())
        img_part.add_header("Content-ID", "<post_image>")
        img_part.add_header("Content-Disposition", "inline", filename=img_file.name)
        msg.attach(img_part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, email_to, msg.as_string())

    return True
