import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # plots
import yfinance as yf
import csv
import plotly.graph_objects as go
import math
#import sklearn.preprocessing as preprocessing
#import sklearn.cross_validation as cross_validation
#from sklearn.linear_model import LinearRegression

def moving_average(series, n):
    return np.average(series[-n:])

def SaveDataframetinCSV(data,name):
    data.to_csv(name + ".csv", header=True)  # Don't forget to add '.csv' at the end of the path
    
def GetStockAndSaveinCSV(name, start, end):
    data = yf.download(name, start=start, end=end, prepost=True)
    SaveDataframetinCSV(data, name)

def PlotGrafcs(name):
    ads = pd.read_csv(name + ".csv", index_col=['Date'], parse_dates=['Date'])
    plt.figure(figsize=(15, 7))
    plt.plot(ads.High)
    plt.plot(ads.High.rolling(window=5).mean())
    plt.plot(ads.High.rolling(window=10).mean())
    plt.title(name)
    plt.grid(True)
    plt.savefig(name+'.png')

def AccumulatedValue(name):
    ads = pd.read_csv(name + ".csv")
    newAds = ads
    newAds['HighMeasure3Days'] = (ads.High.rolling(window=3).mean())
    newAds['HighMeasure5Days'] = (ads.High.rolling(window=5).mean())
    newAds['HighMeasure10Days'] = ads.High.rolling(window=10).mean()
    newAds['HighMeasure15Days'] = ads.High.rolling(window=15).mean()
    newAds['LowMeasure3Days'] = (ads.Low.rolling(window=3).mean())
    newAds['LowMeasure5Days'] = (ads.Low.rolling(window=5).mean())
    newAds['LowMeasure10Days'] = ads.Low.rolling(window=10).mean()
    newAds['LowMeasure15Days'] = ads.Low.rolling(window=15).mean()
    newAds['Buy'] = [0]*len(newAds)
    newAds['Sell'] = [0]*len(newAds)
    newAds['High1'] = ads['High'].shift(1)
    newAds['High2'] = ads['High'].shift(2)
    newAds['High3'] = ads['High'].shift(3)
    newAds['High4'] = ads['High'].shift(4)
    newAds['Low1'] = ads['Low'].shift(1)
    newAds['Low2'] = ads['Low'].shift(2)
    newAds['Low3'] = ads['Low'].shift(3)
    newAds['Low4'] = ads['Low'].shift(4)
    return newAds

    '''for index, row in newAds.iterrows():
        if float(row['High4']) > float(row['High3']) and float(row['High3']) > float(row['High2']) and float(row['High2']) > float(row['High1']) and float(row['High1']) > float(row['High'])  :
        #if float(row['High1']) > float(row['High']):
            newAds.loc[index, 'Sell'] = str(row['Sell'] + 5)
            #row['Sell'] = str(row['Sell'] + 5)
        if float(row['High4']) < float(row['High3']) and float(row['High3']) < float(row['High2']) and float(row['High2']) < float(row['High1']) and float(row['High1']) < float(row['High'])  :
        #if float(row['High1']) < float(row['High']):
            #row['Buy'] = str(row['Buy'] + 5)
            newAds.loc[index, 'Buy'] = str(row['Buy'] + 5)
    '''


def SellAndBuySimulation(df):
    accumulatedValue=0
    buyValue=0
    AbleToBuyStock=True
    for index, row in df.iterrows():
        if (float(row['High']) < float(row['HighMeasure3Days'] or row['High'] < buyValue*0.9) and (not AbleToBuyStock)):
            if(row['High'] < buyValue*0.9):
                print("STOP!")
            #sellValue=(row['High']+row['Low'])/2
            sellValue=(row['High'])
            #print("Sell Price is : "+str(sellValue))
            accumulatedValue=accumulatedValue+sellValue-buyValue
            AbleToBuyStock=True

        if float(row['High']) > float(row['HighMeasure3Days']) and AbleToBuyStock:
            #buyValue=(row['High']+row['Low'])/2
            buyValue=(row['Low'])
            #print("Buy Price is : "+str(buyValue))
            AbleToBuyStock = False
    print(accumulatedValue)
