import pandas as pd
import yfinance as yf


class StockDetails:
    """Class with methods to assist other technical indicators like fibo, candlestick etc."""

    def get_stock_data(
        self, stock_id: str, period: int, time_frame: str
    ) -> pd.DataFrame:
        """Helper Method to fetch stock price details for a certain period.

        stock_id (str): unique id of the Stock.
        period (int): time period for which stock details will be fetched.
        """

        stock_data = (
            yf.Ticker(str(stock_id) + ".NS")
            .history(period=f"{period}{time_frame}")
            .tz_localize(None)
        )
        stock_data.columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "Stock Splits",
        ]

        return stock_data

    def get_stock_list(self) -> pd.DataFrame:
        """Helper function to get the list of stocks trading under NSE."""
        stock_data = pd.read_csv(
            "/Users/ujejyoti/Documents/PrakashSpace/Samohini/src/module_stock/static_files/EQUITY_L.csv"
        )
        stock_data.columns = [
            "Symbol",
            "Name",
            "Series",
            "List_Date",
            "Paid_Value",
            "Market_Lot",
            "ISIN",
            "Face_Value",
        ]
        return stock_data
