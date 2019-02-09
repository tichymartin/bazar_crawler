from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_tables import Links_table
from sql_inserts import insert_link

db = 'sqlite:///crawler_files/sqlite_database.db'


def query_link(link, website):
    engine = create_engine('sqlite:///crawler_files/sqlite_database.db')

    Session = sessionmaker(bind=engine)
    session = Session()

    record = session.query(Links_table).filter(Links_table.website == website, Links_table.link == link).first()

    return record


# def query_stopuser(data):
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     record = session.query(Stopusers).filter(Stopusers.stopuser == data).first()
#
#     if not record:
#         return False
#     else:
#         return True
#
#
# def query_stopwords():
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     stopword_list = []
#     for stopword in session.query(Stopwords):
#         stopword_list.append(stopword.stopword)
#
#     return stopword_list
#
#
# def query_wordlist():
#     engine = create_engine(db)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     wordlist = []
#     for word in session.query(Keywords):
#         wordlist.append(word.keyword)
#
#     return wordlist


if __name__ == "__main__":
    print(query_wordlist())
