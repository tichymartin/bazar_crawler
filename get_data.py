from requests_html import HTMLSession
import re
import urllib.request
from PIL import Image


def get_data_sbazar(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    try:
        img = r.html.find("img.ob-c-gallery__img", first=True).attrs
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
    data["link"] = link

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
    data["link"] = link

    return data


def get_data_letgo(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    try:
        img = r.html.find("._3v5bo img", first=True).attrs
        data["img_url"] = img["srcset"].split()[0]
    except AttributeError:
        data["img_url"] = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

    data["user"] = r.html.find(".hBaak", first=True).text
    data["location"] = r.html.find("._2FRXm", first=True).text
    data["title"] = r.html.find("._3rJ6e", first=True).text
    data["price"] = r.html.find("._2xKfz", first=True).text
    try:
        body = r.html.find(".rui-2vHTl div p", first=True).text
    except AttributeError:
        body = ""

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    data["words_set"] = set(title_body.lower().split())
    data["link"] = link
    print(data)


def get_image_from_url(url):
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


if __name__ == "__main__":
    letgo_list = ['https://www.letgo.cz/item/ikea-glenn-barova-zidle-iid-14236303',
                  'https://www.letgo.cz/item/vse-za-900kc-ikea-knihovna-regalovy-policovy-dil-psaci-stul-a-zidle-iid-14232380',
                  'https://www.letgo.cz/item/kuchynsky-stul-dve-zidle-iid-14233539',
                  'https://www.letgo.cz/item/jidelni-stul-4-zidle-iid-14233479',
                  'https://www.letgo.cz/item/stolickazidlicka-iid-14234917',
                  'https://www.letgo.cz/item/jidelni-zidle-iid-14234821',
                  'https://www.letgo.cz/item/kuchynske-zidle-ikea-iid-14233239',
                  'https://www.letgo.cz/item/stul-6-zidli-iid-14232786',
                  'https://www.letgo.cz/item/psaci-stul-a-zidle-iid-14236192',
                  'https://www.letgo.cz/item/barova-zidle-glenn-iid-14236419',
                  'https://www.letgo.cz/item/pohodlna-kozena-jidelni-zidle-ikea-iid-14235793',
                  'https://www.letgo.cz/item/kancelarska-zidle-iid-14232788',
                  'https://www.letgo.cz/item/drevene-calounene-zidle-2ks-iid-14232868',
                  'https://www.letgo.cz/item/toaletni-zidle-top-stav-iid-14233103',
                  'https://www.letgo.cz/item/zidle-ikea-franklin-63-cm-bila-iid-14234052',
                  'https://www.letgo.cz/item/jidelni-zidle-iid-14233463',
                  'https://www.letgo.cz/item/decka-plastova-zidle-iid-14233150',
                  'https://www.letgo.cz/item/stul-a-zidle-za-odvoz-iid-14234149',
                  'https://www.letgo.cz/item/pc-zidle-iid-14235785']
    letgo_link_no_title = 'https://www.letgo.cz/item/zidle-iid-14234456'
    letgo_link = "https://www.letgo.cz/item/stul-6-zidli-iid-14232786"
    for l in letgo_list:
        get_data_letgo(l)
