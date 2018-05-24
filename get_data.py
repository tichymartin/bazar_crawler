from requests_html import HTMLSession
import re
import urllib.request
from PIL import Image


def get_data_sbazar(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    try:
        img = r.html.find("img.gallery-element-image", first=True).attrs
        data["img_url"] = "https:" + img["src"]
    except AttributeError:
        data["img_url"] = "https://rumratings-production.s3.amazonaws.com/uploads/brand/image/654/Plantation_XO_20th_Anniversary_rum.png"

    data["title"] = r.html.find("h1.p-uw-item__header", first=True).text
    # print(data["title"])

    data["price"] = r.html.find("b.c-price__price", first=True).text
    # print(data["price"])

    data["user"] = r.html.find("a.c-seller-info__name", first=True).text.lower()
    # print(data["user"])

    data["location"] = r.html.find("a.atm-link", first=True).text
    # print(data["location"])
    try:
        body = r.html.find("p.p-uw-item__description", first=True).text
    except AttributeError:
        body = ""

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    words_set = set(title_body.lower().split())
    data["words_set"] = words_set

    return data


def get_data_bazos(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    try:
        img = r.html.find("#bobrazek", first=True).attrs["src"]
        img_url = img.split("?t=")[0]
    except AttributeError:
        img_url = "https://rumratings-production.s3.amazonaws.com/uploads/brand/image/1052/Don_Papa_Rum.png"

    data["img_url"] = img_url

    tab = r.html.find("td.listadvlevo", first=True)
    texts = tab.text.split("\n")
    data["user"] = texts[4].lower()
    data["location"] = texts[9]
    data["price"] = texts[17]

    data["title"] = r.html.find("h1.nadpis", first=True).text

    body = r.html.find("div.popis", first=True).text

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    words_set = set(title_body.lower().split())
    data["words_set"] = words_set

    return data


def get_image_from_url(url):

    # img_name = url.split("/")[-1]
    # img_path = r"crawler_files/" + img_name
    # urllib.request.urlretrieve(url, img_path)

    img_path = r"crawler_files/temp.jpg"
    urllib.request.urlretrieve(url, img_path)

    # resize image
    base_h = 250
    img = Image.open(img_path)

    h_percent = (base_h / float(img.size[1]))
    w_size = int((float(img.size[0]) * float(h_percent)))

    img = img.resize((w_size, base_h), Image.ANTIALIAS)
    img.save(img_path)

    return img_path


if __name__ == "__main__":
    # link = r'https://www.sbazar.cz/eliska.si/detail/26329154-stara-zehlicka'
    # data = get_data_sbazar(link)
    # print(data["img_url"])
    # get_image_from_url(data["img_url"])


    link = "https://www.sbazar.cz/eliska.si/detail/26329154-stara-zehlicka"
    # print(get_data_bazos2(link))
    print(get_data_sbazar(link))
