import os


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker


DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_INSTANCE = os.environ.get('DB_INSTANCE')
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_INSTANCE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CoreCRUD:
    def __init__(self, model: DeclarativeMeta):
        self.db = SessionLocal()
        self.model = model


    def create(self, item: dict):
        """Method to Create Entry."""
        print("Creating Entry..")
        print(item)
        db_item = self.model(**item)
        db_item_entry = self.db.query(self.model).filter(self.model.stock_id == db_item.stock_id).first()
        if not db_item_entry:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return {'message': f'Entry Created successfully for {db_item.stock_id}.'}
        return {'Exception': f'Entry Already Exists for {db_item.stock_id}.'}


    def get_by_stock_id(self, stock_id: str):
        """Method to fetch stock details by stock_id"""

        stock_details = self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        return vars(stock_details) if stock_details else {'Exception':f'No Entry found with {stock_id}'}


    def get_all(self, skip: int = 0, limit: int = 10):
        """Method to fetch all the stock details."""
        response = self.db.query(self.model).offset(skip).limit(limit).all()
        return [vars(res) for res in response] if response else {'message':'Nothing here yet.'}


    def update(self, stock_id: str, updated_item: dict):
        """Method to Update Entry."""
        db_item = self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        if db_item:
            for attr, value in updated_item.items():
                setattr(db_item, attr, value) if value is not None else None
            self.db.commit()
            self.db.refresh(db_item)
            return {'message': f'Updated successfully for {stock_id}.'}
        return {'Exception':f'Entry Not Found for {stock_id}'}


    def delete(self, stock_id: str):
        """Method to delete Entry."""
        db_item = self.db.query(self.model).filter(self.model.stock_id == stock_id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return {"message": f"{stock_id} deleted successfully."}
        return {"Exception": f"Entry not found for {stock_id}"}
