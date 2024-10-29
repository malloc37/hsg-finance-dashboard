import yfinance as yf

def get_ticker_data(ticker):
    return yf.Ticker(ticker).history(period="5y")

def get_ticker_info(ticker):
    return yf.Ticker(ticker).info