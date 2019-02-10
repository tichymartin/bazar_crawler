from get_data import get_data_bazos, get_data_sbazar, get_data_letgo
from get_links import get_links_bazos, get_links_sbazar, get_links_letgo
from sql_alchemy_query import query_link
from sql_alchemy_inserts import insert_link_list
from links import stopusers_set, stopwords_set, keywords_set


def get_links_from_website(links_dict):
    new_links_dict = {}
    for website in links_dict:
        if website == "sbazar":
            new_links_dict["sbazar"] = []

            for link in links_dict[website]:
                new_links_dict["sbazar"].extend(get_links_sbazar(link))

            new_links_dict["sbazar"] = list(set(new_links_dict["sbazar"]))

        elif website == "bazos":
            new_links_dict["bazos"] = []

            for link in links_dict[website]:
                new_links_dict["bazos"].extend(get_links_bazos(link))

            new_links_dict["bazos"] = list(set(new_links_dict["bazos"]))

        elif website == "letgo":
            new_links_dict["letgo"] = []

            for link in links_dict[website]:
                new_links_dict["letgo"].extend(get_links_letgo(link))

            new_links_dict["letgo"] = list(set(new_links_dict["letgo"]))



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


def compare_keywords(metadata):
    data_to_send = []
    for single_data in metadata:
        user = set()
        user.add(single_data['user'])

        if stopusers_set.intersection(user):
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
    data = [
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/ua33k9yh30xs2-LETCZ/image;s=280x0;q=20',
         'user': 'Juan Don Alberto', 'location': 'Hrabůvka, Ostrava, Moravskoslezský kraj',
         'title': 'Počítačový stolek + křeslo', 'price': '1\xa0000Kč',
         'words_set': {'prodávám', 'ušák', 'křeslo', 'stolek', 'výškově', 'moc', 's', 'stavitelný', 'stav', 'pultem',
                       'počítačovy', 'křeslem', 'dobrý', 'stůl', 'nevyužit', 'koženka', 'výsuvným', 'počítačový'},
         'link': 'https://www.letgo.cz/item/pocitacovy-stolek-kreslo-iid-14237325'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/d12xeei7kf6c3-LETCZ/image;s=280x0;q=20',
         'user': 'danielilusak26', 'location': 'Ostrov, Ostrov, Karlovarský kraj', 'title': 'Křeslo', 'price': '700Kč',
         'words_set': {'křeslo', 'top', 'prodam', 'stav', 'malo', 'používané'},
         'link': 'https://www.letgo.cz/item/kreslo-iid-14237321'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/poc6th9i5xy31-LETCZ/image;s=280x0;q=60',
         'user': 'Vladislav', 'location': 'Žižkov, Praha 3, Hlavní město Praha', 'title': 'Křeslo IKEA',
         'price': '2\xa0800Kč', 'words_set': {'křeslo', 'béžová', 'ikea', 'tmavě', 'barva'},
         'link': 'https://www.letgo.cz/item/kreslo-ikea-iid-14229618'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/3vpwktr4xg112-LETCZ/image;s=280x0;q=60',
         'user': 'jarinka', 'location': 'Slezská Ostrava, Ostrava, Moravskoslezský kraj',
         'title': 'Podnožka ke křeslu POANG IKEA', 'price': '390Kč',
         'words_set': {'dokonalé', 'stav', 'super', 'ikea', 'křeslu', 'ke', 'poang', 'pro', 'pohodlí', 'podnožka'},
         'link': 'https://www.letgo.cz/item/podnozka-ke-kreslu-poang-ikea-iid-14236109'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/wqjmrniqbtcv-LETCZ/image;s=280x0;q=20',
         'user': 'kikinica1', 'location': 'Opava, Opava, Moravskoslezský kraj', 'title': 'Křeslo', 'price': '500Kč',
         'words_set': {'křeslo', 'hezké', 'staré', 'použitelné', 'ale', 'a'},
         'link': 'https://www.letgo.cz/item/kreslo-iid-14230451'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/r82h9sy4i8bg1-LETCZ/image;s=280x0;q=20',
         'user': 'juliankav', 'location': 'Chvalovice, Chvalovice, Jihomoravský kraj', 'title': 'Ratanove křeslo',
         'price': '500Kč', 'words_set': {'křeslo', 'ratanove'},
         'link': 'https://www.letgo.cz/item/ratanove-kreslo-iid-14233811'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/ai9d21lwq1zh1-LETCZ/image;s=280x0;q=60',
         'user': 'Karel Nivak', 'location': 'Staré Město, Praha 1, Hlavní město Praha',
         'title': 'Profesionální tatérské křeslo', 'price': '3\xa0289Kč',
         'words_set': {'standardním', '130kg', 'křeslo', 'osobní', 'profesionální', 'polohy', 'vyzkoušené', 'je',
                       'prodám', 'unese', 'ocelový', 'do', 'tatérské', 'rám', 'černá', 'předání', 'oproti', 'variant',
                       'několik', 'i', 'v', 'praze', 'kůže', 'nastavení', '100kg', 'zátěže', 'má', 'a'},
         'link': 'https://www.letgo.cz/item/profesionalni-taterske-kreslo-iid-14236790'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/jwesgrn1picd2-LETCZ/image;s=280x0;q=20',
         'user': 'jarinka', 'location': 'Slezská Ostrava, Ostrava, Moravskoslezský kraj', 'title': 'Křeslo IKEA POANG',
         'price': '890Kč', 'words_set': {'křeslo', 'ikea', 'z', 'poang', 'potah', 'ohýbaného', 'světlého', 'dřeva'},
         'link': 'https://www.letgo.cz/item/kreslo-ikea-poang-iid-14236093'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/pw4hj3xr7fnq-LETCZ/image;s=280x0;q=60',
         'user': 'asemra84', 'location': 'Teplice, Teplice, Ústecký kraj', 'title': 'Masážní křeslo Casada',
         'price': '8\xa0000Kč',
         'words_set': {'křeslo', 'jde', 'masážní', 'masírovat', 'je', 'módy', 'prodám', 'nastavit', 'vibrační', 'od',
                       'časovač', 'po', 'si', 'intenzitu', 'z', 'krku', 'až', 'casada', 'kůže', 'také', 'lýtka',
                       'umělé', 'možnost', 'lze', 'slevy', 'a'},
         'link': 'https://www.letgo.cz/item/masazni-kreslo-casada-iid-14229667'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/05qxnx5q71r51-LETCZ/image;s=280x0;q=20',
         'user': 'rybova', 'location': 'Libuš, Praha 12, Hlavní město Praha',
         'title': 'Relaxační a polohovatelné křeslo nejen pro seniory', 'price': '5\xa0900Kč',
         'words_set': {'křeslo', 'výborném', 'prostoru', 'polohovatelné', 'k', 'malému', 'pro', 'kč', 'dobře', 'stavu',
                       'nejen', 'seniory', 'pc', 'nešlo', 'relaxační', 'potah', 'vzhledem', 've', 'nafotit', 'byla',
                       'a', '12000'},
         'link': 'https://www.letgo.cz/item/relaxacni-a-polohovatelne-kreslo-nejen-pro-seniory-iid-14230072'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/67enyvqtdahf3-LETCZ/image;s=280x0;q=20',
         'user': 'Petr Kubík', 'location': 'Frýdek, Frýdek-Místek, Moravskoslezský kraj',
         'title': 'Prodám PC stůl rohový + křeslo', 'price': '650Kč',
         'words_set': {'prodám', 'smazání', 'křeslo', 'rohový', 'cena', '650', 'za', 'pc', 'celek', 'do', 'pevná',
                       'platí', 'je', 'stůl', 'inzerátu', 'kč'},
         'link': 'https://www.letgo.cz/item/prodam-pc-stul-rohovy-kreslo-iid-14235797'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/qzjj1un85csj1-LETCZ/image;s=280x0;q=60',
         'user': 'Beranová Patinka', 'location': 'Řepy, Praha 17, Hlavní město Praha', 'title': 'Oranžové křeslo',
         'price': '150Kč', 'words_set': {'oranžové', 'křeslo'},
         'link': 'https://www.letgo.cz/item/oranzove-kreslo-iid-14234511'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/7quh0gbuw2hs1-LETCZ/image;s=280x0;q=60',
         'user': 'Markéta Ciglerová', 'location': 'Mladá Boleslav IV, Mladá Boleslav, Středočeský kraj',
         'title': 'Staré masivní křeslo', 'price': '1\xa0000Kč',
         'words_set': {'prodám', 'křeslo', 'viz', 'staré', 'masivní', 'foto'},
         'link': 'https://www.letgo.cz/item/stare-masivni-kreslo-iid-14232766'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/nd29c6m7rt1u2-LETCZ/image;s=280x0;q=20',
         'user': 'Ludmila Dvořáková', 'location': 'Trojanovice, Trojanovice, Moravskoslezský kraj',
         'title': 'Starožitná pohovka a 2 křesla', 'price': '6\xa0000Kč',
         'words_set': {'prodám', 'výška', 'pohovky', '2', 'starožitnou', 'stav', 'délka', 'zachovalý', 'křesel',
                       'pohovku', 'přečalouněno', '60cm', 'starožitná', 'pohovka', 'šířka', 'cca', 'křesla', '85cm',
                       '130cm', 'a'}, 'link': 'https://www.letgo.cz/item/starozitna-pohovka-a-2-kresla-iid-14235578'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/t7we5sxqinm91-LETCZ/image;s=280x0;q=60',
         'user': 'hrpavlus', 'location': 'Liberec VI-Rochlice, Liberec, Liberecký kraj', 'title': 'Křeslo/ušák',
         'price': '2\xa0499Kč', 'words_set': {'ve', 'křeslo/ušák', 'křeslo', 'stylu', 'nabízím', 'ušák', 'scotty'},
         'link': 'https://www.letgo.cz/item/kreslousak-iid-14237534'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/4mfa828ilp511-LETCZ/image;s=280x0;q=60',
         'user': 'Interior', 'location': 'Teplice, Teplice, Ústecký kraj', 'title': 'Nádherné zámecké křeslo ušák šedé',
         'price': '5\xa0200Kč',
         'words_set': {'antracitová', 'křeslo', 'prostorné', 'velmi', 'nevyužívané', 'šedé', 'barva', 'obrovské', 'pc',
                       'téměř', '8500', 'zaslat', 'cupido', 'vysoké', 'zámecké', 'pohodlné', 'krásný', 'dřevěné',
                       'ušák', 'nádherné', 'stav', 'lze', 'nohy', 'a'},
         'link': 'https://www.letgo.cz/item/nadherne-zamecke-kreslo-usak-sede-iid-14231143'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/w82xyh28tm4b-LETCZ/image;s=280x0;q=20',
         'user': 'Regina Beránková', 'location': 'Královo Pole, Brno, Jihomoravský kraj', 'title': 'Rozkládací křeslo',
         'price': '500Kč', 'words_set': {'o', 'rozkládací', 'křeslo', 'se', 'rozměrech', '95x80cm', 'jedná'},
         'link': 'https://www.letgo.cz/item/rozkladaci-kreslo-iid-14229083'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/ycb91r349fmf1-LETCZ/image;s=280x0;q=20',
         'user': 'Markéta Heroldová', 'location': 'Buštěhrad, Buštěhrad, Středočeský kraj',
         'title': 'Sedací souprava (sedačka, dvě křesla a stolek)', 'price': '1\xa0500Kč',
         'words_set': {'zachovalý', 'sedací', 'velmi', 'k', 'vlastní', '230', 'prodám', '80', 'souprava', 'konferenční',
                       'cca', 'křesla', 'odvoz', 'stolek', 'gauč', 'dvě', 'cm', 'starý', 'rozkládací', 'sedačka',
                       'němu', 'ale', 'a'},
         'link': 'https://www.letgo.cz/item/sedaci-souprava-sedacka-dve-kresla-a-stolek-iid-14231375'},
        {'img_url': 'https://apollo-ireland.akamaized.net:443/v1/files/pemev4wf1urm3-LETCZ/image;s=280x0;q=20',
         'user': 'Petr Kubík', 'location': 'Frýdek, Frýdek-Místek, Moravskoslezský kraj',
         'title': 'Prodám PC stůl + křeslo', 'price': '650Kč',
         'words_set': {'prodám', 'smazání', 'křeslo', '650', 'cena', 'za', 'pc', 'celek', 'do', 'pevná', 'platí', 'je',
                       'stůl', 'inzerátu', 'kč'},
         'link': 'https://www.letgo.cz/item/prodam-pc-stul-kreslo-iid-14235784'}
    ]

    for dat in compare_keywords(data):
        print(dat)
    # print(get_links_from_website(links_dict))
