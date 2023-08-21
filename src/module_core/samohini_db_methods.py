import os

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from .samohini_core_schema import ExecutedTradeTable, SelectedTradeTable


DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_INSTANCE = os.environ.get("DB_INSTANCE")
DB_NAME = os.environ.get("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_INSTANCE}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=15)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def open_and_close_session():
    session = SessionLocal()
    try:
        yield session  # Provide the session to the caller
        session.commit()  # Commit changes before closing
    except Exception as e:
        session.rollback()  # Rollback changes if an exception occurs
        raise e
    finally:
        session.close()

class CoreCRUD:
    def __init__(self, model: DeclarativeMeta):
        with open_and_close_session() as session:
            self.db = session
        self.model = model

    def create(self, item: dict):
        """Method to Create Entry."""
        self.db_item = self.model(**item)
        self.db_item_entry = (
            self.db.query(self.model)
            .filter(self.model.stock_id == self.db_item.stock_id)
            .first()
        )
        if not self.db_item_entry:
            self.db.add(self.db_item)
            self.db.commit()
            self.db.refresh(self.db_item)
            
            return {"message": f"Entry Created successfully for {self.db_item.stock_id}."}
        return {"Exception": f"Entry Already Exists for {self.db_item.stock_id}."}
    
    def create_multiple_entries(self, items):
        """Method to Create Multiple Entries."""
        new_entries = [ExecutedTradeTable(**item) for item in items]
        self.db.add_all(new_entries)
        self.db.commit()
        

    def get_by_stock_id(self, stock_id: str):
        """Method to fetch stock details by stock_id"""
        stock_details = (
            self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        )
        
        return (
            vars(stock_details)
            if stock_details
            else {"Exception": f"No Entry found with {stock_id}"}
        )

    def get_all(self, skip: int = 0, limit: int = 10):
        """Method to fetch all the stock details."""
        response = self.db.query(self.model).offset(skip).limit(limit).all()
        
        return (
            [vars(res) for res in response]
            if response
            else {"message": "Nothing here yet."}
        )

    def update(self, stock_id: str, updated_item: dict):
        """Method to Update Entry."""
        self.db_item = (
            self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        )
        if self.db_item:
            for attr, value in updated_item.items():
                setattr(self.db_item, attr, value) if value is not None else None
            self.db.commit()
            self.db.refresh(self.db_item)
            
            return {"message": f"Updated successfully for {stock_id}."}
        return {"Exception": f"Entry Not Found for {stock_id}"}

    def delete(self, stock_id: str):
        """Method to delete Entry."""
        self.db_item = (
            self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        )
        if self.db_item:
            self.db.delete(self.db_item)
            self.db.commit()
            
            return {"message": f"{stock_id} deleted successfully."}
        return {"Exception": f"Entry not found for {stock_id}"}
