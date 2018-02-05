from general import *
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


logger = setup_logger("email")


def get_links_sbazar(project):
    link_list = []

    source_code = requests.get(r"http://www.sbazar.cz/" + project).text
    soup = BeautifulSoup(source_code, "html.parser")
    links = soup.find("div", id="mrEggsResults").find_all("a",class_="mrEggPart")

    for line in links:
        link = line.get("href")
        link_list.append("http://www.sbazar.cz" + link)

    return link_list


def get_links_bazos(project):
    link_list = []
    link_address = project.split("/", 1).pop(0)

    source_code = requests.get("https://" + project).text
    soup = BeautifulSoup(source_code, "html.parser")

    for line in soup.find_all("a"):
        link = line.get("href").startswith("/inzerat")
        if link is True:
            link_list.append("https://" + link_address + line.get("href"))

    link_list = set(link_list)
    return link_list


def get_words_sbazar(link):
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    img = soup.findAll("img")[2]
    if img.startwith(r"////img.sbazar.cz"):
        img_link = "http:" + img["src"]
    else:
        img_link = "https://www.sbazar.cz/img/logo-sbazar.png"
    print(img)
    print(img_link)
    print(link)

    title = soup.title.string
    # print(title + "\n" + link)

    try:
        price = soup.find("span", itemprop="price").contents[0]
    except IndexError:
        price = "cena neuvedena"
        pass

    try:
        user = soup.find("dd", itemprop="familyName").contents[0].string
        user = user.lower()

    except IndexError:
        user = ""
        # print("nema uzivatele")
        pass

    try:
        body = soup.find("span", itemprop="description").contents[0]

    except IndexError:
        body = "inzerát bez textu"
        # print("nemá text")
        pass

    title_body = title + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    words_set = set(title_body.lower().split())

    return words_set, title, price, user, img_link


def get_words_bazos(link):
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    title = soup.title.string
    title_split = str(title)
    title_split = title_split.replace("<br>", "").replace("<br/>", "").replace("\\r", "").replace("\\n", "")
    title_split = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_split)
    title_set = set(title_split.lower().split())
    # print(title + "\n" + link)

    tabulka = soup.find("table", cellspacing=1).find_next("td").find_next_sibling("td")

    user = tabulka.find_next("b").string
    user = user.lower()

    price = tabulka.find_next("b").find_next("b").string

    text = soup.find("div", {"class": "popis"}).contents
    string = str(text)
    string = string.replace("<br>", "").replace("<br/>", "").replace("</br>", "").replace("\\r", "").replace("\\n", "")
    string = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', string)
    words_set = set(string.lower().split())

    words_set = words_set.union(title_set)
    return words_set, title, price, user


def search_links(project):

    stopword_set = set(select_stopwords())
    keyword_set = set(select_wordlist())

    if project[0].isdigit():
        queue_list = get_links_sbazar(project)
    else:
        queue_list = get_links_bazos(project)

    for link in queue_list:
        print("kontroluju", link)

        if not select_link_from_db(link):
            print("prochazim", link)
            if link.startswith("http://www.sbazar.cz"):
                data = get_words_sbazar(link)
            else:
                data = get_words_bazos(link)

            # compare_words(*data, link, stopword_set, keyword_set)

        else:
            continue


def compare_words(words_set, title, price, user, img_link, link, stopword_set, keyword_set):

    if not select_stopuser(user):
        pass
    elif stopword_set.intersection(words_set):
        pass

    elif keyword_set.intersection(words_set):
        result = set.intersection(keyword_set, words_set)
        # send_mail(result, title, link, price)
        print("test email odeslan")
        # logger.info("email send - " + link)
    else:
        pass


def send_mail(result, title, link, price):

    fromaddr = "kouril53@gmail.com"
    toaddr = "kouril53@gmail.com"
    username = "kouril53@gmail.com"
    password = "bulik01cz"
    keywords = ", ".join(result)
    msg = MIMEMultipart()
    msg["Subject"] = keywords + " " + price
    msg["From"] = fromaddr
    msg["To"] = toaddr

    body = title + "\n" + link
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    # https: // www.google.com / settings / security / lesssecureapps
    # server.sendmail(fromaddr, toaddr, msg)
    server.send_message(msg)
    server.quit()
    logger.info("email send - " + link)

    # print("email odeslán")


def start(project):
    create_project_dir()
    search_links(project)


if __name__ == "__main__":
    # # page1 = [r"219-starozitny-nabytek", r"nabytek.bazos.cz/kresla/"]
    # page = [r"219-starozitny-nabytek"]
    # for i in page:
    #     print("testuju", i)
    #     start(i)

    test_link = "https://www.sbazar.cz/l.korytak/detail/27782921-ceskoslovensky-billiardovy-stul"
    get_words_sbazar(test_link)
