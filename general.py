import os
from database import *
import logging
from sql_tables import Links, Keywords, Stopwords, Stopusers, write_tables_to_db


def create_project_dir():
    path = r"crawler_files/"
    database = os.path.join(path, r"sqlite_database.db")

    if not os.path.exists(path):
        os.makedirs(path)
        print("Vytvořena složka " + path)

    if not os.path.isfile(database):
        # create_database()
        write_tables_to_db()


def insert_keywords_to_db(file):
    if os.path.isfile(file):
        keywords_list = file_to_list(file)

        conn = create_connection()
        cursor = conn.cursor()
        for item in keywords_list:
            cursor.execute('INSERT INTO Keywords(keywords) values (?)', (item,))
        conn.commit()
        print("keywords uloženy do databáze")


def insert_stopusers_to_db(file):
    if os.path.isfile(file):
        stopusers_list = file_to_list(file)

        conn = create_connection()
        cursor = conn.cursor()
        for item in stopusers_list:
            cursor.execute('INSERT INTO Stopusers(stopusers) values (?)', (item,))
        conn.commit()
        print("stopusers uloženy do databáze")


def insert_stopwords_to_db(file):
    if os.path.isfile(file):
        stopwords_list = file_to_list(file)

        conn = create_connection()
        cursor = conn.cursor()
        for item in stopwords_list:
            cursor.execute('INSERT INTO Stopwords(stopwords) values (?)', (item,))
        conn.commit()
        print("stopwords uloženy do databáze")


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
    handler = logging.FileHandler('crawler.log')

    # create a logging format
    formatter = logging.Formatter('%(asctime)s ; %(name)s ; %(levelname)s ; %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    file = r"text_files/stopusers.txt"
    file2 = r"text_files/stopusers2.txt"
    new = set(file_to_list(file))
    set_to_file_del(file, new)
