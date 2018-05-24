from get_data import get_image_from_url
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from general import setup_logger


logger = setup_logger("email")


def send_mail(result, data, link):
    img_path = get_image_from_url(data["img_url"])

    fp = open(img_path, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    os.remove(img_path)

    from_addr = "kouril53@gmail.com"
    to_addr = "kouril53@gmail.com"
    username = "kouril53@gmail.com"
    password = "bulik01cz"
    keywords = ", ".join(result)
    msg = MIMEMultipart()
    msg["Subject"] = keywords + " " + data["price"]
    msg["From"] = from_addr
    msg["To"] = to_addr

    body = "cena: " + data["price"] + "\n" + "Místo: " + data["location"] + "\n" + "klíčová slova: " + keywords + "\n" + \
           data["title"] + "\n" + link
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(msg_image)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)

    server.send_message(msg)
    server.quit()
    logger.info("email send ; " + link)

    print("email odeslán")