from general import *
from get_data_from_links import get_data_bazos, get_data_sbazar, get_image_from_url
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


logger = setup_logger("email")


def get_links_sbazar(project):
    link_list = []

    source_code = requests.get(r"http://www.sbazar.cz/" + project).text
    soup = BeautifulSoup(source_code, "html.parser")
    links = soup.find("div", id="mrEggsResults").find_all("a", class_="mrEggPart")

    for line in links:
        link = line.get("href")
        link_list.append("http://www.sbazar.cz" + link)

    return link_list


# def get_links_bazos(project):
#     link_list = []
#     link_address = project.split("/", 1).pop(0)
#
#     source_code = requests.get("https://" + project).text
#     soup = BeautifulSoup(source_code, "html.parser")
#
#     for line in soup.find_all("a"):
#         link = line.get("href").startswith("/inzerat")
#         if link is True:
#             link_list.append("https://" + link_address + line.get("href"))
#
#     link_list = set(link_list)
#     return link_list


def get_links_bazos(project):
    link_list = []
    counter = 0
    while True:

        link_address = project.split("/", 1).pop(0)
        link = "https://" + project + "/" + str(counter) + "/"
        source_code = requests.get(link).text
        soup = BeautifulSoup(source_code, "html.parser")

        for line in soup.find_all("a"):
            link = line.get("href").startswith("/inzerat")
            if link is True:
                link_list.append("https://" + link_address + line.get("href"))

        top = soup.findAll("span", {"class": "ztop"})
        if len(top) == 0:
            break
        counter += 20


    link_list = set(link_list)
    return link_list


def search_links(project):

    stopword_set = set(select_stopwords())
    keyword_set = set(select_wordlist())

    if project[0].isdigit():
        queue_list = get_links_sbazar(project)
    else:
        queue_list = get_links_bazos(project)

    for link in queue_list:
        # print("kontroluju", link)

        if select_link_from_db(link):
            # print("prochazim", link)
            if link.startswith("http://www.sbazar.cz"):
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
        send_mail(result, data["title"], link, data["price"], data["img_url"])
        # print("test email odesilan")
        # print("data - result", result)
        # print("data - title ", data["title"])
        # print("data - link, price, img", link, data["price"], data["img_url"])
        # logger.info("email send - " + link)
    else:
        pass


def send_mail(result, title, link, price, img_link):

    img_path = get_image_from_url(img_link)

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
    msg["Subject"] = keywords + " " + price
    msg["From"] = from_addr
    msg["To"] = to_addr

    body = "cena: "+ price + "\n" + "klíčová slova: " + keywords + "\n" + title + "\n" + link
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
    # page1 = [r"219-starozitny-nabytek", r"nabytek.bazos.cz/kresla/"]
    # page = [r"nabytek.bazos.cz/kresla/"]
    # for i in page:
    #     print("testuju", i)
    #     start(i)
    #
    # # test_link = "https://stroje.bazos.cz/inzerat/84820308/Koupim-kompresor-PKD-6-nebo-12.php"
    # # get_words_bazos(test_link)

    test = get_links_bazos("nabytek.bazos.cz/zidle")
    print(test)
    print(len(test))