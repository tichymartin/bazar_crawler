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

    body = r.html.find("div.popisdetail", first=True).text

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


def get_data_marketplace(link=None):
    if not link:
        link = "https://www.facebook.com/marketplace/item/748009305939357/"
        # link = "https://www.facebook.com/marketplace/item/212316809750738/"
    data = {}
    session = HTMLSession()
    r = session.get(link)
    r.html.render()

    data["link"] = link
    img = r.html.find("img.k4urcfbm.bixrwtb6.datstx6m", first=True).attrs
    # imgs = r.html.find("img")

    # for img in imgs:
    #     print(img)
    data["img_url"] = img["src"]
    # data["img_url"] = "Noneni"

    texts = r.html.find(".dati1w0a.qt6c0cv9")

    data["title"], data["price"], *_ = texts[0].text.splitlines()

    print(f"link je: {data['link']}")
    print(f"obrazek je: {data['img_url']}")
    print(f"titulek je: {data['title']}")
    print(f"cena je: {data['price']}")

    try:
        data["location"] = texts[1].text.splitlines()[3]
        data["body"] = texts[1].text.splitlines()[2]

    except:
        data["location"] = texts[1].text.splitlines()[1]
        data["body"] = texts[1].text.splitlines()[0]

    print(f"poloha: {data['location']}")
    print(f"body: {data['body']}")
    print("")

    # print(texts[1].text.splitlines()[3])

    #
    # data["price"] = r.html.find("b.c-price__price", first=True).text
    # # print(data["price"])
    #
    # data["user"] = r.html.find("a.c-seller-info__name", first=True).text.lower()
    # # print(data["user"])
    #
    # # data["location"] = r.html.find("a.atm-link", first=True).text
    # "atm-link dava telefonni cislo"
    # data["location"] = r.html.find("a.p-uw-item__link", first=True).text
    # # print(data["location"])
    # try:
    #     body = r.html.find("p.p-uw-item__description", first=True).text
    # except AttributeError:
    #     body = ""
    #
    # title_body = data["title"] + " " + body
    # title_body = re.sub(r'[.,"!\'–()\[\]*;:+-]', ' ', title_body)
    # data["words_set"] = set(title_body.lower().split())
    # data["website"] = "sbazar"
    #
    # return data


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
    letgolink = "https://www.letgo.cz/item/zidle-starozitna-iid-14639209"
    bazoslink = 'https://nabytek.bazos.cz/inzerat/126194877/sedacka-z-brousene-kuze.php'

    sbazarlink = "https://www.sbazar.cz/martin.tolnay/detail/113051516-starozitna-zidle-thonet-nr-a-238-schneck"

