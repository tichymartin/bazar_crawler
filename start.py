from main import start
from general import setup_logger
import time


logger = setup_logger("start")
timer = time.time()

url_list_sbazar = [r"524-jidelni-stoly-zidle", r"300-kresla", r"219-starozitny-nabytek"]
url_list_bazos = ["nabytek.bazos.cz/kresla", "nabytek.bazos.cz/zidle", "ostatni.bazos.cz"]

project_list = url_list_bazos + url_list_sbazar


for page in project_list:
    start(page)

end = time.time()
end_time = str(end - timer)
print(end_time)
logger.info("crawler ended in ; " + end_time)