def PlotMore(df,name):

    #plt.figure(figsize=(60, 28))
    plt.figure(figsize=(30, 14))
    plt.plot(df.High)
    plt.plot(df.Low)
    #plt.plot(df.HighMeasure10Days)
    plt.plot(df.HighMeasure15Days)
    #plt.plot(df.LowMeasure10Days)
    plt.plot(df.LowMeasure15Days)
    #plt.plot(df.Measure5Days)
    #plt.plot(df.Measure3Days)
    plt.plot(df.High)
    plt.plot(df.Buy, 'v', color='green')
    plt.plot(df.Sell, '^', color='red')
    plt.title(name)
    plt.grid(True)
    plt.savefig(name + '.png')


def ReadCSV(name):
    with open(name + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print({", ".join(row)})
                line_count += 1
            else:
                print('\t{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}.')
                line_count += 1
        print('Processed {line_count} lines.')

def PlotCandle(name):
    #df = pd.read_csv(name + ".csv")
    df = AccumulatedValue(name)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name=name)])
    fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure3Days'], mode='lines', name='High Measure 3 Days'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure5Days'], mode='lines', name='High Measure 5 Days'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['HighMeasure15Days'], mode='lines', name='High Measure 15 Days'))
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume']/5000000, name='Volume'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Buy'], mode='markers', name='markers'))
    #fig.add_trace(go.Scatter(x=df['Date'], y=df['Sell'], mode='markers', name='markers'))
    #go.Scatter(x=[1, 2, 3], y=[4, 5, 6], marker={'color': 'red', 'symbol': 104, 'size': "10"}, mode="markers+lines", text=["one", "two", "three"])
    #plt.plot(df.Buy, 'v', color='green')
    #plt.plot(df.Sell, '^', color='red')
    fig.show()

TickerA = 'BPAC11.SA'

tickers = ['ABEV3.SA','AZUL4.SA','B3SA3.SA','BBAS3.SA','BBDC3.SA','BBDC4.SA','BBSE3.SA','BRAP4.SA','BRDT3.SA','BRFS3.SA','BRKM5.SA','BRML3.SA','BTOW3.SA','CCRO3.SA','CIEL3.SA','CMIG4.SA','COGN3.SA','CSAN3.SA','CSNA3.SA','CVCB3.SA','CYRE3.SA','ECOR3.SA','EGIE3.SA','ELET3.SA','ELET6.SA','EMBR3.SA','ENBR3.SA','EQTL3.SA','FLRY3.SA','GGBR4.SA','GNDI3.SA','GOAU4.SA','GOLL4.SA','HYPE3.SA','IGTA3.SA','IRBR3.SA','ITSA4.SA','ITUB4.SA','JBSS3.SA','LAME4.SA','LREN3.SA','MGLU3.SA','MRFG3.SA','MRVE3.SA','MULT3.SA','NATU3.SA','PCAR4.SA','PETR3.SA','PETR4.SA','QUAL3.SA','RADL3.SA','RAIL3.SA','RENT3.SA','SBSP3.SA','SMLS3.SA','SUZB3.SA','TIMP3.SA','UGPA3.SA','USIM5.SA','VALE3.SA','VIVT4.SA','VVAR3.SA','WEGE3.SA','YDUQ3.SA']
#tickers = [TickerA]
#for t in tickers:
    #GetStockAndSaveinCSV(t, start="2019-08-01", end="2019-11-01")
    # ReadCSV(t)
    #PlotGrafcs(t)
    #Machine(t)
    #PlotMore(AccumulatedValue(t), t)
    #SellAndBuySimulation(AccumulatedValue(t))
    #SaveDataframetinCSV(AccumulatedValue(t), t+"New")
    #PlotCandle(t)
    #Teste(t)
    #SaveDataframetinCSV(AccumulatedValue(t), t)

def DailyAnalysis(dfstock):
    last = dfstock.iloc[-1:]
    return float(last['HighMeasure3Days']-last['High'])

Stocks=[]
for t in tickers:
    dfstock = pd.read_csv(t + ".csv", index_col=['Date'], parse_dates=['Date'])
    Stocks.append({'Name':str(t), 'Difference': str(DailyAnalysis(dfstock))})

def myFunc(e):
  return e['Difference']

Stocks.sort(key=myFunc)
for Stock in Stocks:
    print("Name:"+str(Stock['Name'])+" - Difference:"+str(Stock['Difference']))