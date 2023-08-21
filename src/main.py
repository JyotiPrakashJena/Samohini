from fastapi import FastAPI, Query
from datetime import datetime
import pytz

from module_fibo.fibo import FiboModules
from module_candlestick.bull_candlestick import BullCandleStick
from module_indicators.indicators import BullIndicators
from module_sr.support_resistance import SupportResistanceIndicator
from module_stock.stock import StockDetails
from module_volume.bull_volume import VolumeIndicator
from module_core.samohini_db_methods import CoreCRUD
from automated_scripts.stock_screener import StockScreener
from models.candlestick_model import request_candle_module, response_candle_module
from models.fibo_model import request_fibo_module, response_fibo_module
from models.indicators_model import request_indicator_module, response_indicator_module
from models.risk_reward_model import (
    request_risk_reward_module,
    response_risk_reward_module,
)
from models.samohini_core_model import (
    PySelectedTradeTable,
    PyExecutedTradeTable,
    PyProfitExecutedTable,
    PyLossExecutedTable,
)
from module_core.samohini_core_schema import (
    SelectedTradeTable,
    ExecutedTradeTable,
    ProfitExecutedTable,
    LossExecutedTable,
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
from samohini_report import generate_profit_loss_report, execute_selected_stocks



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
        "name": "DBSelectedTrade",
        "description": "Operations with DB Modules with SelectedTrade Table.",
    },
    {
        "name": "DBExecutedTrade",
        "description": "Operations with DB Modules with ExecutedTrade Table.",
    },
    {
        "name": "DBProfitExecuted",
        "description": "Operations with DB Modules with ExecutedProfit Table.",
    },
    {
        "name": "DBLossExecuted",
        "description": "Operations with DB Modules with ExecutedLoss Table.",
    },
    {
        "name": "Performance Testing",
        "description": "Module Specially Designed for Checking the Performance of Samohini.",
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

from datetime import timedelta
ist_timezone = pytz.timezone("Asia/Kolkata")
@app.get("/validate_performance_buy_calls", tags=["Performance Testing"])
def get_bullish_buy_calls(start_date:str, back_in_period: int, end_date: str=datetime.now(ist_timezone).strftime("%d-%m-%Y")):
    #end_date is the date from which recommendations with start. 
    #back_in_period is the no of days data will be fetched like 1y/2y
    try:
        end_date_obj = datetime.strptime(end_date, "%d-%m-%Y")
        start_date_obj = datetime.strptime(start_date, "%d-%m-%Y")
        if start_date_obj > end_date_obj:
            return {'Exception':f'Starting Date {start_date} should be before Ending Date {end_date}'}
        responses = []
        while start_date_obj<end_date_obj:
            if start_date_obj.weekday() < 5:
                start_date = start_date_obj.strftime("%d-%m-%Y")
                print(f"Processing for {start_date}")
                response = StockScreener().get_buy_calls_v2_performance(start_date, back_in_period)
                yield response
                print("Output:", response)
            start_date_obj += timedelta(days=1)
        print("Executing Stocks from Selected Stock.")
        execute_selected_stocks()
        print("Generating Profit/Loss from Executed Stock.")
        generate_profit_loss_report()
        return {"Execution Done. DB Updated."}
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
    back_in_period: int,
    period: int = 1,
    time_frame: str = "d",
    end_day_period: int = 0,
    end_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y"),
):
    request = request_stock_data_by_period(
        stock_id=stock_id,
        back_in_period=back_in_period,
        period=period,
        time_frame=time_frame,
        end_day_period=end_day_period,
        end_date=end_date,
    )
    response = StockDetails().get_stock_data_by_period(request)
    return response.to_dict(orient="records")


@app.get("/selected_table/add_entry", tags=["DBSelectedTrade"])
def selected_table_add_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    target: float,
    expected_profit: float,
    expected_loss: float,
    exp_risk_reward_ratio: float,
    stock_name: str = "",
):
    """Create Entry of SelectedTable by stock_id."""
    request = PySelectedTradeTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        expected_profit=expected_profit,
        expected_loss=expected_loss,
        exp_risk_reward_ratio=exp_risk_reward_ratio,
        stock_name=stock_name,
    )
    return CoreCRUD(SelectedTradeTable).create(vars(request))


