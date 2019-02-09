import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_tables import Links_table
from general import file_to_list

db = 'sqlite:///crawler_files/sqlite_database.db'


# engine = create_engine('sqlite:///:memory:')


def insert_link(data):
    engine = create_engine(db)

    Session = sessionmaker(bind=engine)
    session = Session()

    # insert a item

    link = Links_table(link_url=data)

    # instead session.add you can use bulk_save_objects

    session.add(link)
    session.commit()
    print("ukládám do databáze", link.link_url)


def insert_link_list(link_list, website):
    engine = create_engine(db)

    Session = sessionmaker(bind=engine)
    session = Session()
    save_list = []
    # insert a item
    for item in link_list:
        save_list.append(Links_table(link=item, website=website))

    save_list = set(save_list)

    session.bulk_save_objects(save_list)
    session.commit()

#
# def insert_keywords_to_db():
#     file = r"text_files/keywords.txt"
#
#     if os.path.isfile(file):
#         k_list = file_to_list(file)
#     else:
#         k_list = []
#         print("Cannot find source file for import")
#
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     save_list = []
#     # insert a item
#     for item in k_list:
#         save_list.append(Keywords(keyword=item))
#
#     session.bulk_save_objects(save_list)
#     session.commit()
#
#
# def insert_stopwords_to_db():
#     file = r"text_files/stopwords.txt"
#
#     if os.path.isfile(file):
#         s_list = file_to_list(file)
#     else:
#         s_list = []
#         print("Cannot find source file for import")
#
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     save_list = []
#     # insert a item
#     for item in s_list:
#         save_list.append(Stopwords(stopword=item))
#
#     session.bulk_save_objects(save_list)
#     session.commit()
#
#
# def insert_stopusers_to_db():
#     file = r"text_files/stopusers.txt"
#
#     if os.path.isfile(file):
#         s_list = file_to_list(file)
#     else:
#         s_list = []
#         print("Cannot find source file for import")
#
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     save_list = []
#     # insert a item
#     for item in s_list:
#         save_list.append(Stopusers(stopuser=item))
#
#     session.bulk_save_objects(save_list)
#     session.commit()
#
#
# def insert_all_init():
#     insert_keywords_to_db()
#     insert_stopwords_to_db()
#     insert_stopusers_to_db()


if __name__ == "__main__":
    pass
