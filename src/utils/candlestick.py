from statistics import mean


def average_body(Open, Close):
    """Helper function to get the avg body size given the historic stock data."""
    return mean(abs(x - y) for x, y in zip(Open, Close))


def stock_ratio(a, b):
    """Helper to provide ratios."""
    return abs(round((a - b) / a, 2)) if a != 0 else 0
