import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # plots
import yfinance as yf
import csv
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#import candlestick_ohlc as candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import math

def Plot1(df, name):
    #last = df.iloc[-1:]
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name=name)])
    #fig.plot(max(df.iloc[-5:].High))
    #x = np.arange(10)
    #fig.add_trace(go.Scatter(y=min(last['Low'],last['Low1'],last['Low2'],last['Low3'],last['Low4'])))
    #fig.add_trace(go.Figure(data=go.Scatter(x=x, y=min(last['Low'],last['Low1'],last['Low2'],last['Low3'],last['Low4']))))
    #fig.add_trace(go.Figure(data=go.Scatter(x=x, y=max(last['High'],last['High1'],last['High2'],last['High3'],last['Low4']))))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure3Days'], mode='lines', name='High Measure 3 Days'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure5Days'], mode='lines', name='High Measure 5 Days'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure15Days'], mode='lines', name='High Measure 15 Days'))
    #fig.add_trace(go.Bar(x=df['Date'], y=df['Volume']/5000000, name='Volume'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Buy'], mode='markers', name='markers'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Sell'], mode='markers', name='markers'))
    #go.Scatter(x=[1, 2, 3], y=[4, 5, 6], marker={'color': 'red', 'symbol': 104, 'size': "10"}, mode="markers+lines", text=["one", "two", "three"])
    #plt.plot(df.Buy, 'v', color='green')
    #plt.plot(df.Sell, '^', color='red')
    fig.show()
def Plot2(Stock):
    plt.style.use('ggplot')

    # Extracting Data for plotting
    data = pd.read_csv('candlestick_python_data.csv')
    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)

    # Creating Subplots
    fig, ax = plt.subplots()

    #candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    # Setting labels & titles
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('Daily Candlestick Chart of NIFTY50')

    # Formatting Date
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    plt.show()
