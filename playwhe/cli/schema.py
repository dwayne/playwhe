from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Date, Integer, String
from sqlalchemy import ForeignKey


metadata = MetaData()


marks = Table('marks', metadata,
    Column('number', Integer, primary_key=True, autoincrement=False),
    Column('name', String(12), nullable=False)
)

periods = Table('periods', metadata,
    Column('abbr', String(2), primary_key=True),
    Column('label', String(7), nullable=False),
    Column('time_of_day', Integer, nullable=False)
)

results = Table('results', metadata,
    Column('draw', Integer, primary_key=True, autoincrement=False),
    Column('date', Date, nullable=False),
    Column('period_abbr', None, ForeignKey('periods.abbr'), nullable=False),
    Column('mark_number', None, ForeignKey('marks.number'), nullable=False)
)
