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
            send_mail_smtplib(link_data)
            # send_mail_yagmail(link_data)


def send_mail_yagmail(data):
    logger = setup_logger("email")

    receiver = "kouril53@gmail.com"
    receiver = "karelundkarel@gmail.com"
    filename = get_image_from_url(data["img_url"])

    keywords = ", ".join(data["keywords"])
    price = f'cena: {data["price"]}'
    location = f'místo: {data["location"]}'
    keywords_text = f'klíčová slova: {keywords}'
    # body = f'{price}\n{location}\n{keywords_text}\n{data["title"]}\n{data["link"]}'
    body = f'ahoj'

    yag = yagmail.SMTP("karelundkarel@gmail.com", "hwojpuqybnbmnqbp")
    yag.send(
        to=receiver,
        subject=f'{keywords} {data["price"]}',
        contents=body,
        attachments=filename,
    )

    os.remove(filename)
    logger.info("email send ; " + data["link"])


def send_mail_smtplib(data):
    logger = setup_logger("email")
    img_path = get_image_from_url(data["img_url"])

    fp = open(img_path, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    os.remove(img_path)

    from_addr = "karelundkarel@gmail.com"
    to_addr = "karelundkarel@gmail.com"
    username = "karelundkarel@gmail.com"
    password = "Bulik01cz"
    password = "karel1karel1"
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
    single_data = {'link': 'https://zvirata.bazos.cz/inzerat/142661276/nevska-maskarada-kotatka-s-pp.php',
                   'img_url': 'https://www.bazos.cz/img/1/276/142661276.jpg?t=1633553028', 'user': 'talisman nevy',
                   'location': '169 00 Praha 6', 'price': 'Dohodou', 'title': 'Něvská maškaráda koťátka s PP',
                   'words_set': {'narodili', 'žijí', 'očkovaná', 'i', 'telefonicky', 'koťátka', '07', 'mazlíčka',
                                 'testovaný', 'koťata', 'vynikající', 'nebo', 'jsou', 'plně', 'jak', 'tak', '2021',
                                 'něvská', '“talisman', 'námi', 'chovu', 'hcm', 'socializovaní', 'negativní',
                                 'chovatelská', 'vhodná', 'dvakrát', '“nabízí', 'nevy', 'odčervená', 'pp', '777002095',
                                 'maminka', 'do', 'domácnosti', 'fiv', 'chov', 'více', 's', 'se', 'testování',
                                 'informací', 'koťatka', 'tatínek', 'na', 'a', 'maškaráda', 'cz', '24', 'povahu',
                                 'kočičí', 'čipovaní', 'stanice', 'n/n', 'k', 'sms', 'vidění', 'zvyklí', 'prodeji',
                                 'rodiče', 'felv', 'mají', 'v', 'wc'}, 'keywords': {'test bazos'}, 'website': 'bazos'}

    data = {
        'link': 'https://www.sbazar.cz/trempy87/detail/153662259-obrazy',
        'img_url': 'https://d46-a.sdn.cz/d_46/c_img_QR_y/H3VOw9.jpeg?fl=exf|crr,1.33333,2|res,1024,768,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1',
        'title': 'Obrazy', 'price': '149', 'user': 'timmy7', 'location': 'Plzeň',
        'words_set': {'obrazy', 'cena', 'kus', 'za', 'uvedená', 'je'},
        'keywords': {'test sbazar'},
        'website': 'sbazar'}
    send_mail_yagmail(single_data)
    send_mail_yagmail(data)
