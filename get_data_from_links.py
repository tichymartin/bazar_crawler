import re
import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image


# class LinkFinder:
#     def __init__(self, url):
#         self.url = url
#         self.link_list = []
#
#     def get_links_sbazar(self):
#         source_code = requests.get(r"http://www.sbazar.cz/" + self.url).text
#         soup = BeautifulSoup(source_code, "html.parser")
#         links = soup.find("div", id="mrEggsResults").find_all("a", class_="mrEggPart")
#
#         for line in links:
#             link = line.get("href")
#             self.link_list.append("http://www.sbazar.cz" + link)
#
#         return self.link_list
#
#     def get_links_bazos(self):
#         link_address = self.url.split("/", 1).pop(0)
#
#         source_code = requests.get("https://" + project).text
#         soup = BeautifulSoup(source_code, "html.parser")
#
#         for line in soup.find_all("a"):
#             link = line.get("href").startswith("/inzerat")
#             if link is True:
#                 self.link_list.append("https://" + link_address + line.get("href"))
#
#         link_list = set(self.link_list)
#         return link_list
#
#     def __repr__(self):
#         return f"link finder for url: {self.url}"


# class Crawler:
#     def __init__(self, url):
#         self.url = url
#
#     def get_data_bazos(self):
#         data = {}
#         source_code = requests.get(self.url).text
#         soup = BeautifulSoup(source_code, "html.parser")
#
#         # get img url
#         img = soup.findAll("img")[1]["src"]
#         if img.startswith("https://www.bazos.cz/img"):
#             img_url = img.split("?t=")[0]
#         else:
#             img_url = "https://www.bazos.cz/obrazky/bazos.gif"
#
#         data["img_url"] = img_url
#
#         # get title
#         title_string = str(soup.title.string)
#         data["title"] = title_string
#
#         # get user
#         tabulka = soup.find("table", cellspacing=1).find_next("td").find_next_sibling("td")
#         user = tabulka.find_next("b").string
#         user = user.lower()
#         data["user"] = user
#
#         # get price
#         price = str(tabulka.find_next("b").find_next("b").string)
#         data["price"] = price
#
#         # get words
#         body_list = soup.find("div", {"class": "popis"}).contents
#         body_string = " ".join(str(i) for i in body_list)
#         body_string = body_string + title_string
#         body_string = body_string.replace(
#             "<br>", "").replace("<br/>", "").replace("</br>", "").replace("\\r","").replace("\\n", "")
#         body_string = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', body_string)
#         words_set = set(body_string.lower().split())
#
#         data["words_set"] = words_set
#
#         return data
#
#     def get_data_sbazar(self):
#         data = {}
#         source_code = requests.get(self.url).text
#         soup = BeautifulSoup(source_code, "html.parser")
#
#         # get img url
#         img = soup.findAll("img")[2]["src"]
#
#         if img.startswith(r"//img.sbazar.cz"):
#             img_url = "https:" + img
#         else:
#             img_url = "https://www.sbazar.cz/img/logo-sbazar.png"
#         data["img_url"] = img_url
#
#         # get title
#         title = str(soup.title.string)
#         data["title"] = title
#
#         # get price
#         try:
#             price = str(soup.find("span", itemprop="price").contents[0])
#         except IndexError:
#             price = "cena neuvedena"
#             pass
#         data["price"] = price
#
#         # get user
#         try:
#             user = soup.find("dd", itemprop="familyName").contents[0].string
#             user = user.lower()
#
#         except IndexError:
#             user = "anonymní uživatel"
#             # print("nema uzivatele")
#             pass
#         data["user"] = user
#
#         # get words
#         try:
#             body = soup.find("span", itemprop="description").contents[0]
#
#         except IndexError:
#             body = "inzerát bez textu"
#             # print("nemá text")
#             pass
#
#         title_body = title + " " + body
#         title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
#         words_set = set(title_body.lower().split())
#         data["words_set"] = words_set
#
#         return data
#
#     def __repr__(self):
#         return f"crawler class for url: {self.url}"


