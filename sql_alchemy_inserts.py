import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_alchemy_tables import LinksTable, GoodOnes, BadOnesUser, BadOnesKeywords
from general import file_to_list

db = 'sqlite:///crawler_files/sqlite_database.db'


# def insert_link(data):
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     # insert a item
#
#     link = LinksTable(link_url=data)
#
#     # instead session.add you can use bulk_save_objects
#
#     session.add(link)
#     session.commit()
#     print("ukládám do databáze", link.link_url)


def insert_link_list(link_list, website):
    save_list = []
    engine = create_engine(db)

    Session = sessionmaker(bind=engine)
    session = Session()

    for link in link_list:
        save_list.append(LinksTable(link=link, website=website))

    save_list = set(save_list)

    session.bulk_save_objects(save_list)
    session.commit()


def insert_good_ones(link_list):
    save_list = []
    engine = create_engine(db)

    Session = sessionmaker(bind=engine)
    session = Session()

    for link in link_list:
        save_list.append(GoodOnes(website=link["website"], link=link["link"], keywords=link["keywords"]))

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
