from get_data import get_data_bazos, get_data_sbazar, get_data_letgo
from get_links import get_links_bazos, get_links_sbazar, get_links_letgo
from sql_query import query_link, query_stopuser
from sql_inserts import insert_link_list


def get_links_from_website(links_dict):
    new_links_dict = {}
    for website in links_dict:
        if website == "sbazar":
            new_links_dict["sbazar"] = []
            for link in links_dict[website]:
                new_links_dict["sbazar"].extend(get_links_sbazar(link))
        elif website == "bazos":
            new_links_dict["bazos"] = []
            for link in links_dict[website]:
                new_links_dict["bazos"].extend(get_links_bazos(link))
        elif website == "letgo":
            new_links_dict["letgo"] = []
            for link in links_dict[website]:
                new_links_dict["letgo"].extend(get_links_letgo(link))

    return new_links_dict


def check_links_in_database(new_links_dict):
    links_to_check = {}
    for website in new_links_dict:
        links_to_check[website] = []
        for link in new_links_dict[website]:
            # print("kontroluju", link)
            if not query_link(link, website):
                links_to_check[website].append(link)

    return links_to_check


def insert_new_links_into_database(new_links_dict):
    for website in new_links_dict:
        insert_link_list(new_links_dict[website], website)


def search_links_for_metadata(links_to_check):
    data_to_compare_with_sets = []
    for website in links_to_check:

        if website == "sbazar":
            for link in links_to_check[website]:
                metadata = get_data_sbazar(link)
                data_to_compare_with_sets.append(metadata)

        if website == "bazos":
            for link in links_to_check[website]:
                metadata = get_data_bazos(link)
                data_to_compare_with_sets.append(metadata)

        if website == "letgo":
            for link in links_to_check[website]:
                metadata = get_data_letgo(link)
                data_to_compare_with_sets.append(metadata)

    return data_to_compare_with_sets


def compare_keywords(metadata, stopwords_set, keywords_set):
    data_to_send = []
    for single_data in metadata:

        if query_stopuser(single_data["user"]):
            continue

        elif stopwords_set.intersection(single_data["words_set"]):
            continue

        elif keywords_set.intersection(single_data["words_set"]):
            single_data["keywords"] = set.intersection(keywords_set, single_data["words_set"])
            data_to_send.append(single_data)

        else:
            continue

    return data_to_send


