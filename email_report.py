import smtplib
from email.message import EmailMessage
from credentials import EMAIL_ADDRESS, EMAIL_PASSWORD, MANAGER_EMAIL


# noinspection PyTypeChecker
def send_email_with_pdf(subject: object, body: object, attachment_path: object) -> object:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = MANAGER_EMAIL
    msg.set_content(body)

    with open(attachment_path,'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename="Shopify_Weekly_Report.pdf")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("🗣️ Email sent to the company!")
