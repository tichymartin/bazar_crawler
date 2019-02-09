from main import get_links_from_website, check_links_in_database, insert_new_links_into_database, \
    search_links_for_metadata, compare_keywords
from send_mail import send_mails
from general import start_logger, stop_logger
from links import links_dict

if __name__ == '__main__':
    logger, timer = start_logger("start")

    new_links = get_links_from_website(links_dict)
    links_to_check = check_links_in_database(new_links)
    insert_new_links_into_database(links_to_check)
    data_to_compare_with_sets = search_links_for_metadata(links_to_check)
    data_to_send = compare_keywords(data_to_compare_with_sets)
    send_mails(data_to_send, test=False)

    stop_logger(logger, timer)
