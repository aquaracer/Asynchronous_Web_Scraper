import asyncio

from sqlalchemy_aio import ASYNCIO_STRATEGY
from datetime import time, date, datetime
from sqlalchemy import (Column, Integer, MetaData, Table, Text, create_engine, select)
from sqlalchemy.schema import CreateTable, DropTable

engine = create_engine('postgresql+psycopg2://user_5:555@localhost/base_scraper', strategy=ASYNCIO_STRATEGY)  # соединяемся с базой PostgresSQL

metadata = MetaData()

HeadHunter_db = Table(
        'HeadHunter' + str(date.today()), metadata,
        Column('id', Integer, primary_key=True),
        Column('link', Text),
        Column('salary', Text),
        Column('title', Text),
        Column('responsibilites_short', Text),
        Column('requirements_short', Text),
        Column('company', Text),
        Column('experience', Text),
        Column('employment_mode', Text),
        Column('description', Text))


MoiKrug_db = Table(
        'MoiKrug' + str(date.today()), metadata,
        Column('id', Integer, primary_key=True),
        Column('link', Text),
        Column('title', Text),
        Column('salary', Text),
        Column('skills', Text),
        Column('company', Text),
        Column('occupation', Text),
        Column('description', Text))






