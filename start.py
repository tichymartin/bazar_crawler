from main import get_links_from_website, check_links_in_database, insert_new_links_into_database, \
    search_links_for_metadata
from send_mail import send_mails
from general import start_logger, stop_logger
from data_file import servers_to_search
from one_link_process import link_process

if __name__ == '__main__':
    logger, timer = start_logger("start")

    new_links = get_links_from_website(servers_to_search)
    links_to_check = check_links_in_database(new_links)

    link_process(links_to_check)

    stop_logger(logger, timer)
