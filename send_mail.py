import os
import yagmail
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from general import setup_logger
from get_data import get_image_from_url


def send_mails(links_to_send_by_email, test=False):
    for link_data in links_to_send_by_email:
        if test:
            print(f'test - sending a mail with {link_data["link"]}')
        else:
            print(f'tohle neni test - sending a mail with {link_data["link"]}')
            # send_mail_smtplib(link_data)
            send_mail_yagmail(link_data)


def send_mail_yagmail(data):
    logger = setup_logger("email")

    receiver = "kouril53@gmail.com"
    receiver = "karelundkarel@gmail.com"
    filename = get_image_from_url(data["img_url"])
    # filename = get_image_from_url(data["img_url"])

    keywords = ", ".join(data["keywords"])
    price = f'cena: {data["price"]}'
    location = f'místo: {data["location"]}'
    keywords_text = f'klíčová slova: {keywords}'
    body = f'{price}\n{location}\n{keywords_text}\n{data["title"]}\n{data["link"]}'

    yag = yagmail.SMTP("karelundkarel@gmail.com", "hwojpuqybnbmnqbp")
    yag.send(
        to=receiver,
        subject=f'{keywords} {data["price"]}',
        contents=body,
        attachments=filename,
    )

    # os.remove(filename)
    logger.info("email send ; " + data["link"])


def send_mail_smtplib(data):
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


if __name__ == '__main__':
    single_data = {
        'link': 'https://www.sbazar.cz/martin.tolnay/detail/113051516-starozitna-zidle-thonet-nr-a-238-schneck',
        'img_url': 'https://d46-a.sdn.cz/d_46/c_img_gU_E/gOtGHu.jpeg?fl=exf|crr,1.33333,2|res,1024,768,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1',
        'title': 'starožitná židle THONET Nr. A 238 Schneck', 'price': '3\xa0949', 'user': 'martin tolnay',
        'location': 'Jedovnice',
        'words_set': {'výplet', 'opěrky', 'model', 'po', 'dubového', 'osobní', '1928', 'pořádku', 'převzetí',
                      'starožitná', 'černé', 'dřeva', 'židle', 'málo', 'patinou', 'a', 'doprava', 'renovaci', 'sedáku',
                      'nr', 'nebo', 'šelakem', 'pěkném', 'zajímavý', 'konstrukce', '238', 'architekt', 'gustav', 's',
                      'povrchu', 'dostupný', 'thonet', 'roce', 'v', 'stavu', 'mírně', 'navrhl', 'poškozen', 'pevná',
                      'přeleštěno', 'schneck', 'lakování', 'kterou', 'značky', 'imitací', 'nálepka', 'původní',
                      'adolf', 'zaslání', 'lehké', 'kurýrem'}, 'website': 'sbazar', 'keywords': {'thonet'}
    }
    send_mail_yagmail(single_data)
