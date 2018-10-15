from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Date, Integer, String
from sqlalchemy import ForeignKey


metadata = MetaData()


marks = Table('marks', metadata,
    Column('number', Integer, primary_key=True, autoincrement=False),
    Column('name', String(12), nullable=False)
)


results = Table('results', metadata,
    Column('draw', Integer, primary_key=True, autoincrement=False),
    Column('date', Date, nullable=False),
    Column('period', String(2), nullable=False),
    Column('number', Integer, ForeignKey('marks.number'), nullable=False)
)
