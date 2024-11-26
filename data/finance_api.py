import yfinance as yf

def get_ticker_data(ticker):
    return yf.Ticker(ticker).history(period="5y")

def get_ticker_info(ticker):
    return yf.Ticker(ticker).info

def get_investment_metrics(ticker, asset_class):
    stock = yf.Ticker(ticker)
    metrics = {}

    if asset_class.lower() == "stock":
        metrics["Short Description"] = stock.info.get("longBusinessSummary", "N/A")
        metrics["P/E Ratio"] = stock.info.get("trailingPE", "N/A")
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Dividend Yield"] = stock.info.get("dividendYield", "N/A")
        metrics["Volatility"] = stock.history(period="1y")["Close"].pct_change().std() * (252 ** 0.5)
    elif asset_class.lower() == "crypto":
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Volatility"] = stock.history(period="1y")["Close"].pct_change().std() * (252 ** 0.5)
        metrics["Circulating Supply"] = stock.info.get("circulatingSupply", "N/A")
    elif asset_class.lower() == "etf":
        metrics["Expense Ratio"] = stock.info.get("expenseRatio", "N/A")
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
    elif asset_class.lower() == "bonds":
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Duration"] = stock.info.get("duration", "N/A")
    return metrics