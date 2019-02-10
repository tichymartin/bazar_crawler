from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

db = 'sqlite:///crawler_files/sqlite_database.db'

# engine = create_engine('sqlite:///:memory:')

engine = create_engine(db)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class LinksTable(Base):
    __tablename__ = "links_table"

    link_id = Column(Integer, primary_key=True)
    link = Column(String(255), index=True, unique=True)
    website = Column(String(10))


# class Keywords(Base):
#     __tablename__ = "keywords"
#
#     id = Column(Integer, primary_key=True)
#     keyword = Column(String(50), unique=True)
#
#
# class Stopwords(Base):
#     __tablename__ = "stopwords"
#
#     id = Column(Integer, primary_key=True)
#     stopword = Column(String(50), unique=True)
#
#
# class Stopusers(Base):
#     __tablename__ = "stopusers"
#
#     id = Column(Integer, primary_key=True)
#     stopuser = Column(String(50), unique=True)


def write_tables_to_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    write_tables_to_db()