@app.get("/selected_table/update_entry", tags=["DBSelectedTrade"])
def selected_table_update_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    target: float,
    expected_profit: float,
    expected_loss: float,
    exp_risk_reward_ratio: float,
    stock_name: str = "",
):
    """Update Entry of SelectedTable by stock_id."""
    request = PySelectedTradeTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        expected_profit=expected_profit,
        expected_loss=expected_loss,
        exp_risk_reward_ratio=exp_risk_reward_ratio,
        stock_name=stock_name,
    )
    return CoreCRUD(SelectedTradeTable).update(stock_id, vars(request))


@app.get("/selected_table/get_details_by_id", tags=["DBSelectedTrade"])
def selected_table_details_by_id(stock_id: str):
    """Method to stock details of SelectedTable by stock_id."""
    return CoreCRUD(SelectedTradeTable).get_by_stock_id(stock_id)


@app.get("/selected_table/delete_details_by_id", tags=["DBSelectedTrade"])
def selected_table_delete_by_id(stock_id: str):
    """Method to stock details of SelectedTable by stock_id."""
    return CoreCRUD(SelectedTradeTable).delete(stock_id)


@app.get("/selected_table/get_all", tags=["DBSelectedTrade"])
def get_all_from_selected_table(offset: int = 0, limit: int = 10):
    """Method to stock details of Selected Trade Table by stock_id."""
    return CoreCRUD(SelectedTradeTable).get_all(skip=offset, limit=limit)


@app.get("/selected_table/clear_all", tags=["DBSelectedTrade"])
def clear_all_from_selected_table():
    """Method to stock details of Selected Trade Table by stock_id."""
    return CoreCRUD(SelectedTradeTable).clear_entries()


@app.get("/executed_table/add_entry", tags=["DBExecutedTrade"])
def executed_table_add_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    current_market_price: float,
    target: float,
    profit_till_now: float,
    loss_till_now: float,
    profit_check: bool,
    loss_check: bool,
    stock_name: str = "",
):
    """Create Entry of SelectedTable by stock_id."""
    request = PyExecutedTradeTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        current_market_price=current_market_price,
        profit_till_now=profit_till_now,
        loss_till_now=loss_till_now,
        profit_check=profit_check,
        loss_check=loss_check,
        stock_name=stock_name,
    )
    return CoreCRUD(ExecutedTradeTable).create(vars(request))


@app.get("/executed_table/update_entry", tags=["DBExecutedTrade"])
def executed_table_update_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    current_market_price: float,
    target: float,
    profit_till_now: float,
    loss_till_now: float,
    profit_check: bool,
    loss_check: bool,
    stock_name: str = "",
):
    """Update Entry of ElectedTable by stock_id."""
    request = PyExecutedTradeTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        current_market_price=current_market_price,
        profit_till_now=profit_till_now,
        loss_till_now=loss_till_now,
        profit_check=profit_check,
        loss_check=loss_check,
        stock_name=stock_name,
    )
    return CoreCRUD(ExecutedTradeTable).update(stock_id, vars(request))


@app.get("/executed_table/get_stock_details_by_id", tags=["DBExecutedTrade"])
def executed_table_details_by_id(stock_id: str):
    """Method to stock details of ExecutedTrade Table by stock_id."""
    return CoreCRUD(ExecutedTradeTable).get_by_stock_id(stock_id)


@app.get("/executed_table/delete_details_by_id", tags=["DBExecutedTrade"])
def executed_table_delete_by_id(stock_id: str):
    """Method to stock details of Executed Trade Table by stock_id."""
    return CoreCRUD(ExecutedTradeTable).delete(stock_id)


@app.get("/executed_table/get_all", tags=["DBExecutedTrade"])
def get_all_from_executed_table(offset: int = 0, limit: int = 10):
    """Method to stock details of Executed Trade Table by stock_id."""
    return CoreCRUD(ExecutedTradeTable).get_all(skip=offset, limit=limit)


@app.get("/executed_table/clear_all", tags=["DBExecutedTrade"])
def clear_all_from_executed_table():
    """Method to stock details of Executed Trade Table by stock_id."""
    return CoreCRUD(ExecutedTradeTable).clear_entries()


# Profit Table
@app.get("/profit_executed/add_entry", tags=["DBProfitExecuted"])
def profit_executed_add_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    curr_price: float,
    target: float,
    sell_price: float,
    booked_profit: float,
    stock_name: str = "",
):
    """Create Entry of Profit Executed by stock_id."""
    trade_date = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y")
    trade_date_obj = datetime.strptime(trade_date,'%d-%m-%Y')
    request = PyProfitExecutedTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        curr_price=curr_price,
        sell_price=sell_price,
        booked_profit=booked_profit,
        trade_date=trade_date_obj,
        stock_name=stock_name,
    )
    return CoreCRUD(ProfitExecutedTable).create(vars(request))


