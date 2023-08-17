import concurrent.futures
import time
import json
from prettytable import PrettyTable

from module_stock.stock import StockDetails
from module_candlestick.bull_candlestick import BullCandleStick
from module_indicators.indicators import BullIndicators
from module_sr.support_resistance import SupportResistanceIndicator
from module_fibo.fibo import FiboModules
from module_volume.bull_volume import VolumeIndicator

from models.stock_screener_model import (
    request_all_screener_details,
    response_all_screener_details,
    response_bull_buy_call,
)
from models.candlestick_model import request_candle_module, response_candle_module
from models.indicators_model import request_indicator_module, response_indicator_module
from models.support_resistance_model import (
    request_SR_module,
    response_SR_module,
    response_stock_sr,
)
from models.fibo_model import (
    request_fibo_module,
    response_fibo_module,
    response_stock_fibo,
)
from models.volume_model import request_volume_module, response_volume_module
from models.risk_reward_model import (
    response_risk_reward_module,
    request_risk_reward_module,
)
from utils.extras import format_float
from utils.risk_reward import validate_risk_reward
from utils.broadcast import broadcast_msg


class StockScreener:
    """Class with methods to screen stocks from the pool."""

    def handler_bull_candle_response(
        self, request: request_all_screener_details
    ) -> response_candle_module:
        """Handler for Bull Candle Response."""
        bull_candle_stick_request = request_candle_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            period=request.period,
            time_frame=request.time_frame,
            market=request.market,
            stock_data=request.stock_data,
        )
        return BullCandleStick().get_candle_bull_response(bull_candle_stick_request)

    def handler_indicator_response(
        self, request: request_all_screener_details
    ) -> response_indicator_module:
        """Handler for Bull Indicator Response."""
        bull_candle_stick_request = request_indicator_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            period=request.period,
            time_frame=request.time_frame,
            market=request.market,
            stock_data=request.stock_data,
        )
        return BullIndicators().get_indicators_response(bull_candle_stick_request)

    def handler_sr_response(
        self, request: request_all_screener_details
    ) -> response_SR_module:
        """Handler for Support Resistance."""
        support_resistance_request = request_SR_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            period=request.period,
            time_frame=request.time_frame,
            market=request.market,
            stock_data=request.stock_data,
        )
        return SupportResistanceIndicator().get_support_resistance_levels(
            support_resistance_request
        )

    def handler_fibo_response(
        self, request: request_all_screener_details
    ) -> response_fibo_module:
        """Handler for Fibo Response."""
        fibo_request = request_fibo_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            period=request.period,
            time_frame=request.time_frame,
            market=request.market,
            stock_data=request.stock_data,
        )
        return FiboModules().get_fibo_levels(fibo_request)

    def handler_volume_response(
        self, request: request_all_screener_details
    ) -> response_volume_module:
        """Handler for Volume Response."""
        volume_request = request_volume_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            period=request.period,
            time_frame=request.time_frame,
            market=request.market,
            stock_data=request.stock_data,
        )
        return VolumeIndicator().volume_indicator_response(volume_request)

    def get_all_screener_details(
        self, request: request_all_screener_details
    ) -> response_all_screener_details:
        """Validate if a stock passes all the checks."""
        try:
            stock_data = StockDetails().get_stock_data(
                stock_id=request.stock_id,
                period=request.period,
                time_frame=request.time_frame,
            )
            request.stock_data = stock_data
            candle_stick_response = self.handler_bull_candle_response(request)
            indicator_response = self.handler_indicator_response(request)
            sr_response = self.handler_sr_response(request)
            fibo_response = self.handler_fibo_response(request)
            volume_response = self.handler_volume_response(request)
            get_all_screener_response = response_all_screener_details(
                stock_id=request.stock_id,
                stock_name=request.stock_name,
                time_period=f"{request.period}{request.time_frame}",
                candle_stick_response=candle_stick_response,
                indicator_response=indicator_response,
                fibo_response=fibo_response,
                sr_response=sr_response,
                volume_response=volume_response,
            )
            return get_all_screener_response
        except Exception as e:
            print(f"Exception: {e}")

    def is_candle_stick_validated(self, request: response_candle_module) -> bool:
        """Helper function to validate if the candle_stick pattern satisfied."""
        bull_candles = vars(request.bullish_candles)
        bull_candles_true = sum(value == True for value in bull_candles.values())
        return True if bull_candles_true else False

    def is_indicator_stock_validated(self, request: response_indicator_module) -> bool:
        """Helper function to validate if the indicator satisfied."""
        indicator_response = vars(request.bull_indicators)
        indicator_response_true = sum(
            value == True for value in indicator_response.values()
        )
        return True if indicator_response_true else False

    def are_approximately_close(self, num1, num2, percent_threshold=2):
        """Method to validate if the provided numbers are close by a given threshold %"""
        return abs(num1 - num2) <= (num1 * (percent_threshold / 100))

    def find_range(self, numbers_list, target_number):
        """Find the range the given number is in between a list."""
        numbers_list.sort()

        no_of_index = len(numbers_list) - 1
        for i in range(no_of_index):
            if numbers_list[i] <= target_number <= numbers_list[i + 1]:
                return numbers_list[i], numbers_list[i + 1]

        if numbers_list[-1] < target_number:
            return numbers_list[-1], numbers_list[-1] * 1.236  # 0.236 for Fibo Level

    def is_sr_stock_validated(self, request: response_SR_module) -> response_stock_sr:
        """Helper function to validate Support Resistance levels."""
        sr_response_levels = request.levels
        current_mkt_price_now = request.cur_market_price.price_now
        support, resistance = self.find_range(sr_response_levels, current_mkt_price_now)

        # Check is only for bullish pattern
        # For Bullish pattern suppprt is the StopLoss & resistance is the Target.
        if self.are_approximately_close(
            current_mkt_price_now, support
        ):  # if close by 2% thrshold
            sr_response_stock = response_stock_sr(
                price_now=current_mkt_price_now,
                stop_loss=support,
                target=resistance,
                sr_indicator=True,
            )
            return sr_response_stock
        return response_stock_sr(price_now=current_mkt_price_now, sr_indicator=False)

    def is_fibo_validated(self, request: response_fibo_module) -> response_stock_fibo:
        """Helper function to validate fibo levels."""
        fibo_response_levels = [req.level for req in request.levels]
        current_mkt_price_now = request.cur_market_price.price_now
        support, resistance = self.find_range(
            fibo_response_levels, current_mkt_price_now
        )

        # Check is only for bullish pattern
        # For Bullish pattern suppprt is the StopLoss & resistance is the Target.
        if self.are_approximately_close(
            current_mkt_price_now, support
        ):  # if close by 2% thrshold
            sr_response_stock = response_stock_fibo(
                price_now=current_mkt_price_now,
                stop_loss=support,
                target=resistance,
                fibo_indicator=True,
            )
            return sr_response_stock
        return response_stock_fibo(
            price_now=current_mkt_price_now, fibo_indicator=False
        )

    def is_volume_validated(self, request: response_volume_module):
        """Method to validate volume indicator."""
        return request.volume_indicators.vol_indicator_check

    def is_risk_reward_validation_response(
        self, request: request_risk_reward_module
    ) -> response_risk_reward_module:
        """Method to validate Risk Reward."""
        response_risk_reward = validate_risk_reward(request)
        return response_risk_reward

    def is_stock_valid(self, request: request_all_screener_details):
        """Helper function to validate if a stock is valid."""
        try:
            all_screener_response = self.get_all_screener_details(request)
            candle_check = self.is_candle_stick_validated(
                all_screener_response.candle_stick_response
            )
            indicator_check = self.is_indicator_stock_validated(
                all_screener_response.indicator_response
            )
            volume_check = self.is_volume_validated(
                all_screener_response.volume_response
            )
            sr_validation_response = self.is_sr_stock_validated(
                all_screener_response.sr_response
            )
            sr_validation_check = sr_validation_response.sr_indicator

            fibo_validation_response = self.is_fibo_validated(
                all_screener_response.fibo_response
            )
            fibo_validation_check = fibo_validation_response.fibo_indicator

            current_market_data = request.stock_data
            current_market_price = current_market_data.iloc[-1]

            SR_EXP_RR_RATIO = 2
            risk_reward_request_sr = request_risk_reward_module(
                buy_price=current_market_price["close"],
                sell_price=sr_validation_response.target,
                stop_loss=sr_validation_response.stop_loss,
                rr_ratio=SR_EXP_RR_RATIO,
            )
            risk_reward_sr_response = self.is_risk_reward_validation_response(
                risk_reward_request_sr
            )
            risk_reward_check_sr = risk_reward_sr_response.risk_reward_check
            # TO-DO: After Validation of Support Resistance.

            # For Fibo Risk Reward Check
            FIBO_EXP_RR_RATIO = 2
            risk_reward_request_fibo = request_risk_reward_module(
                buy_price=current_market_price["close"],
                sell_price=fibo_validation_response.target,
                stop_loss=fibo_validation_response.stop_loss,
                rr_ratio=FIBO_EXP_RR_RATIO,
            )
            risk_reward_fibo_response = self.is_risk_reward_validation_response(
                risk_reward_request_fibo
            )
            risk_reward_check_fibo = risk_reward_fibo_response.risk_reward_check
            if (
                candle_check
                and indicator_check
                and volume_check
                and fibo_validation_check
                and risk_reward_check_fibo
            ):
                print("Found a Buy Call.")
                expected_profit = format_float(
                    risk_reward_fibo_response.sell_price
                    - risk_reward_fibo_response.buy_price
                )
                expected_loss = format_float(
                    risk_reward_fibo_response.buy_price
                    - risk_reward_fibo_response.stop_loss
                )
                buy_call_response = response_bull_buy_call(
                    stock_id=request.stock_id,
                    stock_name=request.stock_name,
                    cur_market_price=risk_reward_fibo_response.buy_price,
                    stoploss=risk_reward_fibo_response.stop_loss,
                    target=risk_reward_fibo_response.sell_price,
                    expected_profit=expected_profit,
                    expected_loss=expected_loss,
                    exp_risk_reward_ratio=risk_reward_fibo_response.exp_risk_reward,
                )
                # Telegram Notification , Streamline later
                buy_call_response_dict = vars(buy_call_response)
                pretty_table = PrettyTable()
                pretty_table.field_names = ["Key", "Value"]
                for key, value in buy_call_response_dict.items():
                    pretty_table.add_row([key, value])
                print(pretty_table)

                # Convert PrettyTable data to a list of dictionaries
                table_data = [
                    {"Field": row[0], "Value": row[1]} for row in pretty_table._rows
                ]

                # Convert table data to a string
                table_string = ""
                for row in table_data:
                    table_string += f"{row['Field']}: {row['Value']}\n"

                # Replace newlines with '\n' for JSON serialization
                table_string = table_string.replace("\n", "\\n")

                # Convert table data to JSON
                # json_data = json.dumps(table_data, indent=4)
                # print(buy_call_response)
                broadcast_msg(table_string)

                return buy_call_response
            """
            #To Be Enabled after Testing
            elif candle_check and indicator_check and volume_check and sr_validation_check and risk_reward_check_sr:
                print('SR Module levels Detected.')
                print(risk_reward_request_sr.__dict__)
                return all_screener_response
            """
        except Exception as e:
            print("Exception:", e)

    def recommended_stocks(self):
        """Helper method to extract stocks from the pool."""
        stock_list = StockDetails().get_stock_list()

        start_time = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for index, row in stock_list.iterrows():
                request_screener = request_all_screener_details(
                    stock_id=row["Symbol"], stock_name=row["Name"]
                )
                futures.append(
                    executor.submit(self.get_all_screener_details, request_screener)
                )

            results = []
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                print(f"Task Completed with Id: {i}")
                results.append(result)
                if len(results) % 10:
                    yield results
                    results = []
            print(f"Total Time Consumed: {time.time()-start_time}")
            # return results

    def get_buy_calls(self):
        """Helper method to extract stocks from the pool."""
        stock_list = StockDetails().get_stock_list()

        start_time = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for index, row in stock_list[:500].iterrows():
                request_screener = request_all_screener_details(
                    stock_id=row["Symbol"], stock_name=row["Name"]
                )
                futures.append(executor.submit(self.is_stock_valid, request_screener))

            # results = []
            counter = 0
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                print(f"Task Completed with Id: {i}")
                if result:
                    counter += 1
                    yield result
                    # results.append(result)
                    # if len(results) % 10:
                    #     yield results
                    #     results = []
            print(f"Total Time Consumed: {time.time()-start_time}")
            print(f"Total Buy Calls...{counter}")