if __name__ == "__main__":
    data = [{
        'img_url': 'https://d46-a.sdn.szn.cz/d_46/c_img_G_j/Dp2CDMa.jpeg?fl=exf|crr,1.33333,2|res,1024,768,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1',
        'title': 'židle jídelní nové', 'price': '9\xa0000', 'user': 'pilasd', 'location': 'Polička',
        'words_set': {'jsou', 'všech', '120', 'je', 'příjemné', 'se', '1', 'pohodlné', 'nohama',
                      'vysouvací', 'koupené', 'hloubka', 'asko', 'stůl', '6', 'ks', 's', '17', 'prodám',
                      'a', '2019', 'pod', 'nevejdeme', '105cm', 'na', 'nové', 'ale', 'pouze', 'prodej',
                      'nosnost', 'v', 'šířka', 'sedu', 'jídelní', '48cm', 'velmi', '41cm', 'kg',
                      'výška', 'židle'},
        'link': 'https://www.sbazar.cz/pilasd/detail/64679352-zidle-jidelni-nove'}, {
        'img_url': 'https://d46-a.sdn.szn.cz/d_46/c_img_G_a/yp7Bp07.jpeg?fl=exf|crr,1.33333,2|res,1024,768,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1',
        'title': 'Otáčecí polohovatelná židle v super stavu', 'price': '1\xa0470', 'user': 'marela',
        'location': 'část obce Tábor',
        'words_set': {'pc', 'nastavitelnou', '3000kč', '0táčecí', 'funkční', 'výškou', 'nepoškozená',
                      'super', 'polohovatelná', 's', 'plně', 'stavu', 'židle', 'v', 'otáčecí'},
        'link': 'https://www.sbazar.cz/Marela/detail/40047982-otaceci-polohovatelna-zidle-v-super-stavu'},
        {'img_url': 'https://www.bazos.cz/img/1/054/100424054.jpg?t=1549633984', 'user': 'klára',
         'location': '130 00 Praha 3', 'price': '1 650 Kč', 'title': 'Otočné křeslo Leo bílé',
         'words_set': {'sedacím', 'je', 'přechází', 'ruce', 'opatřené', 'potah', 'pohodlné', 'osobní',
                       'obývacím', 's', 'stavitelné', 'ozdobné', 'viz', 'exkluzivní', 'barvy', 'knoflíčky',
                       'čalounění', 'známky', 'opěradlo', 'funkčnosti', 'užívání', 'foto', 'hodit',
                       'barevné', 've', 'noha', 'výškové', 'opěradla', 'leo', 'čalouněné', 'dvě',
                       'centrální', '3', 'a', 'pěkný', 'praha', 'nebo', 'syntetické', 'na', 'domácí',
                       'nosnost', 'vysokou', 'měkké', 'drobné', 'kg', 'až', 'otočné', 'opěrky', 'bude',
                       'jednací', 'odběr', 'křeslo', 'prošíváním', 'se', 'své', 'domácnosti', 'chromovaná',
                       'použití', 'pokoji', 'moderními', 'stane', 'pracovny', 'skvěle', 'nábytkem',
                       'univerzálním', 'straně', 'v', 'plynule', 'místnosti', 'kromě', 'díky', 'do',
                       'diamantovým', 'moderní', 'o', 'nastavitelnosti', '360°', 'ze', 'funkčností', 'kůže',
                       'stav', 'výškově', 'také', 'vaší', 'běžného', 'funkce', 'kovová', 'bílé', 'sedací',
                       'skvrnky', 'čalouněný', 'jídelně', 'nábytek', '136', 'nastavitelné', 'vnitřní'},
         'link': 'https://nabytek.bazos.cz/inzerat/100424054/Otocne-kreslo-Leo-bile.php'},
        {'img_url': 'https://www.bazos.cz/img/1/367/100299367.jpg?t=1549184700', 'user': 'marcela',
         'location': '602 00 Brno', 'price': '4 000 Kč',
         'title': 'Kvalitní proutěná křesla+stolek z přírodního ratanu',
         'words_set': {'možnost', 'i', 'za', 'proutěná', 'stojí', 'je', 'křeslo', 'jednání', 'křesla', '1',
                       'jako', 'kvalitní', 'polstrování', 'přírodního', 'slevy', 'z', 'soupravu', '4500',
                       'prodám', '605991249', 'kč', 'rychlém', 'mob', 'nové', 'zničené', 'ne', 'ceně', 'v',
                       'nejsou', 'sms', 'celou', '4000', 'stolek', 'nikde', 'ratanu', 'při'},
         'link': 'https://nabytek.bazos.cz/inzerat/100299367/Kvalitni-proutena-kreslastolek-z-prirodniho-ratanu.php'},
        {'img_url': 'https://www.bazos.cz/img/1/617/100553617.jpg', 'user': 'radek',
         'location': '533 41 Pardubice', 'price': '1 800 Kč',
         'title': 'Prodám celočalouněný ušák včetně taburetu',
         'words_set': {'x', 'celočalouněný', 've', '35', 'dobrém', 'stavu', 'včetně', 'nepotřebný', '58',
                       'kolečkách', '110', 'h', '95', 'prodám', 'již', 'na', 'taburet', 'ušák', '47', 'v',
                       'rekonstrukci', 'rozměry', 'čalounění', 'sedu', 'obojí', 'velmi', 'taburetu',
                       'neprodřené', 'cm', 'po', '76', 'výška', 'š'},
         'link': 'https://nabytek.bazos.cz/inzerat/100553617/Prodam-celocalouneny-usak-vcetne-taburetu.php'},
        {'img_url': 'https://www.maxrestaurantgroup.com/blog/wp-content/uploads/2014/08/rum-barrel-xxx.jpg',
         'user': 'alice', 'location': '603 00 Brno', 'price': '349 Kč', 'title': 'Ratanove kreslo',
         'words_set': {'stare', 'cena349', 'dva', 'roky', 'kc', 'prodam', 'kreslo', 'ratanove'},
         'link': 'https://nabytek.bazos.cz/inzerat/100552678/Ratanove-kreslo.php'},
        {'img_url': 'https://www.bazos.cz/img/1/345/100551345.jpg', 'user': 'jirásková',
         'location': '466 04 Jablonec nad Nisou', 'price': 'Zdarma', 'title': 'Gauč + křeslo',
         'words_set': {'za', 'stary', 'křeslo', 'odvoz', 'daruji', 'gauč'},
         'link': 'https://nabytek.bazos.cz/inzerat/100551345/Gauc--kreslo.php'},
        {'img_url': 'https://www.bazos.cz/img/1/635/100550635.jpg', 'user': 'linda',
         'location': '251 63 Praha - východ', 'price': '199 Kč', 'title': 'Retro zelená kožená lavice',
         'words_set': {'lavici', 'úložným', 've', 'odběr', 'lavice', 'koženou', 'zelená', 'hloubka',
                       'strančicích', 'praze', 'osobní', 's', 'prostorem', 'prodám', '52cm', 'na', '83cm',
                       'pouze', 'retro', 'rozměry', 'šířka', 'východ', '70cm', 'zelenou', 'výška',
                       'kožená'},
         'link': 'https://nabytek.bazos.cz/inzerat/100550635/Retro-zelena-kozena-lavice.php'},
        {'img_url': 'https://www.bazos.cz/img/1/216/100550216.jpg', 'user': 'soňa',
         'location': '170 00 Praha 7', 'price': '800 Kč',
         'title': 'Prvorepubliková klubová křesílka původní stav á 800',
         'words_set': {'800', 'odběr', 'za', 'kus', '7', 'pár', 'přečalounit', 'původní', 'dohodě', 'stavu',
                       'klubová', 'konstrukčně', 'jen', 'službou', 'jako', 'doporučuji', 'pošlu', '1600',
                       'věkem', 'stav', 'osobní', 'prvorepubliková', 'zachovalém', 'kč', 'pružiny', 'avšak',
                       'nabízím', 'praha', 'nebo', 'již', '/', 'cena', 'přepravní', 'vyšisované',
                       'křesílka', 'v', 'čalounění', 'á', 'pořádku', 'pevné', 'po', 'nepotrhané',
                       'původním', 'neprosezené'},
         'link': 'https://nabytek.bazos.cz/inzerat/100550216/Prvorepublikova-klubova-kresilka-puvodni-stav-a-800.php'},
        {'img_url': 'https://www.bazos.cz/img/1/532/100548532.jpg', 'user': 'gabriel',
         'location': '671 03 Znojmo', 'price': '1 500 Kč', 'title': 'Čalouněné křeslo 2x, starožitné',
         'words_set': {'čalouněné', 'skvělý', 'starožitné', 'křeslo', 'stav', '2x'},
         'link': 'https://nabytek.bazos.cz/inzerat/100548532/Calounene-kreslo-2x-starozitne.php'},
        {'img_url': 'https://www.bazos.cz/img/1/086/100547086.jpg?t=1549661662', 'user': 'karel',
         'location': '251 01 Praha - východ', 'price': '3 000 Kč', 'title': 'Rozkládací pohovka',
         'words_set': {'180x95', 'eko', 'originál', 'nábytku', 'je', '3000', 'kus', 'se', 'původní',
                       'koupě', 'jen', 'novou', 'rozkládací', 'dvě', 'říčan', 'unáhlená', 'krabici', 'u',
                       'osobní', 'prodám', 'jsme', 'pohovku', 'nehodí', 'cena', 'dalšímu', 'viz', 'koženka',
                       'nám', 'velikost', 'lůžka', 'v', 'čalounění', '5000', 'zabalená', 'černá', 'pohovka',
                       'předání', 'strašín', 'rozloženého', 'teď', 'cm', 'k', 'foto', 'kupovali'},
         'link': 'https://nabytek.bazos.cz/inzerat/100547086/Rozkladaci-pohovka.php'},
        {'img_url': 'https://www.bazos.cz/img/1/891/100546891.jpg', 'user': 'kotoucek',
         'location': '391 11 Tábor', 'price': '2 000 Kč', 'title': 'lenoška ektorp',
         'words_set': {'ektorp', 'lenošku', 'série', 'ikea', 'prodám', 'lenoška'},
         'link': 'https://nabytek.bazos.cz/inzerat/100546891/lenoska-ektorp.php'}]

    for d in data:
        print(query_stopuser(d["user"]))
    # print(get_links_from_website(links_dict))
