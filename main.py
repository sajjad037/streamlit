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
from utils.helper import (
    print_data_frame,
    convert_sec_to_datetime,
    convert_to_percent_str
)


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
        label="Select stock ticker",
        options=ticker_list
    )
    if ticker_symbol == "Other":
        ticker_symbol = st.sidebar.text_input(label="Enter stock ticker (Yahoo Finance)", key="txt_ticker_1")

    # Select period or enter date range
    period_list = ["custom", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    period = st.sidebar.selectbox(
        label="Select duration or period",
        options=period_list,
        index=11,
        key="sb_period_1"
    )
    ticker_start_date = None
    end_date = None
    if period == "custom":
        ticker_start_date = st.sidebar.date_input("Start date", datetime.date(datetime.date.today().year - 1, 1, 1))
        end_date = st.sidebar.date_input("End date", datetime.date.today())

    # Select interval
    interval_list = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    interval = st.sidebar.selectbox(
        label="Select interval",
        options=interval_list,
        index=8,
        key="sb_interval_1"
    )

    return ticker_symbol, period, ticker_start_date, end_date, interval


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

    print_data_frame(dividend_data, st=st)


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

    print_data_frame(target_data, st=st)


def get_filtered_dataframe_by_days(df, days):
    if days > 0:
        today = datetime.date.today()
        from_date = today - datetime.timedelta(days=days)
        return df.loc[(df.index >= from_date.strftime("%Y-%m-%d")) & (df.index <= today.strftime("%Y-%m-%d"))]
    return df


def get_min_max_from_dataframe(df):
    return df[df.Low == df.Low.min()], df[df.High == df.High.max()]


def prepare_max_min_states(df, days, min_max_state, interval_name):
    df = get_filtered_dataframe_by_days(df, days)
    if not df.empty:
        min_data, max_data = get_min_max_from_dataframe(df)
        min_date = min_data.index[0].strftime('%Y-%b-%d')
        min_value = round(min_data['Low'].values[0], 2)
        max_date = max_data.index[0].strftime('%Y-%b-%d')
        max_value = round(max_data['High'].values[0], 2)

        min_max_state["min_date"].append(min_date)
        min_max_state["min"].append(min_value)
        min_max_state["max_date"].append(max_date)
        min_max_state["max"].append(max_value)
        min_max_state["interval"].append(interval_name)


def print_max_min_states(df):

    min_max_data = {
        "interval": [],
        'min': [],
        'min_date': [],
        'max': [],
        'max_date': [],
    }

    prepare_max_min_states(
        df=df,
        days=3,
        min_max_state=min_max_data,
        interval_name="3 Days"
    )
    prepare_max_min_states(
        df=df,
        days=5,
        min_max_state=min_max_data,
        interval_name="5 Days"
    )
    prepare_max_min_states(
        df=df,
        days=8,
        min_max_state=min_max_data,
        interval_name="8 days"
    )
    prepare_max_min_states(
        df=df,
        days=13,
        min_max_state=min_max_data,
        interval_name="2 weeks (13D)"
    )
    prepare_max_min_states(
        df=df,
        days=21,
        min_max_state=min_max_data,
        interval_name="3 weeks"
    )
    prepare_max_min_states(
        df=df,
        days=34,
        min_max_state=min_max_data,
        interval_name="1 month(34D)"
    )
    prepare_max_min_states(
        df=df,
        days=60,
        min_max_state=min_max_data,
        interval_name="2 months"
    )
    prepare_max_min_states(
        df=df,
        days=89,
        min_max_state=min_max_data,
        interval_name="3 months(89D)"
    )
    prepare_max_min_states(
        df=df,
        days=150,
        min_max_state=min_max_data,
        interval_name="5 months"
    )
    prepare_max_min_states(
        df=df,
        days=180,
        min_max_state=min_max_data,
        interval_name="6 months"
    )
    prepare_max_min_states(
        df=df,
        days=365,
        min_max_state=min_max_data,
        interval_name="1 year"
    )
    prepare_max_min_states(
        df=df,
        days=730,
        min_max_state=min_max_data,
        interval_name="2 year"
    )
    prepare_max_min_states(
        df=df,
        days=1095,
        min_max_state=min_max_data,
        interval_name="3 year"
    )
    prepare_max_min_states(
        df=df,
        days=1825,
        min_max_state=min_max_data,
        interval_name="5 year"
    )
    prepare_max_min_states(
        df=df,
        days=-1,
        min_max_state=min_max_data,
        interval_name="Max"
    )

    # Add Empty row
    # min_max_data["min_date"].append("")
    # min_max_data["min"].append(0.0)
    # min_max_data["max_date"].append("")
    # min_max_data["max"].append(0.0)
    # min_max_data["interval"].append(" ")

    print_data_frame(min_max_data, st=st)


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
    print_data_frame(market_data, st=st)

    prepare_dividend_data(ticker_data.info)
    prepare_target_data(ticker_data.info)

    # Get historical prices for this ticker
    ticker_dataframe = ticker_data.history(
        period=period,
        interval=interval,
        start=start_date,
        end=end_date
    )

    st.write('---')
    st.header("Past min max states")
    print_max_min_states(ticker_dataframe)
    st.write('---')

    # Ticker historical data
    ticker_data_header = f"**Ticker data ({period}) **"
    if period == "custom":
        ticker_data_header = f"**Ticker data (from {start_date} to {end_date}) **"
    st.header(f"{ticker_data_header} Table")
    st.write(ticker_dataframe)
    st.write('---')

    # Ticker historical data Plot
    st.header(f"{ticker_data_header} Plot")
    st.line_chart(ticker_dataframe.Close)
    st.write('---')

    ticker_historical_data = get_filtered_dataframe_by_days(
        df=ticker_dataframe,
        days=3650
    )
    # Open High Low Close Volume Dividends stock Splits

    st.line_chart(ticker_historical_data.Close)
    st.line_chart(ticker_historical_data.Volume)

    # Bollinger bands
    st.header('**Bollinger Bands**')
    qf=cf.QuantFig(ticker_dataframe, title='First Quant Figure', legend='top', name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)
    st.write('---')

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
