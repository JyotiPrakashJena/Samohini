from fastapi import FastAPI, Query
from datetime import datetime
import pytz

from module_fibo.fibo import FiboModules
from module_candlestick.bull_candlestick import BullCandleStick
from module_indicators.indicators import BullIndicators
from module_sr.support_resistance import SupportResistanceIndicator
from module_stock.stock import StockDetails
from module_volume.bull_volume import VolumeIndicator
from automated_scripts.stock_screener import StockScreener
from models.candlestick_model import request_candle_module, response_candle_module
from models.fibo_model import request_fibo_module, response_fibo_module
from models.indicators_model import request_indicator_module, response_indicator_module
from models.risk_reward_model import (
    request_risk_reward_module,
    response_risk_reward_module,
)
from models.stock import (
    request_stock_data,
    request_stock_data_by_start_end_date,
    request_stock_data_by_period,
)
from models.support_resistance_model import request_SR_module, response_SR_module
from models.volume_model import request_volume_module, response_volume_module
from models.stock_screener_model import (
    request_all_screener_details,
    response_all_screener_details,
)
from utils.risk_reward import validate_risk_reward

import pandas as pd


tags_metadata = [
    {
        "name": "StockDetails",
        "description": "Opearations to fetch stock details.",
    },
    {
        "name": "StockScreeners",
        "description": "Operations with stock screening.",
    },
    {
        "name": "Welcome",
        "description": "Welcome!",
    },
]

app = FastAPI(
    title="Samohini",
    description="Stock Screener and Recommend Engine.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


@app.get("/", tags=["Welcome"])
def samhonini():
    return "Welcome! to Samhohini."


@app.get("/get_fibo_levels", tags=["StockScreeners"])
def get_fibo_levels(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_fibo_module:
    """
    Method to fetch Fibo Levels of a given stock.

    stock_id: unique id of the stock.
    """
    request = request_fibo_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    fibo_response = FiboModules().get_fibo_levels(request=request)
    return fibo_response


@app.get("/get_bullish_candles", tags=["StockScreeners"])
def get_bullish_candles(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_candle_module:
    """Method to validate the bullish candlestick of a given stock."""
    request = request_candle_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    candlestick_response = BullCandleStick().get_candle_bull_response(request=request)
    return candlestick_response


@app.get("/get_bullish_indicators", tags=["StockScreeners"])
def get_bullish_indicators(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_indicator_module:
    """Method to validate the bullish indicators of a given stock."""
    request = request_indicator_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    candlestick_response = BullIndicators().get_indicators_response(request=request)
    return candlestick_response


@app.get("/get_support_resistance_levels", tags=["StockScreeners"])
def get_support_resistance_levels(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_SR_module:
    """Method to extract the support resistance levels of a given stock."""
    request = request_SR_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    candlestick_response = SupportResistanceIndicator().get_support_resistance_levels(
        request
    )
    return candlestick_response


@app.get("/validate_risk_reward", tags=["StockScreeners"])
def validate_risk_reward(
    buy_price: float, sell_price: float, stop_loss: float, rr_ratio: float
) -> response_risk_reward_module:
    """Method to extract the support resistance levels of a given stock."""
    request = request_risk_reward_module(
        buy_price=buy_price,
        sell_price=sell_price,
        rr_ratio=rr_ratio,
        stop_loss=stop_loss,
    )
    return validate_risk_reward(request)


@app.get("/validate_volume", tags=["StockScreeners"])
def validate_volume_indicator(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_volume_module:
    """Method to extract the support resistance levels of a given stock."""
    request = request_volume_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    volume_indicator_response = VolumeIndicator().volume_indicator_response(request)
    return volume_indicator_response


# get_all_screener_details
@app.get("/get_all_screener_details", tags=["StockScreeners"])
def get_all_screener_details(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_all_screener_details:
    """Method to extract all screener details of a given stock."""
    request = request_all_screener_details(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    get_all_screener_details_response = StockScreener().get_all_screener_details(
        request
    )
    return get_all_screener_details_response


@app.get("/get_recommended_stocks", tags=["StockScreeners"])
def get_all_recommended_stocks() -> object:
    try:
        response = StockScreener().recommended_stocks()
        return response
    except Exception as e:
        print(e)


@app.get("/get_buy_calls", tags=["StockScreeners"])
def get_bullish_buy_calls() -> object:
    try:
        response = StockScreener().get_buy_calls()
        return response
    except Exception as e:
        print(e)


@app.get("/get_stock_data", tags=["StockDetails"])
def get_stock_details(stock_id: str, period: int = 1, time_frame: str = "d"):
    request = request_stock_data(
        stock_id=stock_id, period=period, time_frame=time_frame
    )
    response = StockDetails().get_stock_data(request)
    return response.to_dict(orient="records")


@app.get("/get_stock_data_by_start_end_date", tags=["StockDetails"])
def get_stock_details_by_start_end_date(
    stock_id: str,
    start_date: str = Query("18-08-2022"),
    end_date: str = Query("18-08-2023"),
    period: int = Query("1"),
    time_frame: str = Query("d"),
):
    request = request_stock_data_by_start_end_date(
        stock_id=stock_id,
        start_date=start_date,
        end_date=end_date,
        time_frame=time_frame,
        period=period,
    )
    response = StockDetails().get_stock_data_by_start_end_date(request)
    return response.to_dict(orient="records")


@app.get("/get_stock_details_by_period", tags=["StockDetails"])
def get_stock_details_by_period(
    stock_id: str,
    interval: int,
    period: int = 1,
    time_frame: str = "d",
    end_day_period: int = 0,
    end_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y"),
):
    request = request_stock_data_by_period(
        stock_id=stock_id,
        back_in_period=interval,
        period=period,
        time_frame=time_frame,
        end_day_period=end_day_period,
        end_date=end_date,
    )
    response = StockDetails().get_stock_data_by_period(request)
    return response.to_dict(orient="records")
