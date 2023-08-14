from fastapi import FastAPI
from module_fibo.fibo import FiboModules
from module_candlestick.bull_candlestick import BullCandleStick
from module_indicators.indicators import BullIndicators
from module_sr.support_resistance import SupportResistanceIndicator
from module_volume.bull_volume import VolumeIndicator
from models.candlestick_model import request_candle_module, response_candle_module
from models.fibo_model import request_fibo_module, response_fibo_module
from models.indicators_model import request_indicator_module, response_indicator_module
from models.risk_reward_model import (
    request_risk_reward_module,
    response_risk_reward_module,
)
from models.support_resistance_model import request_SR_module, response_SR_module
from models.volume_model import request_volume_module, response_volume_module
from utils.risk_reward import validate_risk_reward

tags_metadata = [
    {
        "name": "StockScreeners",
        "description": "Operations with stocks.",
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
async def get_fibo_levels(
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
async def get_bullish_candles(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_candle_module:
    """Method to validate the bullish candlestick of a given stock."""
    request = request_candle_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    candlestick_response = BullCandleStick().get_candle_bull_response(request=request)
    return candlestick_response


@app.get("/get_bullish_indicators", tags=["StockScreeners"])
async def get_bullish_indicators(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_indicator_module:
    """Method to validate the bullish indicators of a given stock."""
    request = request_indicator_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    candlestick_response = BullIndicators().get_indicators_response(request=request)
    return candlestick_response


@app.get("/get_support_resistance_levels", tags=["StockScreeners"])
async def get_support_resistance_levels(
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
async def validate_risk_reward(
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
async def validate_volume_indicator(
    stock_id: str, stock_name: str = "", period: int = 1, time_frame: str = "y"
) -> response_volume_module:
    """Method to extract the support resistance levels of a given stock."""
    request = request_volume_module(
        stock_id=stock_id, stock_name=stock_name, period=period, time_frame=time_frame
    )
    volume_indicator_response = VolumeIndicator().volume_indicator_response(request)
    return volume_indicator_response
