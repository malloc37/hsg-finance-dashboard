import yfinance as yf

from components.options_list import investment_options
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

def get_ticker_data(ticker):
    return yf.Ticker(ticker).history(period="5y")

def get_ticker_info(ticker):
    return yf.Ticker(ticker).info


def get_investment_metrics(ticker, asset_class):
    """
    Retrieve investment metrics dynamically from Yahoo Finance based on the asset class.
    """
    stock = yf.Ticker(ticker)
    metrics = {}

    try:
        # General metrics
        metrics["Short Description"] = stock.info.get("longBusinessSummary", "N/A")
        metrics["Price History"] = stock.history(period="1y")
        metrics["Annualized Return"] = (
            (metrics["Price History"]["Close"][-1] / metrics["Price History"]["Close"][0]) ** (1 / 1) - 1
        ) if len(metrics["Price History"]["Close"]) > 1 else "N/A"
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Volatility"] = metrics["Price History"]["Close"].pct_change().std() * (252 ** 0.5) if not metrics["Price History"]["Close"].empty else "N/A"

        # Asset-class-specific metrics
        if asset_class.lower() == "stock":
            metrics["P/E Ratio"] = stock.info.get("trailingPE", "N/A")
            metrics["Dividend Yield"] = stock.info.get("dividendYield", "N/A")
            metrics["Sector"] = stock.info.get("sector", "N/A")

        elif asset_class.lower() == "etf":
            metrics["Expense Ratio"] = stock.info.get("expenseRatio", "N/A")
            metrics["Total Net Assets"] = stock.info.get("totalAssets", "N/A")
            metrics["Top Holdings"] = stock.info.get("topHoldings", "N/A")
            metrics["Sector Allocation"] = stock.info.get("sectorWeightings", "N/A")

        elif asset_class.lower() == "bonds":
            metrics["Yield"] = stock.info.get("yield", "N/A")
            metrics["Duration"] = stock.info.get("duration", "N/A")
            metrics["Credit Rating"] = stock.info.get("creditRating", "N/A")

        elif asset_class.lower() == "crypto":
            metrics["Circulating Supply"] = stock.info.get("circulatingSupply", "N/A")
            metrics["24-Hour Volume"] = stock.info.get("regularMarketVolume", "N/A")

    except Exception as e:
        metrics["Error"] = f"An error occurred: {str(e)}"
        print(f"Error fetching metrics for {ticker}: {e}")

    return metrics


'''
REQUIRED_METRICS = {
    "stock": ["Short Description", "Market Cap", "P/E Ratio", "Dividend Yield", "Sector"],
    "etf": ["Short Description", "Market Cap", "Expense Ratio", "Total Net Assets", "Top Holdings", "Sector Allocation"],
    "bonds": ["Short Description", "Market Cap", "Yield", "Duration", "Credit Rating"],
    "crypto": ["Short Description", "Circulating Supply", "24-Hour Volume"],
}

def check_missing_metrics(investment_options):
    """
    Check for missing metrics for each option based on asset class.
    """
    for risk_level, options in investment_options.items():
        print(f"\nRisk Level: {risk_level}")
        for option in options:
            ticker = option["Ticker"]
            asset_class = option["Asset Class"]
            metrics = get_investment_metrics(ticker, asset_class)

            # Get required metrics for the asset class
            required_metrics = REQUIRED_METRICS.get(asset_class.lower(), [])
            missing_metrics = [
                metric for metric in required_metrics
                if metric not in metrics or metrics[metric] is None or
                   (isinstance(metrics[metric], (pd.DataFrame, pd.Series)) and metrics[metric].empty)
            ]

            print(f"Instrument: {option['Instrument']} ({ticker}) - Asset Class: {asset_class}")
            if missing_metrics:
                print(f"  Missing Metrics: {', '.join(missing_metrics)}")
            else:
                print("  All required metrics are available.")


# Example usage
check_missing_metrics(investment_options)
'''