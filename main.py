import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock closing price and volume of Google!
sd
""")

ticker_symbol = "GOOGL"

# Get data stock data from yahoo fiance
ticker_data = yf.Ticker(ticker_symbol)

# Get historical stock data from yahoo fiance
ticker_historical_data = ticker_data.history(period="1d", start="2010-5-31", end='2020-5-31')
# Open High Low Close Volume Dividends stock Splits

st.line_chart(ticker_historical_data.Close)
st.line_chart(ticker_historical_data.Volume)


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
