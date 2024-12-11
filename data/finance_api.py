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
    tooltips = {}

    try:
        # General metrics
        metrics["Short Description"] = stock.info.get("longBusinessSummary", "N/A")
        metrics["Price History"] = stock.history(period="5y")
        metrics["Annualized Return"] = (
            (metrics["Price History"]["Close"][-1] / metrics["Price History"]["Close"][0]) ** (1 / 5) - 1
        ) if len(metrics["Price History"]["Close"]) > 1 else "N/A"
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Volatility"] = metrics["Price History"]["Close"].pct_change().std() * (252 ** 0.5) if not \
            metrics["Price History"]["Close"].empty else "N/A"

        # Tooltips for general metrics
        tooltips["Annualized Return"] = "The average return per year over a specific period, expressed as a percentage."
        tooltips["Market Cap"] = "The total value of a company’s outstanding shares of stock."
        tooltips["Volatility"] = "A measure of the price fluctuations of an asset. Higher volatility means larger price swings."

        # Asset-class-specific metrics
        if asset_class.lower() == "stock":
            metrics["P/E Ratio"] = stock.info.get("trailingPE", stock.info.get("priceToSalesTrailing12Months", "N/A"))
            metrics["Dividend Yield"] = stock.info.get("dividendYield", stock.info.get("trailingEps", "N/A"))
            metrics["Sector"] = stock.info.get("sector", "N/A")
            tooltips["P/E Ratio"] = "A measure of a company’s share price relative to its earnings per share."
            tooltips["Dividend Yield"] = "The annual dividend payment as a percentage of the stock's current price."
            tooltips["Sector"] = "The category of the economy a company operates in, such as technology or healthcare."

        elif asset_class.lower() == "etf":
            metrics["Expense Ratio"] = stock.info.get("expenseRatio", stock.info.get("fundOperationsExpenseRatio", "N/A"))
            metrics["Total Net Assets"] = stock.info.get("totalAssets", stock.info.get("navPrice", "N/A"))
            metrics["Top Holdings"] = stock.info.get("topHoldings", stock.info.get("annualHoldingsTurnover", "N/A"))
            tooltips["Expense Ratio"] = "The annual fee charged by a fund or ETF to manage investments."
            tooltips["Total Net Assets"] = "The total market value of the investments managed by the ETF."
            tooltips["Top Holdings"] = "The largest investments held by the ETF."

        elif asset_class.lower() == "bonds":
            metrics["Yield"] = stock.info.get("yield", stock.info.get("creditRating", "N/A"))
            metrics["Duration"] = stock.info.get("duration", "N/A")
            tooltips["Yield"] = "The return on an investment, expressed as a percentage."
            tooltips["Duration"] = "A measure of the sensitivity of a bond's price to interest rate changes."

        elif asset_class.lower() == "crypto":
            metrics["Circulating Supply"] = stock.info.get("circulatingSupply", "N/A")
            metrics["24-Hour Volume"] = stock.info.get("regularMarketVolume", "N/A")
            tooltips["Circulating Supply"] = "The total amount of a cryptocurrency that is available for trading."
            tooltips["24-Hour Volume"] = "The total volume of a cryptocurrency traded in the past 24 hours."

    except Exception as e:
        metrics["Error"] = f"An error occurred: {str(e)}"
        print(f"Error fetching metrics for {ticker}: {e}")

    return metrics, tooltips
