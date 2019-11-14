from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql+psycopg2://user_5:555@localhost/base_scraper')  # соединяемся с базой PostgresSQL


Session = sessionmaker(bind=engine)
Base = declarative_base()


class HeadHunter(Base):  # Декларативное создание таблицы, класса и отображения за один раз
    __tablename__ = 'HeadHunter'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    title = Column(String)
    salary = Column(String)
    responsibilites_short = Column(String)
    requirements_short = Column(String)
    company = Column(String)
    experience = Column(String)
    employment_mode = Column(String)
    description = Column(String)


    def __init__(self, link, title, salary, responsibilites_short, requirements_short, company, experience, employment_mode, description):
        self.link = link
        self.title = title
        self.salary = salary
        self.responsibilites_short = responsibilites_short
        self.requirements_short = requirements_short
        self.company = company
        self.experience = experience
        self.employment_mode = employment_mode
        self.description = description


    def __repr__(self):
        return "<HeadHunter('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.link, self.title, self.salary, self.responsibilites_short, self.requirements_short, self.company, self.experience, self.employment_mode, self.description)


class MoiKrug(Base):  # Декларативное создание таблицы, класса и отображения за один раз
    __tablename__ = 'MoiKrug'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    title = Column(String)
    salary = Column(String)
    skills = Column(String)
    company = Column(String)
    work_conditions = Column(String)
    description = Column(String)

    def __init__(self, link, title, salary, skills, company, work_conditions, description):
        self.link = link
        self.title = title
        self.salary = salary
        self.skills = skills
        self.company = company
        self.work_conditions = work_conditions
        self.description = description


    def __repr__(self):
        return "<MoiKrug('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.link, self.title, self.salary, self.skills, self.company, self.work_conditions, self.description)


Base.metadata.create_all(engine)

