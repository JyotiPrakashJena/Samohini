from models.risk_reward_model import (request_risk_reward_module,
                                      response_risk_reward_module)


def validate_risk_reward(request: request_risk_reward_module) -> response_risk_reward_module:
    """Validate Risk Reward Provided the Ratio."""
    expected_profit = request.sell_price - request.buy_price
    expected_loss = request.buy_price - request.stop_loss
    expected_risk_reward=float("{:.2f}".format(expected_profit/expected_loss))
    return response_risk_reward_module(buy_price=request.buy_price,
                                       sell_price=request.sell_price,
                                       rr_ratio=request.rr_ratio,
                                       stop_loss=request.stop_loss,
                                       exp_risk_reward=expected_risk_reward,
                                       risk_reward_check=expected_risk_reward>=request.rr_ratio)
