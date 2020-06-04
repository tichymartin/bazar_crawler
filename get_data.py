from requests_html import HTMLSession
import re
import urllib.request
from PIL import Image


def get_data_sbazar(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    data["link"] = link

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

    # data["location"] = r.html.find("a.atm-link", first=True).text
    "atm-link dava telefonni cislo"
    data["location"] = r.html.find("a.p-uw-item__link", first=True).text
    # print(data["location"])
    try:
        body = r.html.find("p.p-uw-item__description", first=True).text
    except AttributeError:
        body = ""

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    data["words_set"] = set(title_body.lower().split())
    data["website"] = "sbazar"

    return data


def get_data_bazos(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    data["link"] = link

    try:
        img = r.html.find("img.carousel-cell-image", first=True).attrs
        img_url = img["data-flickity-lazyload"]
    except AttributeError:
        img_url = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

    data["img_url"] = img_url

    tab = r.html.find("td.listadvlevo", first=True)
    texts = tab.text.split("\n")
    data["user"] = texts[3].lower()
    data["location"] = texts[13]
    data["price"] = texts[21]

    data["title"] = r.html.find("h1.nadpis", first=True).text

    body = r.html.find("div.popis", first=True).text

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    data["words_set"] = set(title_body.lower().split())
    data["website"] = "bazos"

    return data


def get_data_letgo(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    data["link"] = link

    try:
        img = r.html.find("._3v5bo img", first=True).attrs
        data["img_url"] = img["srcset"].split()[0]
    except AttributeError:
        data["img_url"] = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"
    except IndexError:
        data["img_url"] = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

    try:
        data["user"] = r.html.find(".hBaak", first=True).text
    except AttributeError:
        data["user"] = "Nezadané jméno"

    try:
        data["location"] = r.html.find("._2FRXm", first=True).text
    except AttributeError:
        data["location"] = "Nezadaná adresa"
    data["title"] = r.html.find("._3rJ6e", first=True).text
    data["price"] = r.html.find("._2xKfz", first=True).text
    try:
        body = r.html.find(".rui-2vHTl div p", first=True).text
    except AttributeError:
        body = ""

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    data["words_set"] = set(title_body.lower().split())
    data["website"] = "letgo"

    return data


def get_data_annonce(link):
    data = {}
    session = HTMLSession()
    r = session.get(link)

    data["link"] = link

    try:
        img = r.html.find(".carousel-detail", first=True).attrs
        data["img_url"] = f'https://www.annonce.cz{img["data-full"]}'
    except AttributeError:
        data["img_url"] = "https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg"

    try:
        user = r.html.find(".phone-link", first=True).attrs
        data["user"] = user["href"].lstrip("tel:")
    except AttributeError:
        data["user"] = "Není" \
                       ""
    # location = "table.attrs > tbody > tr > td > a"
    try:
        data["location"] = r.html.find("table.attrs > tbody > tr > td > a")[-1].text

    except AttributeError:
        data["location"] = "Není"

    except IndexError:
        data["location"] = "Není"

    data["title"] = r.html.find(".d2-fullwidth", first=True).text

    try:
        data["price"] = r.html.find(".price-row td", first=True).text
    except AttributeError:
        data["price"] = "Není"

    try:
        body = r.html.find(".ad-desc", first=True).text
    except AttributeError:
        body = ""

    title_body = data["title"] + " " + body
    title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    data["words_set"] = set(title_body.lower().split())
    data["website"] = "annonce"

    return data


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


if __name__ == "__main__":
    # annonce_link = "https://www.annonce.cz/inzerat/-2-x-kresla-starsi--43704808-wtpk4n.html"
    #
    # print(get_data_annonce(annonce_link))

    letgolink = "https://www.letgo.cz/item/zidle-starozitna-iid-14639209"
    bazoslink = "https://ostatni.bazos.cz/inzerat/120926672/parova-polokresla-thonet-mundus-b3.php"
    sbazarlink = "https://www.sbazar.cz/martin.tolnay/detail/113051516-starozitna-zidle-thonet-nr-a-238-schneck"
    # sbazarlink = "https://www.sbazar.cz/ateliervidenska/detail/113576301--1430-znackove-zidle-ton-o-heardtl-4x"
    # print(get_data_bazos(bazoslink))
    test_data = get_data_bazos(bazoslink)
    for headr, data in test_data.items():
        print(f"{headr}: {data}")

    sbazar_metadata = {
        'link': 'https://www.sbazar.cz/martin.tolnay/detail/113051516-starozitna-zidle-thonet-nr-a-238-schneck',
        'img_url': 'https://d46-a.sdn.cz/d_46/c_img_gU_E/gOtGHu.jpeg?fl=exf|crr,1.33333,2|res,1024,768,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1',
        'title': 'starožitná židle THONET Nr. A 238 Schneck', 'price': '3\xa0949', 'user': 'martin tolnay',
        'location': 'Jedovnice',
        'words_set': {'zaslání', 'přeleštěno', 'šelakem', 'povrchu', '238', 'doprava', 'roce', 'starožitná', '1928',
                      'pořádku', 'renovaci', 'kurýrem', 'adolf', 'schneck', 'původní', 'kterou', 'patinou', 'opěrky',
                      'a',
                      'nr', 'model', 'gustav', 'sedáku', 'nálepka', 'výplet', 'nebo', 'dostupný', 'dřeva', 'po',
                      'stavu',
                      'málo', 'osobní', 'mírně', 'židle', 'thonet', 'v', 'zajímavý', 'převzetí', 'dubového', 'lakování',
                      'pěkném', 'pevná', 'poškozen', 's', 'navrhl', 'konstrukce', 'architekt', 'lehké', 'značky',
                      'černé',
                      'imitací'}, 'website': 'sbazar'}
