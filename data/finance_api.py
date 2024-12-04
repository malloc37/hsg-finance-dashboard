import yfinance as yf

def get_ticker_data(ticker):
    return yf.Ticker(ticker).history(period="5y")

def get_ticker_info(ticker):
    return yf.Ticker(ticker).info


def get_investment_metrics(ticker, asset_class):
    stock = yf.Ticker(ticker)
    metrics = {}

    try:
        metrics["Short Description"] = stock.info.get("longBusinessSummary", "N/A")
        metrics["Price History"] = stock.history(period="1y")
        metrics["Annualized Return"] = (
            (metrics["Price History"]["Close"][-1] / metrics["Price History"]["Close"][0]) ** (1 / 1) - 1
        ) if len(metrics["Price History"]["Close"]) > 1 else "N/A"
        metrics["Market Cap"] = stock.info.get("marketCap", "N/A")
        metrics["Volatility"] = metrics["Price History"]["Close"].pct_change().std() * (252 ** 0.5) if not metrics["Price History"]["Close"].empty else "N/A"
        #metrics["Sustainability Metrics"] = get_sustainability_metrics(ticker)

        if asset_class.lower() == "stock":
            metrics["P/E Ratio"] = stock.info.get("trailingPE", "N/A")
            metrics["Dividend Yield"] = stock.info.get("dividendYield", "N/A")
            metrics["Sector"] = stock.info.get("sector", "N/A")

        elif asset_class.lower() == "etf":
            metrics["Top Holdings"] = stock.fund_holdings if hasattr(stock, "fund_holdings") else "N/A"
            metrics["Sector Allocation"] = stock.fund_sector_weightings if hasattr(stock, "fund_sector_weightings") else "N/A"
            metrics["Expense Ratio"] = stock.info.get("expenseRatio", "N/A")
            metrics["Total Net Assets"] = stock.info.get("totalAssets", "N/A")

        elif asset_class.lower() == "bonds":
            metrics["Yield"] = stock.info.get("yield", "N/A")
            metrics["Duration"] = stock.info.get("duration", "N/A")
            metrics["Credit Rating"] = stock.info.get("creditRating", "N/A")

        elif asset_class.lower() == "crypto":
            metrics["Circulating Supply"] = stock.info.get("circulatingSupply", "N/A")
            metrics["24-Hour Volume"] = stock.info.get("regularMarketVolume", "N/A")

    except Exception as e:
        metrics["Error"] = f"An error occurred while retrieving metrics: {e}"

    return metrics