from module_stock.stock import StockDetails
from utils.extras import format_float

import yahoo_fin.stock_info as si

TRAILING_PE_DEATILS_CONSTANT = "trailingPE"
FOWARDING_PE_DEATILS_CONSTANT = "forwardPE"
STOCK_PE_CONSTANT = 'PE Ratio (TTM)'


class FundamentalChecker:
    """Helper class with methods for Fundamental Analysis."""

    def get_stock_fundamentals(self, stock_id: str) -> dict:
        """Method to Extract Stock Fundamentals."""
        stock_info = StockDetails().get_stock_info(stock_id)
        return stock_info


    def get_stock_pe(self, stock_id: str) -> float:
        """Method to Extract P/E from Stock Fundamentals."""
        stock_info = self.get_stock_fundamentals(stock_id)

        return format_float(stock_info[f'{stock_id}.NS'][TRAILING_PE_DEATILS_CONSTANT])
