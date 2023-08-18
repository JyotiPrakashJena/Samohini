import pandas as pd
import yfinance as yf
import pytz

from datetime import datetime, timedelta

from models.stock import (
    request_stock_data,
    request_stock_data_by_period,
    request_stock_data_by_start_end_date,
)


class StockDetails:
    """Class with methods to assist other technical indicators like fibo, candlestick etc."""

    def get_stock_data(self, request: request_stock_data) -> pd.DataFrame:
        """Helper Method to fetch stock price details for a certain period.

        stock_id (str): unique id of the Stock.
        period (int): time period for which stock details will be fetched.
        """

        stock_data = (
            yf.Ticker(f"{request.stock_id}.NS")
            .history(period=f"{request.period}{request.time_frame}")
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

    def get_stock_data_by_start_end_date(
        self, request: request_stock_data_by_start_end_date
    ):
        """Method to fetch stock data by start date and end date."""
        # start_date = '2023-01-01'
        # end_date = '2023-08-18'
        # stock_symbol = 'AAPL'  # Replace with your desired stock symbol
        # interval='1d'

        # NOTE: StartDate are not Inclusing so to fetch for 18th Aug, Send request for 19th Augusteifjcbfcnrjturdjvkrnubrjbnditerdrufcbfuelbic

        start_date = datetime.strptime(request.start_date, "%d-%m-%Y")
        end_date = datetime.strptime(request.end_date, "%d-%m-%Y") + timedelta(days=1)
        stock_data = (
            yf.Ticker(f"{request.stock_id}.NS")
            .history(
                start=start_date,
                end=end_date,
                interval=f"{request.period}{request.time_frame}",
            )
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

    def get_stock_data_by_period(self, request: request_stock_data_by_period):
        """Method to fetch stock data by a period for both start day and end day."""

        ist_timezone = pytz.timezone("Asia/Kolkata")
        time_now_obj = datetime.now(ist_timezone).strftime("%d-%m-%Y")
        if time_now_obj != request.end_date:
            print(
                "Fetching stock data for a past start date and end date, Consider end days period"
            )
            # Going Back in time for end date
            time_now_obj = datetime.strptime(time_now_obj, "%d-%m-%Y")
            time_now_obj = time_now_obj - timedelta(days=request.end_day_period)

        # Fetch stock for a period from current date
        end_date_obj = datetime.strptime(request.end_date, "%d-%m-%Y")
        end_date = end_date_obj.strftime("%d-%m-%Y")

        start_date_obj = end_date_obj - timedelta(days=request.back_in_period)
        start_date = start_date_obj.strftime("%d-%m-%Y")

        request_stock_data_by_date = request_stock_data_by_start_end_date(
            stock_id=request.stock_id,
            start_date=start_date,
            end_date=end_date,
            period=request.period,
            time_frame=request.time_frame,
            back_in_period=request.back_in_period,
        )
        stock_data = self.get_stock_data_by_start_end_date(request_stock_data_by_date)
        stock_data.reset_index(inplace=True)
        stock_data.rename(columns={"index": "date"}, inplace=True)
        return stock_data
