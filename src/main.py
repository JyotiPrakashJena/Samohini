from fastapi import FastAPI
from module_fibo.fibo import FiboModules
from models.module_fibo_model import request_fibo_module

app = FastAPI()

@app.get("/")
def samhonini():
    return "Welcome! to Samhohini."

@app.get("/get_fibo_levels")
async def get_fibo_levels(stock_id: str, stock_name: str, period: int = 3):
    """
    Method to fetch Fibo Levels of a given stock.
    
    stock_id: unique id of the stock.
    """
    request = request_fibo_module(stock_id=stock_id,
                                  stock_name=stock_name,
                                  period=period)
    response = FiboModules().get_fibo_levels(request=request)
    return response
