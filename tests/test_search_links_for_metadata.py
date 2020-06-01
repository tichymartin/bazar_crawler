from .test_data_file import links_dict
from main import get_links_from_website, search_links_for_metadata

new_links = {
    'sbazar': [
        'https://www.sbazar.cz/restauratorskadilna/detail/60438637-kresla-typu-l-a-bernkop-30-leta-20-stoleti', ],
    'bazos': ['https://ostatni.bazos.cz/inzerat/100659150/MARIA-Matka-dobre-rady-modlitebni-knizka-r-1887.php', ],
    'letgo': ['https://www.letgo.cz/item/jidelni-zidle-iid-14280855', ],
    'annonce': ['https://www.annonce.cz/inzerat/kreslo-ikea-43715465-w1hncg.html', ]
}

data_to_compare_with_sets = search_links_for_metadata(new_links)

for data in data_to_compare_with_sets:
    print()
    for info in data:
        print(f"{info}: {data[info]}")