@app.get("/profit_executed/update_entry", tags=["DBProfitExecuted"])
def profit_executed_update_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    curr_price: float,
    target: float,
    sell_price: float,
    booked_profit: float,
    stock_name: str = "",
):
    """Update Entry of Profit Executed by stock_id."""
    trade_date = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y")
    trade_date_obj = datetime.strptime(trade_date,'%d-%m-%Y')
    request = PyProfitExecutedTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        curr_price=curr_price,
        sell_price=sell_price,
        booked_profit=booked_profit,
        trade_date=trade_date_obj,
        stock_name=stock_name,
    )
    return CoreCRUD(ProfitExecutedTable).update(stock_id, vars(request))


@app.get("/profit_executed/get_profit_details_by_id", tags=["DBProfitExecuted"])
def profit_executed_details_by_id(stock_id: str):
    """Method to stock details of Profit Executed Table by stock_id."""
    return CoreCRUD(ProfitExecutedTable).get_by_stock_id(stock_id)


@app.get("/profit_executed/delete_details_by_id", tags=["DBProfitExecuted"])
def executed_profit_delete_by_id(stock_id: str):
    """Method to stock details of Profit Executed Trade Table by stock_id."""
    return CoreCRUD(ProfitExecutedTable).delete(stock_id)


@app.get("/profit_executed/get_all", tags=["DBProfitExecuted"])
def get_all_from_profit_executed_table(offset: int = 0, limit: int = 10):
    """Method to stock details of Profit Executed Table by stock_id."""
    return CoreCRUD(ProfitExecutedTable).get_all(skip=offset, limit=limit)


@app.get("/profit_executed/clear_all", tags=["DBProfitExecuted"])
def clear_all_from_profit_table():
    """Method to stock details of Profit Executed Trade Table by stock_id."""
    return CoreCRUD(ProfitExecutedTable).clear_entries()


@app.get("/loss_executed/add_entry", tags=["DBLossExecuted"])
def loss_executed_add_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    curr_price: float,
    target: float,
    sell_price: float,
    booked_loss: float,
    stock_name: str = "",
):
    """Create Entry of loss Executed by stock_id."""
    trade_date = datetime.now(pytz.timezone("Asia/Kolkata"))
    request = PyLossExecutedTable(
        stock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        curr_price=curr_price,
        sell_price=sell_price,
        booked_loss=booked_loss,
        trade_date=trade_date,
        stock_name=stock_name,
    )
    return CoreCRUD(LossExecutedTable).create(vars(request))


@app.get("/loss_executed/update_entry", tags=["DBLossExecuted"])
def loss_executed_update_entry(
    stock_id: str,
    buy_price: float,
    stoploss: float,
    curr_price: float,
    target: float,
    sell_price: float,
    booked_loss: float,
    stock_name: str = "",
):
    """Update Entry of loss Executed by stock_id."""
    trade_date = datetime.now(pytz.timezone("Asia/Kolkata"))
    request = PyLossExecutedTable(
        tock_id=stock_id,
        buy_price=buy_price,
        stoploss=stoploss,
        target=target,
        curr_price=curr_price,
        sell_price=sell_price,
        booked_loss=booked_loss,
        trade_date=trade_date,
        stock_name=stock_name,
    )
    return CoreCRUD(LossExecutedTable).update(stock_id, vars(request))


@app.get("/loss_executed/get_loss_details_by_id", tags=["DBLossExecuted"])
def loss_executed_details_by_id(stock_id: str):
    """Method to stock details of loss Executed Table by stock_id."""
    return CoreCRUD(LossExecutedTable).get_by_stock_id(stock_id)


@app.get("/loss_executed/delete_details_by_id", tags=["DBLossExecuted"])
def executed_loss_delete_by_id(stock_id: str):
    """Method to stock details of loss Executed Trade Table by stock_id."""
    return CoreCRUD(LossExecutedTable).delete(stock_id)


@app.get("/loss_executed/get_all", tags=["DBLossExecuted"])
def get_all_from_loss_executed_table(offset: int = 0, limit: int = 10):
    """Method to stock details of loss Executed Table by stock_id."""
    return CoreCRUD(LossExecutedTable).get_all(skip=offset, limit=limit)


@app.get("/loss_executed/clear_all", tags=["DBLossExecuted"])
def clear_all_from_loss_table():
    """Method to stock details of Loss Executed Trade Table by stock_id."""
    return CoreCRUD(LossExecutedTable).clear_entries()