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


class GoodOnes(Base):
    __tablename__ = "good_ones"

    id = Column(Integer, primary_key=True)
    link = Column(String(255), index=True, unique=True)
    website = Column(String(10))
    keywords = Column(String(255))


class BadOnesUser(Base):
    __tablename__ = "bad_ones_user"

    id = Column(Integer, primary_key=True)
    link = Column(String(255), index=True, unique=True)
    website = Column(String(10))
    user = Column(String(30))


class BadOnesKeywords(Base):
    __tablename__ = "bad_ones_keywords"

    id = Column(Integer, primary_key=True)
    link = Column(String(255), index=True, unique=True)
    website = Column(String(10))
    keywords = Column(String(255))


def write_tables_to_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    write_tables_to_db()
