from requests_html import HTMLSession
import re
import urllib.request
from PIL import Image


def get_data_sbazar(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    try:
        img = r.html.find("img.c-gallery__img", first=True).attrs
        data["img_url"] = "https:" + img["src"]
    except AttributeError:
        data["img_url"] = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

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
        img = r.html.find("img.carousel-cell-image", first=True).attrs
        img_url = img["data-flickity-lazyload"]
    except AttributeError:
        img_url = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

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


def tst_get_data_sbazar(link):

    session = HTMLSession()
    r = session.get(link)

    img = r.html.find("img.ob-c-gallery__img", first=True).attrs
    img_url = "https:" + img["src"]

    return img_url


def tst_get_data_bazos(link):

    session = HTMLSession()
    r = session.get(link)

    img = r.html.find("img.carousel-cell-image", first=True).attrs
    img_url = img["data-flickity-lazyload"]
    return img_url

    # return img_url

if __name__ == "__main__":
    # link = r'https://www.sbazar.cz/eliska.si/detail/26329154-stara-zehlicka'
    # data = get_data_sbazar(link)
    # print(data["img_url"])

    link_bazos = "https://dum.bazos.cz/inzerat/97654527/Koupim-posuvnou-branu.php"
    link = "https://www.sbazar.cz/ondra.kocan/detail/55719902-set-jidelni-zidle-skjern-550-za-kus"
    # print(get_data_sbazar("https://www.sbazar.cz/ondra.kocan/detail/55719902-set-jidelni-zidle-skjern-550-za-kus"))
    # print(tst_get_data_bazos(link_bazos))
    # print(get_data_bazos(link_bazos))
    get_image_from_url("https://www.bazos.cz/img/1/267/97666267.jpg?t=1543392999")
