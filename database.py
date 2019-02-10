import sqlite3


def create_database():
    links_table = """ CREATE TABLE IF NOT EXISTS Links_table (
                                        id integer PRIMARY KEY,
                                        link text
                                        website text
                                    ); """

    wordlist_table = """ CREATE TABLE IF NOT EXISTS Keywords (
                                        keywords text
                                    ); """

    stop_user_list = """ CREATE TABLE IF NOT EXISTS Stopusers (
                                        stopusers text
                                    ); """

    stop_words_list = """ CREATE TABLE IF NOT EXISTS Stopwords (
                                        stopwords text
                                    ); """
    conn = create_connection()
    # c = conn.cursor()
    # c.execute(links_table)
    # c.execute(wordlist_table)
    # c.execute(stop_user_list)
    # c.execute(stop_words_list)
    print("DB created")


def create_connection():
    db_file = r"crawler_files/sqlite_database.db"
    conn = sqlite3.connect(db_file)
    return conn


def insert_links_to_db(link_list):
    conn = create_connection()
    cursor = conn.cursor()
    for item in link_list:
        cursor.execute('INSERT INTO Links(link) values (?)', (item,))
    conn.commit()
    print("nové hromadné záznamy uloženy do databáze")


def insert_link_to_db(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Links(link) values (?)', (data,))
    conn.commit()
    print('nový link uložen do databáze -', data)


def select_link_from_db(check_link):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM Links WHERE link = ?', (check_link,))

    data = cursor.fetchone()[0]
    if data == 0:
        send_back = True
        insert_link_to_db(check_link)
    else:
        send_back = False
    return send_back


def select_stopuser(user):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM Stopusers WHERE stopusers = ?', (user,))

    data = cursor.fetchone()[0]
    if data == 0:
        send_back = True
    else:
        send_back = False
    return send_back


def select_stopwords():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Stopwords')

    data = cursor.fetchall()
    item_list = []
    for item in data:
        item_list.append(item[0])

    return item_list


def select_wordlist():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Keywords')

    data = cursor.fetchall()
    item_list = []
    for item in data:
        item_list.append(item[0])

    return item_list
