import main
from module_core.samohini_db_methods import CoreCRUD
from module_core.samohini_core_schema import ExecutedTradeTable

from utils.extras import format_float

def value_from_dict(dict_: dict, key: str):
    return dict_.get(key)

def value_from_list(list_:list, key: str):
    return list_[0].get(key)

import time
def execute_selected_stocks():
    """Fetch the Selected Stocks for Execution."""
    try:
        selected_stocks = main.get_all_from_selected_table(offset=0, limit=1000)
        if 'message' in selected_stocks:
            return {"Nothing to Trade."}
        EXECUTED_ENTRIES = []
        for selected_stock in selected_stocks:
            stock_id = value_from_dict(selected_stock, "stock_id")
            try:
                stock_current_mkt_price = main.get_stock_details(stock_id)  # For Period=1day
                buy_price = format_float(value_from_dict(selected_stock, "buy_price"))
                current_price = format_float(value_from_list(stock_current_mkt_price, "close"))
                stoploss=format_float(value_from_dict(selected_stock, "stoploss"))
                executed_dict=None
                if current_price > buy_price:
                    profit_till_now = format_float(current_price - buy_price)
                    profit_check = True
                    loss_till_now = 0
                    loss_check = False
                    executed_dict = {"stock_id":stock_id,
                    "stock_name":value_from_dict(selected_stock, "stock_name"),
                    "buy_price":buy_price,
                    "stoploss":stoploss,
                    "current_market_price":current_price,
                    "target":value_from_dict(selected_stock, "target"),
                    "profit_till_now":profit_till_now,
                    "loss_till_now":loss_till_now,
                    "profit_check":profit_check,
                    "loss_check":loss_check
                    }
                else:
                    loss_till_now = format_float(buy_price - current_price)
                    loss_check = True
                    profit_till_now = 0
                    profit_check = False
                    executed_dict = {"stock_id":stock_id,
                    "stock_name":value_from_dict(selected_stock, "stock_name"),
                    "buy_price":buy_price,
                    "stoploss":stoploss,
                    "current_market_price":current_price,
                    "target":value_from_dict(selected_stock, "target"),
                    "profit_till_now":profit_till_now,
                    "loss_till_now":loss_till_now,
                    "profit_check":profit_check,
                    "loss_check":loss_check
                    }
                EXECUTED_ENTRIES.append(executed_dict)
                main.clear_all_from_selected_table()
            except Exception as e:
                print(e)
        CoreCRUD(ExecutedTradeTable).create_multiple_entries(EXECUTED_ENTRIES)
    except Exception as e:
        print(f"Exception:{e}")
    return {"messages": "Execution Completed.(Selected Stocks has been Traded.)"}


def generate_profit_loss_report():
    """Method to generate Insights of Profit/Loss from the Execution Table."""
    try:
        executed_stocks = main.get_all_from_executed_table(offset=0, limit=1000)
        if 'message' in executed_stocks:
            return {"Nothing to generate report."}
        for executed_stock in executed_stocks:
            #print(executed_stock)
            buy_price = format_float(value_from_dict(executed_stock, "buy_price"))
            curr_price = format_float(value_from_dict(executed_stock, "current_market_price"))
            stoploss = format_float(value_from_dict(executed_stock, "stoploss"))
            target = format_float(value_from_dict(executed_stock, "target"))
            stock_id = value_from_dict(executed_stock, "stock_id")
            if curr_price >= target:
                print(f"Time to Book Profit {format_float(curr_price - buy_price)}.")
                main.profit_executed_add_entry(
                    stock_id=stock_id,
                    buy_price=buy_price,
                    stoploss=stoploss,
                    curr_price=curr_price,
                    target=target,
                    sell_price=curr_price,
                    booked_profit=format_float(curr_price - buy_price),
                    stock_name=value_from_dict(executed_stock, "stock_name"),
                )
                main.executed_table_delete_by_id(stock_id)
            elif curr_price <= stoploss:
                print(f"Time to Book Loss {format_float(buy_price - stoploss)}.")
                main.loss_executed_add_entry(
                    stock_id=value_from_dict(executed_stock, "stock_id"),
                    buy_price=format_float(buy_price),
                    stoploss=format_float(stoploss),
                    curr_price=format_float(curr_price),
                    target=format_float(target),
                    sell_price=format_float(curr_price),
                    booked_loss=format_float(buy_price - curr_price),
                    stock_name=value_from_dict(executed_stock, "stock_name"),
                )
                main.executed_table_delete_by_id(stock_id)
        print("Profit/Loss Report Generated.")
    except Exception as e:
        print("Exception:", e)

print("Executing Stocks from Selected Stock.")
execute_selected_stocks()
print("Generating Profit/Loss from Executed Stock.")
generate_profit_loss_report()
print("Execution Done. DB Updated.")
