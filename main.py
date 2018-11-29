from general import *
from get_data import get_data_bazos, get_data_sbazar
from get_links import get_links_bazos, get_links_sbazar
from send_mail import send_mail
from sql_query import query_link, query_wordlist, query_stopwords, query_stopuser
from sql_inserts import insert_link_list


def search_links(url):
    stopword_set = set(query_stopwords())
    keyword_set = set(query_wordlist())
    new_links_list = []
    if url.type == "sbazar":
        queue_list = get_links_sbazar(url.url)
    else:
        queue_list = get_links_bazos(url.url)

    for link in queue_list:
        print("kontroluju", link)

        if not query_link(link, url.type):
            new_links_list.append(link)

            print("prochazim", link)
            if url.type == "sbazar":
                data = get_data_sbazar(link)
            else:
                data = get_data_bazos(link)
            compare_words(data, link, stopword_set, keyword_set)

        else:
            continue
    insert_link_list(new_links_list, url.type)


def compare_words(data, link, stopword_set, keyword_set):
    if query_stopuser(data["user"]):
        pass
    elif stopword_set.intersection(data["words_set"]):
        pass

    elif keyword_set.intersection(data["words_set"]):
        result = set.intersection(keyword_set, data["words_set"])
        send_mail(result, data, link)
        # print("test email odesilan")
        # print("data py- result", result)
        # print("data - title ", data["title"])
        # print(f"data - link: {link}, price: {data['price']}, img: {data['img_url']}, location: {data['location']}")
    else:
        pass


def start(project):
    create_project_dir()
    search_links(project)


if __name__ == "__main__":
    project_list_bazos = ["nabytek.bazos.cz/kresla", "nabytek.bazos.cz/zidle", "ostatni.bazos.cz"]
    page = [r"300-kresla"]
    for i in page:
        print("testuju", i)
        print(get_links_sbazar(i))
        # start(i)
