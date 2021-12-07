from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_alchemy_tables import LinksTable


db = 'sqlite:///crawler_files/sqlite_database.db'


def insert_link(link, website):
    engine = create_engine(db)

    Session = sessionmaker(bind=engine)
    session = Session()

    # insert a item

    line = LinksTable(link=link, website=website)

    # instead session.add you can use bulk_save_objects

    session.add(line)
    session.commit()
    # print("ukládám do databáze", line.link)


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


if __name__ == "__main__":
    insert_link("Hola", "seznam")
