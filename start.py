from main import get_links_from_website, check_links_in_database, insert_new_links_into_database, \
    search_links_for_metadata, compare_keywords, insert_data_to_db
from send_mail import send_mails
from general import start_logger, stop_logger
from data_file import servers_to_search

if __name__ == '__main__':
    logger, timer = start_logger("start")

    new_links = get_links_from_website(servers_to_search)
    # print(new_links)
    links_to_check = check_links_in_database(new_links)
    insert_new_links_into_database(links_to_check)
    data_to_compare_with_sets = search_links_for_metadata(links_to_check)
    links_to_send_by_email, links_stopped_by_stop_users, links_stopped_by_stopwords = compare_keywords(
        data_to_compare_with_sets)

    send_mails(links_to_send_by_email)

    stop_logger(logger, timer)
