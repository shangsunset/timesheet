import time
from datetime import datetime, date
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///timesheet.db', echo=True)
Base = declarative_base()


class TimesheetArchive(Base):

    __tablename__ = 'timesheet_archive'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='archive')
    created_date = Column(Date, default=date.today)


class Timesheet(Base):
    __tablename__ = 'timesheet'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_date = Column(Date, nullable=False, default=date.today)
    total_hours = Column(Float, default=0.0)

    timesheet_archive_id = Column(Integer, ForeignKey('timesheet_archive.id'))
    timesheet_archive = relationship(
            'TimesheetArchive',
            backref=backref('timesheets', order_by=id))


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today)
    checkin_time = Column(DateTime)
    checkout_time = Column(DateTime)
    task = Column(String, nullable=True)
    hours = Column(Float, nullable=True, default=0.0)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'))
    timesheet = relationship('Timesheet', backref=backref('entries', order_by=id))


Base.metadata.create_all(engine)
