from general import *
from get_data_from_links import get_data_bazos, get_data_sbazar
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
                data = get_data_sbazar(link)
            else:
                data = get_data_bazos(link)

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
        # send_mail(result, title, link, price, img_link)
        print("test email odeslan")
        # logger.info("email send - " + link)
    else:
        pass


def send_mail(result, title, link, price, img_link):

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
    image = MIMEImage(img_data, name=os.path.basename(r"crawler_files/"+ img_name ))
    msg.attach(image)

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
    page1 = [r"219-starozitny-nabytek", r"nabytek.bazos.cz/kresla/"]
    page = [r"nabytek.bazos.cz/kresla/"]
    for i in page1:
        print("testuju", i)
        start(i)

    # test_link = "https://stroje.bazos.cz/inzerat/84820308/Koupim-kompresor-PKD-6-nebo-12.php"
    # get_words_bazos(test_link)