def get_data_sbazar(link):
    data = {}
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    # get img url
    img = soup.findAll("img")[2]["src"]

    if img.startswith(r"//img.sbazar.cz"):
        img_url = "https:" + img
    else:
        img_url = "https://www.sbazar.cz/img/logo-sbazar.png"
    data["img_url"] = img_url

    # get title
    title = str(soup.title.string)
    data["title"] = title

    # get price
    try:
        price = str(soup.find("span", itemprop="price").contents[0])
    except IndexError:
        price = "cena neuvedena"
        pass
    data["price"] = price

    # get user
    try:
        user = soup.find("dd", itemprop="familyName").contents[0].string
        user = user.lower()

    except IndexError:
        user = "anonymní uživatel"
        # print("nema uzivatele")
        pass
    data["user"] = user

    # get location
    location = soup.find("span",{"itemprop":"addressRegion"}).text
    data["location"] = str(location)
    # get words
    try:
        body = soup.find("span", itemprop="description").contents[0]

    except IndexError:
        body = "inzerát bez textu"
        # print("nemá text")
        pass

    title_body = title + " " + body
    # print(title_body)
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    words_set = set(title_body.lower().split())
    data["words_set"] = words_set

    return data


def get_data_bazos(link):
    data = {}
    source_code = requests.get(link).text
    soup = BeautifulSoup(source_code, "html.parser")

    # get img url
    img = soup.findAll("img")[1]["src"]
    if img.startswith("https://www.bazos.cz/img"):
        img_url = img.split("?t=")[0]
    else:
        img_url = "https://www.bazos.cz/obrazky/bazos.gif"

    data["img_url"] = img_url

    # get title
    title_string = str(soup.title.string)
    data["title"] = title_string

    # title_split = str(title)
    # title_split = title_split.replace("<br>", "").replace("<br/>", "").replace("\\r", "").replace("\\n", "")
    # title_split = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_split)
    # title_set = set(title_split.lower().split())

    # get user
    tabulka = soup.find("table", cellspacing=1).find_next("td").find_next_sibling("td")
    user = tabulka.find_next("b").string
    user = user.lower()
    data["user"] = user

    # get price
    price = str(tabulka.find_next("b").find_next("b").string)
    data["price"] = price

    # get location
    location = soup.findAll("a", {"rel": "nofollow"})[2].text
    data["location"] = str(location)

    # get words
    body_list = soup.find("div", {"class": "popis"}).contents
    body_string = " ".join(str(i) for i in body_list)
    body_string = body_string + title_string
    body_string = body_string.replace("<br>", "").replace("<br/>", "").replace("</br>", "").replace("\\r", "").replace("\\n", "")
    body_string = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', body_string)
    words_set = set(body_string.lower().split())

    data["words_set"] = words_set

    return data


# def get_image_from_url(img_url):
#     img_name = img_url.split("/")[-1]
#     img_path = r"crawler_files/" + img_name
#     urllib.request.urlretrieve(img_url, img_path)
#     return img_path


def get_image_from_url(url):
    img_name = url.split("/")[-1]
    img_path = r"crawler_files/" + img_name
    urllib.request.urlretrieve(url, img_path)

    # resize image
    base_h = 100
    img = Image.open(img_path)

    h_percent = (base_h / float(img.size[1]))
    w_size = int((float(img.size[0]) * float(h_percent)))

    img = img.resize((w_size, base_h), Image.ANTIALIAS)
    img.save(img_path)

    return img_path


if __name__ == "__main__":
    img_url = 'https://www.bazos.cz/img/1/679/86706679.jpg'
    print(get_image_from_url(img_url))

    # link = "https://nabytek.bazos.cz/inzerat/86706679/kuchynske-zidle.php"
    # print(get_data_bazos(link))