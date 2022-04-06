
import streamlit
import pandas as pd


def print_data_frame(data_frame, st: streamlit):
    df = pd.DataFrame(data_frame)
    # df.reset_index(drop=True, inplace=True)
    st.dataframe(df)


def convert_sec_to_datetime(seconds):
    if seconds:
        return pd.to_datetime(seconds, unit='s', utc=True).strftime('%d-%b-%Y')


def convert_to_percent_str(value):
    if value:
        return f"{round(value*100, 2)}%"