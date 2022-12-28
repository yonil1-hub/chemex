import smtplib
from email.message import EmailMessage
smtp_ob = smtplib.SMTP('smtp.gmail.com', 587)
smtp_ob.starttls()
smtp_ob.login("chemextutorial@gmail.com", "passwordforchem")

msg = EmailMessage()
msg['subject'] = "test"
msg['From'] = "chemextutorial@gmail.com"
msg['To'] = "jamescog72@gmail.com"
msg.set_content("this is test")
smtp_ob.send_message(msg)

