from general import *
from get_data_from_links import get_data_bazos, get_image_from_url, get_data_sbazar
# import requests
# from bs4 import BeautifulSoup
from requests_html import HTMLSession
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


logger = setup_logger("email")


def get_links_sbazar(url):
    session = HTMLSession()
    r = session.get(f"http://www.sbazar.cz/" + url)

    url_list = []
    tags = r.html.find("a.c-item__link")

    for tag in tags:
        url_list.append(list(tag.links)[0])

    return(url_list)


def get_links_bazos(raw_url):

    link_list = []
    counter = 0

    url_base = raw_url.split("/", 1).pop(0)

    while True:
        url = raw_url + "/" + str(counter) + "/"
        session = HTMLSession()
        r = session.get("https://" + url)

        a_tags = r.html.find("span.nadpis a")

        for tag in a_tags:
            link = list(tag.links)[0]
            link_list.append("https://" + url_base + link)

        top_tag = r.html.find(".ztop")
        if len(top_tag) == 0:
            break
        counter += 20

    return link_list


# def get_links_bazos(url):
#     link_list = []
#     counter = 0
#     while True:
#
#         link_address = url.split("/", 1).pop(0)
#         link = "https://" + url + "/" + str(counter) + "/"
#         source_code = requests.get(link).text
#         soup = BeautifulSoup(source_code, "html.parser")
#
#         for line in soup.find_all("a"):
#             link = line.get("href").startswith("/inzerat")
#             if link is True:
#                 link_list.append("https://" + link_address + line.get("href"))
#
#         top = soup.findAll("span", {"class": "ztop"})
#         if len(top) == 0:
#             break
#         counter += 20
#
#     link_list = set(link_list)
#     return link_list


def search_links(url):

    stopword_set = set(select_stopwords())
    keyword_set = set(select_wordlist())

    if url[0].isdigit():
        queue_list = get_links_sbazar(url)
    else:
        queue_list = get_links_bazos(url)

    for link in queue_list:
        print("kontroluju", link)

        if select_link_from_db(link):
            print("prochazim", link)
            if link.startswith("https://www.sbazar.cz"):
                data = get_data_sbazar(link)
            else:
                data = get_data_bazos(link)
            compare_words(data, link, stopword_set, keyword_set)

        else:
            continue


def compare_words(data, link, stopword_set, keyword_set):

    if not select_stopuser(data["user"]):
        pass
    elif stopword_set.intersection(data["words_set"]):
        pass

    elif keyword_set.intersection(data["words_set"]):
        result = set.intersection(keyword_set, data["words_set"])
        # send_mail(result, data, link)
        print("test email odesilan")
        # print("data - result", result)
        # print("data - title ", data["title"])
        # print("data - link, price, img", link, data["price"], data["img_url"], data["location"])
        # logger.info("email send - " + link)
    else:
        pass


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

    body = "cena: "+ data["price"] + "\n" + "Místo: " + data["location"] + "\n" + "klíčová slova: " + keywords + "\n" + data["title"] + "\n" + link
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(msg_image)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    # https: // www.google.com / settings / security / lesssecureapps
    # server.sendmail(fromaddr, toaddr, msg)
    server.send_message(msg)
    server.quit()
    logger.info("email send ; " + link)

    print("email odeslán")


def start(project):
    create_project_dir()
    search_links(project)


if __name__ == "__main__":
    project_list_bazos = ["nabytek.bazos.cz/kresla", "nabytek.bazos.cz/zidle", "ostatni.bazos.cz"]
    page = [r"300-kresla"]
    for i in page:
        print("testuju", i)
        print(get_links_sbazar(i))
        # start(i)
