import os
import time
import logging
from database import create_database
from sql_alchemy_tables import write_tables_to_db


def delete_database_file():
    path = r"crawler_files/"
    database = os.path.join(path, r"sqlite_database.db")
    os.remove(database)


def create_database_file():
    path = r"crawler_files/"
    database = os.path.join(path, r"sqlite_database.db")

    if not os.path.exists(path):
        os.makedirs(path)
        print("Vytvořena složka " + path)

    if not os.path.isfile(database):
        create_database()
        write_tables_to_db()


def write_file(file_name, data):
    f = open(file_name, "w", encoding="ISO-8859-1")
    f.write(data)
    f.close()


def append_to_file(file_name, data):
    with open(file_name, "a", encoding="UTF-8") as f:
        f.write(data + "\n")


def delete_file_content(file_name):
    with open(file_name, "w"):
        pass


def file_to_list(file_name):
    results = []
    with open(file_name, "rt", encoding="utf-8-sig") as f:
        for line in f:
            results.append(line.replace("\n", ""))
    return results


def set_to_file_del(file_name, data):
    delete_file_content(file_name)
    for line in data:
        append_to_file(file_name, line)


def set_to_file(file_name, data):
    for line in data:
        append_to_file(file_name, line)


def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('logging_file.log')

    # create a logging format
    formatter = logging.Formatter('%(asctime)s ; %(name)s ; %(levelname)s ; %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


def start_logger(name):
    logger = setup_logger(name)
    timer = time.time()

    return logger, timer


def stop_logger(logger, timer):
    end = time.time()
    end_time = str(end - timer)
    print(end_time)
    logger.info(f"crawler ended in {end_time}")


if __name__ == "__main__":
    pass
