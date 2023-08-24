from main import (get_all_from_profit_executed_table, 
                  get_all_from_loss_executed_table,
                  get_all_from_executed_table)

from utils.extras import format_float


class ProfitLossInsight:
    """Class with Methods to generate Profit/Loss."""

    def get_profit_report(self):
        """Method to generate Insight on Profit"""
        print('***Generating Profit Report***')
        total_capital = 0
        total_profit = 0
        all_stocks = get_all_from_profit_executed_table(offset=0, limit=1000)
        for stock in all_stocks:
            total_capital += stock.get('buy_price')
            total_profit += stock.get('booked_profit')
        print(f"Stocks Hit Target: {format_float(len(all_stocks))}")
        print(f"Capital: {format_float(total_capital)}")
        print(f"Profit: {format_float(total_profit)}")
        print(f'% of Return {format_float(total_profit*100/total_capital)}')
        return total_capital, total_profit


    def get_loss_report(self):
        """Method to generate Insight on Loss"""
        print('***Generating Loss Report***')
        total_capital = 0
        total_loss = 0
        all_stocks = get_all_from_loss_executed_table(offset=0, limit=1000)
        for stock in all_stocks:
            total_capital += stock.get('buy_price')
            total_loss += stock.get('booked_loss')
        print(f"Stocks Hit Loss: {format_float(len(all_stocks))}")
        print(f"Capital: {format_float(total_capital)}")
        print(f"Loss: {format_float(total_loss)}")
        print(f'% of Return {format_float(total_loss*100/total_capital)}')
        return total_capital, total_loss


    def get_executed_profit_loss_report(self):
        """Method to generate Insight on Stocks which has not reached Stoploss/Target"""
        print('***Generating Profit/Loss Report from Executed Stocks.***')
        total_capital = 0
        total_loss = 0
        total_profit = 0
        all_stocks = get_all_from_executed_table(offset=0, limit=1000)
        stocks_on_profit = 0
        stocks_on_loss = 0
        for stock in all_stocks:
            if stock.get('profit_check'): #If Stock is in Profit
                total_profit += stock.get('profit_till_now')
                stocks_on_profit += 1
            else:
                total_loss += stock.get('loss_till_now')
                stocks_on_loss += 1
            total_capital += stock.get('buy_price')
        
        print(f"Stocks on Profit: {stocks_on_profit}")
        print(f"Profit: {format_float(total_profit)}")
        print(f"Stocks on Loss: {stocks_on_loss}")
        print(f"Loss: {format_float(total_loss)}")
        print(f"Capital: {format_float(total_capital)}")
        print(f'% of Gain/Loss: {format_float((total_profit-total_loss)*100/total_capital)}')
        return [total_capital, total_profit, total_loss]


    def get_profit_loss_insight(self):
        """Method to generate overall insight on Profit/Loss."""
        exec_capital, exec_profit, exec_loss = self.get_executed_profit_loss_report()
        profit_capital, profit = self.get_profit_report()
        loss_capital, loss = self.get_loss_report()

        total_capital = exec_capital + profit_capital + loss_capital
        total_gain = exec_profit + profit - exec_loss - loss
        print("***Generating Overall Insight on Trades**")
        print(f"Total Capital: {format_float(total_capital)}")
        print(f"Total Gain: {format_float(total_gain)}")
        print(f"% Gain: {format_float(total_gain*100/total_capital)}")
        return total_capital, total_gain
    
pl_insight = ProfitLossInsight()
pl_insight.get_profit_loss_insight()