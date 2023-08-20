from running_module import main

def value_from_dict(dict_: dict, key: str):
    return dict_.get(key)

def value_from_list(list_:list, key: str):
    return list_[0].get(key)

import time
def execute_selected_stocks():
    """Fetch the Selected Stocks for Execution."""
    selected_stocks = main.get_all_from_selected_table(offset=0, limit=50)
    for selected_stock in selected_stocks:
        stock_id = value_from_dict(selected_stock, "stock_id")
        stock_current_mkt_price = main.get_stock_details(stock_id)  # For Period=1day

        buy_price = value_from_dict(selected_stock, "buy_price")
        current_price = value_from_list(stock_current_mkt_price, "close")

        if current_price > buy_price:
            profit_till_now = current_price - buy_price
            profit_check = True
            loss_till_now = 0
            loss_check = False
        else:
            loss_till_now = buy_price - current_price
            loss_check = True
            profit_till_now = 0
            profit_check = False
        get_executed_by_stock_id = main.executed_table_details_by_id(stock_id)
        # If stocks in the Selected List not present in Executed List, Add an Entry
        if "Exception" in get_executed_by_stock_id:
            # main.executed_table_add_entry(
            #     stock_id=stock_id,
            #     stock_name=value_from_dict(selected_stock, "stock_name"),
            #     buy_price=buy_price,
            #     stoploss=value_from_dict(selected_stock, "stoploss"),
            #     current_market_price=current_price,
            #     target=value_from_dict(selected_stock, "target"),
            #     profit_till_now=profit_till_now,
            #     loss_till_now=loss_till_now,
            #     profit_check=profit_check,
            #     loss_check=loss_check,
            # )
            print(f"{stock_id} Included in the Execution Table. profit till Now: {profit_till_now}")
        else:
            # If stocks in the Selected List present in Executed List, Update the Entry
            # main.executed_table_update_entry(
            #     stock_id=stock_id,
            #     stock_name=value_from_dict(selected_stock, "stock_name"),
            #     buy_price=buy_price,
            #     stoploss=value_from_dict(selected_stock, "stoploss"),
            #     current_market_price=current_price,
            #     target=value_from_dict(selected_stock, "target"),
            #     profit_till_now=profit_till_now,
            #     loss_till_now=loss_till_now,
            #     profit_check=profit_check,
            #     loss_check=loss_check,
            # )
            print(f"{stock_id} updated in the Execution Table. Loss till now: {loss_till_now}")
    return {"messages": "Execution Completed.(Selected Stocks has been Traded.)"}


def generate_profit_loss_report():
    """Method to generate Insights of Profit/Loss from the Execution Table."""
    executed_stocks = main.get_all_from_executed_table(offset=0, limit=50)
    for executed_stock in executed_stocks:
        #print(executed_stock)
        buy_price = value_from_dict(executed_stock, "buy_price")
        curr_price = value_from_dict(executed_stock, "current_market_price")
        stoploss = value_from_dict(executed_stock, "stoploss")
        target = value_from_dict(executed_stock, "target")
        if curr_price >= target:
            print(f"Time to Book Profit {(curr_price - buy_price)}.")
            # main.profit_executed_add_entry(
            #     stock_id=value_from_dict(executed_stock, "stock_id"),
            #     buy_price=buy_price,
            #     stoploss=stoploss,
            #     curr_price=curr_price,
            #     target=target,
            #     sell_price=curr_price,
            #     booked_profit=(curr_price - buy_price),
            #     stock_name=value_from_dict(executed_stock, "stock_name"),
            # )
        elif curr_price <= stoploss:
            print(f"Time to Book Loss {(buy_price - curr_price)}.")
            # main.loss_executed_add_entry(
            #     stock_id=value_from_dict(executed_stock, "stock_id"),
            #     buy_price=buy_price,
            #     stoploss=stoploss,
            #     curr_price=curr_price,
            #     target=target,
            #     sell_price=curr_price,
            #     booked_loss=(buy_price - curr_price),
            #     stock_name=value_from_dict(executed_stock, "stock_name"),
            # )
    print("Profit/Loss Report Generated.")

print("Executing Selected Stocks")
execute_selected_stocks()
print("Booking Profit/Loss")
generate_profit_loss_report()
