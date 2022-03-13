"""
    Simple Stock app for learning
    Learning: https://aroussi.com/post/python-yahoo-finance
    https://github.com/ranaroussi/yfinance
"""

import yfinance as yf
import streamlit as st
import pandas as pd
import cufflinks as cf
import datetime


def sidebar_elements():
    """
    Sidebar elements
    :return:
    """
    # Sidebar Header Title
    global end_date
    st.sidebar.subheader("Query parameters")

    # Select or enter symbol name
    ticker_list = ["AAPL", "FB", "NVDA", "HUT.TO", "Other"]
    ticker_symbol = st.sidebar.selectbox(
        label="Stock ticker",
        options=ticker_list
    )
    if ticker_symbol == "Other":
        ticker_symbol = st.sidebar.text_input(label="Stock ticker")

    # Select period or enter date range
    period_list = ["custom", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    period = st.sidebar.selectbox(
        label="Select duration or period",
        options=period_list,
        index=5
    )
    ticker_start_date = None
    end_date = None
    if period == "custom":
        ticker_start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
        end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

    # Select interval
    interval_list = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    interval = st.sidebar.selectbox(
        label="Select interval",
        options=interval_list,
        index=8
    )

    return ticker_symbol, period, ticker_start_date, end_date, interval


def print_data_frame(data_frame):
    df = pd.DataFrame(data_frame)
    # df.reset_index(drop=True, inplace=True)
    st.dataframe(df)


def convert_sec_to_datetime(seconds):
    if seconds:
        return pd.to_datetime(seconds, unit='s', utc=True).strftime('%d-%b-%Y')


def convert_to_percent_str(value):
    if value:
        return f"{round(value*100, 2)}%"


def prepare_dividend_data(ticker_data_info):
    dividend_data = {}

    if 'lastDividendValue' in ticker_data_info:
        dividend_data['Last Div'] = [ticker_data_info['lastDividendValue']]

    if 'lastDividendDate' in ticker_data_info:
        dividend_data['Last Div Date'] = [convert_sec_to_datetime(ticker_data_info['lastDividendDate'])]

    if 'exDividendDate' in ticker_data_info:
        dividend_data['ex Div Date'] = [convert_sec_to_datetime(ticker_data_info['exDividendDate'])]

    if 'dividendYield' in ticker_data_info:
        dividend_data['Div Yield'] = [convert_to_percent_str(ticker_data_info['dividendYield'])]

    print_data_frame(dividend_data)


def prepare_target_data(ticker_data_info):
    target_data = {}

    if 'targetLowPrice' in ticker_data_info:
        target_data['Low target'] = [ticker_data_info['targetLowPrice']]

    if 'targetMedianPrice' in ticker_data_info:
        target_data['Median target'] = [ticker_data_info['targetMedianPrice']]

    if 'targetMeanPrice' in ticker_data_info:
        target_data['Mean target'] = [ticker_data_info['targetMeanPrice']]

    if 'targetHighPrice' in ticker_data_info:
        target_data['High target'] = [ticker_data_info['targetHighPrice']]

    print_data_frame(target_data)


# Sidebar
ticker_symbol, period, start_date, end_date, interval = sidebar_elements()
if ticker_symbol:

    # Get ticker data
    ticker_data = yf.Ticker(ticker_symbol)

    st.write(f"""
    # {ticker_data.info['longName']} 
    
    Recommendation: **{ticker_data.info['recommendationKey']}**
    
    Ask: **{ticker_data.info['ask']}** ({ticker_data.info['askSize']})
    Bid: **{ticker_data.info['bid']}** ({ticker_data.info['bidSize']})\n
    volume: **{ticker_data.info['volume']}** (AVG Vol: {ticker_data.info['averageVolume']})\n
    Regular Market Price: **{ticker_data.info['regularMarketPrice']}**   Pre-Market Price: **{ticker_data.info['preMarketPrice']}**
    """)
    # st.write(ticker_data.info)

    market_data = {
        'Current': [ticker_data.info['currentPrice'], 0.0],
        'open': [ticker_data.info['open'], 0.0],
        'Low': [ticker_data.info['dayLow'], 0.0],
        'dayHigh': [ticker_data.info['dayHigh'], 0.0],
        '52 Week High': [ticker_data.info['fiftyTwoWeekHigh'], 0.0],
        '52 Week Low': [ticker_data.info['fiftyTwoWeekLow'], 0.0],
    }
    print_data_frame(market_data)

    prepare_dividend_data(ticker_data.info)
    prepare_target_data(ticker_data.info)

    # Get historical prices for this ticker
    tickerDf = ticker_data.history(
        period=period,
        interval=interval,
        start=start_date,
        end=end_date
    )

    st.write('---')

    # # Get data stock data from yahoo fiance
    # ticker_data = yf.Ticker(ticker_symbol)

    # Get historical stock data from yahoo fiance
    ticker_historical_data = ticker_data.history(period="1d", start="2010-5-31", end='2020-5-31')
    # Open High Low Close Volume Dividends stock Splits

    st.line_chart(ticker_historical_data.Close)
    st.line_chart(ticker_historical_data.Volume)


    # Ticker data
    st.header('**Ticker data**')
    st.write(tickerDf)

    # Bollinger bands
    st.header('**Bollinger Bands**')
    qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)

else:
    st.write("Please enter stock ticker name.")

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    print("Printing DF:")
    print(type(df))
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


playerstats = load_data(2020)
# print(playerstats)
