from main import start
from general import setup_logger
from collections import namedtuple

import time

logger = setup_logger("start")
timer = time.time()

project_list = []

searched_links = namedtuple("searched_links", "url, type")
url_list_sbazar = [r"524-jidelni-stoly-zidle", r"300-kresla", r"219-starozitny-nabytek"]
url_list_bazos_nabytek = ["nabytek.bazos.cz/kresla", "nabytek.bazos.cz/zidle"]
url_list_bazos_ostatni = ["ostatni.bazos.cz"]

for i in url_list_sbazar:
    project_list.append(searched_links(url=i, type="sbazar"))

for i in url_list_bazos_nabytek:
    project_list.append(searched_links(url=i, type="bazos_nabytek"))

for i in url_list_bazos_ostatni:
    project_list.append(searched_links(url=i, type="bazos_ostatni"))

for page_tuple in project_list:
    start(page_tuple)


end = time.time()
end_time = str(end - timer)
print(end_time)
logger.info("crawler ended in ; " + end_time)
