from get_data import get_image_from_url

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from general import setup_logger
import os


def send_mails(all_data, test=False):
    for data in all_data:
        if test:
            print(f'test - sending a mail with {data["link"]}')
        else:
            # print("tohle neni test")
            send_mail(data)


def send_mail(data):
    logger = setup_logger("email")
    img_path = get_image_from_url(data["img_url"])

    fp = open(img_path, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    os.remove(img_path)

    from_addr = "kouril53@gmail.com"
    to_addr = "kouril53@gmail.com"
    username = "kouril53@gmail.com"
    password = "Bulik01cz"
    keywords = ", ".join(data["keywords"])

    msg = MIMEMultipart()
    msg["Subject"] = f'{keywords} {data["price"]}'
    msg["From"] = from_addr
    msg["To"] = to_addr

    price = f'cena: {data["price"]}'
    location = f'místo: {data["location"]}'
    keywords_text = f'klíčová slova: {keywords}'

    body = f'{price}\n{location}\n{keywords_text}\n{data["title"]}\n{data["link"]}'
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(msg_image)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)

    server.send_message(msg)
    server.quit()
    logger.info("email send ; " + data["link"])
