from requests_html import HTMLSession


def get_links_sbazar(url):
    session = HTMLSession()
    r = session.get(f"http://www.sbazar.cz/" + url)

    link_list = []
    tags = r.html.find("a.c-item__link")

    for tag in tags:
        link_list.append(list(tag.links)[0])

    return list(set(link_list))


def get_links_bazos(raw_url):
    link_list = []
    counter = 0

    url_base = raw_url.split("/", 1).pop(0)

    while True:
        if counter == 0:
            url = f"{raw_url}/"
        else:
            url = f"{raw_url}/{str(counter)}/"

        session = HTMLSession()
        r = session.get(f"https://{url}")

        # a_tags = r.html.find("span.nadpis a")
        links = r.html.find("div.inzeratynadpis a")

        for one_link in links:
            link = list(one_link.links)[0]
            if link.startswith("/inzerat/"):
                link_list.append(f"https://{url_base}{link}")

        top_tag = r.html.find(".ztop")
        if not top_tag:
            break

        counter += 20

    return list(set(link_list))


def get_links_letgo(keyword):
    link_list = []
    url_base = f"https://www.letgo.cz/items/q-{keyword}?sorting=desc-creation"
    session = HTMLSession()
    r = session.get(url_base)
    all_links = r.html.links
    for link in all_links:
        if link.startswith("/item/"):
            link_list.append(f"https://www.letgo.cz{link}")

    return list(set(link_list))


def get_links_annonce(keyword):
    link_list = []
    url_base = f"https://www.annonce.cz/{keyword}$18.html?sort=ageasc&nabidkovy=1"
    session = HTMLSession()
    r = session.get(url_base)
    all_links = r.html.links
    for link in all_links:
        if link.startswith("/inzerat/"):
            link_list.append(f"https://www.annonce.cz{link}")

    return list(set(link_list))


def get_links_marketplace():
    link_list = []
    url_base = "https://www.facebook.com/marketplace/prague/furniture"

    session = HTMLSession()
    r = session.get(url_base)
    r.html.render()
    all_links = r.html.links
    for link in all_links:
        if "item" in link:
            link_list.append(f"https://www.facebook.com{link}")
            print(f"https://www.facebook.com{link}")

    return list(set(link_list))


if __name__ == '__main__':
    a = ("nabytek.bazos.cz/kresla", "nabytek.bazos.cz/zidle", "ostatni.bazos.cz",)
    for i in a:
        print(get_links_bazos(i))
