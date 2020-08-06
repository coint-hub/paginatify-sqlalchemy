from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from paginatify_sqlalchemy import Pagination

engine = create_engine('sqlite://')
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Item(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)

    __tablename__ = 'item'


Base.metadata.create_all()


def paginate(count, page=1):
    def first(item):
        return item[0]

    session = Session()
    # keep reference to prevent garbage collected
    items = [Item() for _ in range(count)]
    session.add_all(items)
    try:
        session.flush()
        pagination = Pagination(session.query(Item.id), page=page, per_page=3,
                                per_nav=3, map_=first)
        assert pagination.total == count
        return pagination
    finally:
        session.rollback()
        session.close()


def test_len():
    assert paginate(0).total == 0
    assert paginate(10).total == 10


def test_getitem():
    assert paginate(0).items == tuple()
    assert paginate(10, 2).items == (4, 5, 6)
