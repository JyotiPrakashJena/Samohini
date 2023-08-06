import pandas as pd
import yfinance as yf

class StockDetails:
    """Class with methods to assist other technical indicators like fibo, candlestick etc."""

    def get_stock_data(self, stock_id: str, period: int) -> pd.DataFrame:
        """Helper Method to fetch stock price details for a certain period.
            
        stock_id (str): unique id of the Stock.
        period (int): time period for which stock details will be fetched.
        """

        stock_data = yf.Ticker(str(stock_id) + '.NS').history(period=f'{period}mo').tz_localize(None)
        stock_data.columns = ['open', 'high', 'low', 'close', 'Volume', 'Dividends', 'Stock Splits']

        return stock_data