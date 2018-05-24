from requests_html import HTMLSession


def get_links_sbazar(url):
    session = HTMLSession()
    r = session.get(f"http://www.sbazar.cz/" + url)

    link_list = []
    tags = r.html.find("a.c-item__link")

    for tag in tags:
        link_list.append(list(tag.links)[0])

    return link_list


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

    return link_list


# def get_links_bazos(url):
#     link_list = []
#     counter = 0
#     while True:
#
#         link_address = url.split("/", 1).pop(0)
#         link = "https://" + url + "/" + str(counter) + "/"
#         source_code = requests.get(link).text
#         soup = BeautifulSoup(source_code, "html.parser")
#
#         for line in soup.find_all("a"):
#             link = line.get("href").startswith("/inzerat")
#             if link is True:
#                 link_list.append("https://" + link_address + line.get("href"))
#
#         top = soup.findAll("span", {"class": "ztop"})
#         if len(top) == 0:
#             break
#         counter += 20
#
#     link_list = set(link_list)
#     return link_list