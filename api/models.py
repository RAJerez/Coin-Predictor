from sqlalchemy import Date, Column, String, Float, JSON, Integer, PrimaryKeyConstraint, ForeignKey
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DB_CONNSTR = config("DB_CONNSTR")


engine = create_engine(DB_CONNSTR)
meta = MetaData(schema='public')
Base = declarative_base(metadata=meta)


class CoinData(Base):
    __tablename__ = "coin_data"
    
    coin = Column(String(255), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True)
    price = Column(Float, nullable=False)
    json = Column(JSON(255), nullable=False)


class CoinMonthData(Base):
    __tablename__ = "coin_month_data"

    coin = Column(String, nullable=False, primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)
    month = Column(Integer, nullable=False, primary_key=True)
    min_price = Column(Float)
    max_price = Column(Float)
    
