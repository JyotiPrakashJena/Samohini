import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Float, Boolean, MetaData


DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_INSTANCE = os.environ.get('DB_INSTANCE')
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_INSTANCE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SelectedTradeTable(Base):
    """Stocks Selected to be Traded added to the trade_selection_table."""

    __tablename__ = "trade_selection"
    stock_id = Column(String, primary_key=True)
    stock_name = Column(String)
    buy_price = Column(Float)
    stoploss = Column(Float)
    target = Column(Float)
    expected_profit = Column(Float)
    expected_loss = Column(Float)
    exp_risk_reward_ratio = Column(Float)


class ExecutedTradeTable(Base):
    """Stocks actual Executed added to the trade_executed table."""

    __tablename__= "trade_executed"
    stock_id = Column(String, primary_key=True)
    stock_name = Column(String)
    buy_price = Column(Float)
    stoploss = Column(Float)
    current_market_price = Column(Float) #Updated for every executions
    target = Column(Float)
    profit_till_now = Column(Float)
    loss_till_now = Column(Float)
    profit_check = Column(Boolean)
    loss_check = Column(Boolean)

#Creating Tables in database
#Base.metadata.create_all(bind=engine) #To Create Entries in DB
