import re
import requests
from bs4 import BeautifulSoup
import urllib.request

def get_data_sbazar(link):
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    img = soup.findAll("img")[2]["src"]
    print(img)
    if img.startswith(r"//img.sbazar.cz"):
        img_link = "https:" + img
    else:
        img_link = "https://www.sbazar.cz/img/logo-sbazar.png"

    print(img_link)

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


def get_data_bazos(link):
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    img = soup.findAll("img")[1]["src"]
    if img.startswith("https://www.bazos.cz/img"):
        img_link = img.split("?t=")[0]
    else:
        img_link = "https://www.bazos.cz/obrazky/bazos.gif"
    print(img_link)

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
    return words_set, title, price, user, img_link


def get_jpg(url):
    name = url.split("/")[-1]
    path = r"crawler_files/" + name
    print(name)
    urllib.request.urlretrieve(url, path)


if __name__ == "__main__":

    # test_link = "https://nabytek.bazos.cz/inzerat/85338401/Prodam-sedacku-a-stolek-z-palet.php"
    # get_data_bazos(test_link)

    # test_link = "http://www.sbazar.cz/prenosilova111/detail/27642202-starozitna-skrin-orechove-drevo"
    # get_data_sbazar(test_link)

    img_links = ["https://img.sbazar.cz/big-lq/201801/2812/ed/5a6dc0f1edcdc506edde0100.jpg", "https://www.bazos.cz/img/1/769/85266769.jpg", "https://www.bazos.cz/obrazky/bazos.gif", "https://www.sbazar.cz/img/logo-sbazar.png"]
    for i in img_links:
        get_jpg(i)