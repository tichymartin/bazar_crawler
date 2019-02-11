from tests.test_data_file import links_dict
from main import get_links_from_website, search_links_for_metadata

new_links = {
    # 'sbazar': [
    #     'https://www.sbazar.cz/restauratorskadilna/detail/60438637-kresla-typu-l-a-bernkop-30-leta-20-stoleti', ],
    # 'bazos': ['https://ostatni.bazos.cz/inzerat/100659150/MARIA-Matka-dobre-rady-modlitebni-knizka-r-1887.php', ],
    # 'letgo': ['https://www.letgo.cz/item/jidelni-zidle-iid-14280855', ],
    'annonce': ['https://www.annonce.cz/inzerat/kreslo-ikea-43715465-w1hncg.html',
                'https://www.annonce.cz/inzerat/kancelarska-zidle-43751505-w5axwy.html',
                'https://www.annonce.cz/inzerat/mensi-rozkl-pohovka-43659115-wdpn8z.html',
                'https://www.annonce.cz/inzerat/taburet-43749044-wgsrjg.html',
                'https://www.annonce.cz/inzerat/relaxacni-lehatko-lc4-43727128-w74n6n.html',
                'https://www.annonce.cz/inzerat/prodam-4x-kozene-zidle-43692452-whkfms.html',
                'https://www.annonce.cz/inzerat/dve-43689000-wsu8un.html',
                'https://www.annonce.cz/inzerat/chaise-longue-thonet-33387955-wfrvrn.html',
                'https://www.annonce.cz/inzerat/designove-cervene-lehatko-43716867-waqmxs.html',
                'https://www.annonce.cz/inzerat/kuchynskou-rohovou-soupravu-43553749-wbdgec.html',
                'https://www.annonce.cz/inzerat/kozena-sedaci-souprava-43071580-w1mxyp.html',
                'https://www.annonce.cz/inzerat/sedaci-soupravu-43694528-wshzp4.html',
                'https://www.annonce.cz/inzerat/-4ks-kuchynske-kovove-43748607-wwbeda.html',
                'https://www.annonce.cz/inzerat/prodej-jid-zidli-43688858-wpnubu.html',
                'https://www.annonce.cz/inzerat/zidle-43574685-w3y7ck.html',
                'https://www.annonce.cz/inzerat/otocna-zidle-cervena-43527601-wekgut.html',
                'https://www.annonce.cz/inzerat/-2-starsi-drevene-zidle-43078635-wj9vnh.html',
                'https://www.annonce.cz/inzerat/dve-nove-opravena-kresla-43746512-wfvc18.html',
                'https://www.annonce.cz/inzerat/kozenkovy-gauc-bezovy-43651384-wq3jr7.html',
                'https://www.annonce.cz/inzerat/-3-kancelarska-kresla-43694771-wwmuy9.html',
                'https://www.annonce.cz/inzerat/otocna-zidle-43628239-wxanrc.html',
                'https://www.annonce.cz/inzerat/proutena-kresla-zidle-43628101-wescaj.html',
                'https://www.annonce.cz/inzerat/zidle--300-kc-ks-43751719-w1c6t6.html',
                'https://www.annonce.cz/inzerat/levne-tv-kreslo-43694558-w5cm1q.html',
                'https://www.annonce.cz/inzerat/male-pekne-kreslo-zachovale-43748874-w1537q.html',
                'https://www.annonce.cz/inzerat/tri-zidle-43685401-wf23vg.html',
                'https://www.annonce.cz/inzerat/barovou-zidli-43480113-wpz8aq.html',
                'https://www.annonce.cz/inzerat/starozitna-zidle-43751373-wnkzqc.html',
                'https://www.annonce.cz/inzerat/levna-sofa-egon-43714389-wyd93f.html',
                'https://www.annonce.cz/inzerat/jidelni-zidle-43639759-w6bh7d.html',
                'https://www.annonce.cz/inzerat/-2-barove-rustikalni-zidle-43551839-wd6j57.html',
                'https://www.annonce.cz/inzerat/otocna-zidle-43573143-w1f2xf.html',
                'https://www.annonce.cz/inzerat/-2-x-kresla-starsi--43704808-wtpk4n.html',
                'https://www.annonce.cz/inzerat/luxusni-zidle-4ks-43639735-wudryb.html',
                'https://www.annonce.cz/inzerat/jidelni-zidle--nove-43746293-w9j9h7.html',
                'https://www.annonce.cz/inzerat/polohovaci-kreslo-43701790-wp8wg9.html',
                'https://www.annonce.cz/inzerat/zidle-43627896-w45sy9.html',
                'https://www.annonce.cz/inzerat/novou-rozkladaci-bilou-43595733-wdkjq1.html',
                'https://www.annonce.cz/inzerat/novy-gauc-43747255-w6wbvc.html',
                'https://www.annonce.cz/inzerat/sedaci-souprava-43725698-wf29br.html',
                'https://www.annonce.cz/inzerat/retro-kreslo--pekne-43716406-w53vn1.html',
                'https://www.annonce.cz/inzerat/masazni-kreslo-43691881-w71qhg.html',
                'https://www.annonce.cz/inzerat/rozkladaci-gauc-za-odvoz-43692590-w9avnx.html',
                'https://www.annonce.cz/inzerat/zachovaly-sedaci-vak-42865205-wk63rp.html',
                'https://www.annonce.cz/inzerat/kozene-kreslo-43695466-wwsgdc.html',
                'https://www.annonce.cz/inzerat/-8-elegantnich-zidli-43651414-w3sdes.html',
                'https://www.annonce.cz/inzerat/kreslo-jennylund-43738903-wq1p9v.html',
                'https://www.annonce.cz/inzerat/pohodlny-zanovni-gauc-43691071-wu1c7e.html',
                'https://www.annonce.cz/inzerat/originalni-barova-zidle-43615027-wtzjbh.html',
                'https://www.annonce.cz/inzerat/zidle-do-restaurace-43505049-wxshvc.html',
                'https://www.annonce.cz/inzerat/zidle-43ks-obrousene-43672571-wj5h7m.html',
                'https://www.annonce.cz/inzerat/hmeda-zidle-thonet-cena-43739254-wvsmqz.html',
                'https://www.annonce.cz/inzerat/otocne-kancelarske-kreslo-43725459-wdh6yb.html',
                'https://www.annonce.cz/inzerat/kancelarska-zidle-43622746-wrczr4.html',
                'https://www.annonce.cz/inzerat/bl-mes-vysoka-zidle-s-43596384-wp8hs8.html',
                'https://www.annonce.cz/inzerat/dve-otocne-calounene-42552359-wt4a5a.html']
}

data_to_compare_with_sets = search_links_for_metadata(new_links)

for data in data_to_compare_with_sets:
    print()
    for info in data:
        print(f"{info}: {data[info]}")
