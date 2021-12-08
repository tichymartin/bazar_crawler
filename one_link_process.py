import traceback

from sql_alchemy_inserts import insert_link
from get_data import get_data_bazos, get_data_sbazar, get_data_annonce
from send_mail import send_mail_yagmail, send_error_yagmail
from config import TEST
from compare_keywords import compare_keywords_one_link

func_dict_get_data = {
    "sbazar": get_data_sbazar,
    "bazos": get_data_bazos,
    "annonce": get_data_annonce,
}


def link_process(link_dict):
    for website, link_list in link_dict.items():
        for link in link_list:
            insert_link(link, website)
            try:
                link_data = func_dict_get_data[website](link)
                check = compare_keywords_one_link(link_data)
                if check:
                    if TEST:
                        print(f'test - sending a mail with {link_data["link"]}')
                    else:
                        print(f'tohle neni test - sending a mail with {link_data["link"]}')
                        send_mail_yagmail(link_data)

            except:
                error_msg = {"subject": "traceback bazar crawler",
                             "body": traceback.print_exc()}
                send_error_yagmail(error_msg, flag=True)
