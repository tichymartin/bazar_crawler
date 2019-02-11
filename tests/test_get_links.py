from tests.test_data_file import links_dict
from main import get_links_from_website

data_all = get_links_from_website(links_dict)

for data in data_all:
    for link in sorted(data_all[data]):
        print(link)

for data in data_all:
    print(data_all[data])
