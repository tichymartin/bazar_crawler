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
        url = raw_url + "/" + str(counter) + "/"
        session = HTMLSession()
        r = session.get("https://" + url)

        a_tags = r.html.find("span.nadpis a")

        for tag in a_tags:
            link = list(tag.links)[0]
            link_list.append("https://" + url_base + link)

        top_tag = r.html.find(".ztop")
        if len(top_tag) == 0:
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


if __name__ == '__main__':

    print(get_links_letgo("židle"))
    # print(get_links_bazos("nabytek.bazos.cz/kresla"))
