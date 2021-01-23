from numpy.core.fromnumeric import mean
import plotly.graph_objects as go
import plotly.express as px
from requests import NullHandler
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yahoo_fin.stock_info as si
import statistics
from Fundamentus import get_data
import math
from StocksSectors import *
# https://github.com/jealous/stockstats/blob/master/stockstats.py
from stockstats import StockDataFrame as Sdf
from enum import Enum     # for enum34, or the stdlib version
import talib as ta

GlobalDatasOfFundamentus = get_data()

class Stock:
    def GetData(self):

        self.df = self.dfRaw
        self.df['Date'] = self.df.index

        rolling = self.df['Close'].rolling(window=5)
        self.df['Close5'] = rolling.mean()

        rolling = self.df['Close'].rolling(window=28)
        self.df['Close28'] = rolling.mean()
        
        self.df['Diff_28-5'] = self.df['Close5'].sub(self.df['Close28'], axis = 0) 


    def DownLoadDataforme(self):
        start = (datetime.today()+relativedelta(months=-12)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

        self.dfRaw = yf.download(self.NameSA, start=start, end=end,actions = True)

    def __init__(self,stockName):
        self.Name = stockName
        self.NameSA = stockName+'.SA'
        self.DownLoadDataforme()
        self.GetFundamentusIndices()
        self.GetData()
        self.GetValorIntrínsecoGrahamIndices()
        self.GetGraficIndices()
        StockSector = GetStockSector(stockName)
        self.MACDAnalyze = str(self.ConvertAnalyze(self.GetMACDAnalyze()))
        self.OBVAnalyze = str(self.ConvertAnalyze(self.GetOBVAnalyze()))
        self.RSIAnalyze = str(self.ConvertAnalyze(self.GetRSIAnalyze()))
        self.StochasticAnalyze = str(self.ConvertAnalyze(self.GetStochasticAnalyze()))
        self.MomentumAnalyze = str(self.ConvertAnalyze(self.GetMomentumAnalyze()))
        
        if StockSector is None:
            print(stockName)
        else:
            self.Sector = StockSector.Sector

    def GetIndices(self):
      self.LastClose = self.df['Close'].iloc[-1]
      self.PV_Max15 = self.df[self.df.last_valid_index()-pd.DateOffset(15, 'D'):]['High'].max()
      self.PV_Min15 = self.df[self.df.last_valid_index()-pd.DateOffset(15, 'D'):]['Low'].min()
      self.PV_Max360 = self.df['High'].max()
      self.PV_Min360 = self.df['Low'].min()

    def GetProfitPower(self):
        self.GetIndices()
        range = (self.PV_Max360 - self.PV_Min360)
        self.ProfitPower = 1 - ((self.LastClose - self.PV_Min360)/range)

        self.Risco = self.PV_Min360/ self.LastClose
        self.Potencial = min(self.PV_Max360, self.TargetEst1Y) / self.LastClose
        self.Indicador = self.Potencial* self.Risco
        return

    def GetValorIntrínsecoGrahamIndices(self):
        quote = si.get_quote_table(self.NameSA)
        try:
            self.EPS = quote["EPS (TTM)"]
        except:
            print(quote["EPS (TTM)"])
            self.EPS = 0

        try:
            self.TargetEst1Y = quote["1y Target Est"]
        except:
            self.TargetEst1Y = 0

        try:     
            quote2 = si.get_stats(self.NameSA)
            self.BVPS = float(quote2[quote2['Attribute'] == "Book Value Per Share (mrq)"]['Value'].values)
        except:
            self.BVPS = 0
        try:
            self.ValorIntrínsecoGraham = math.pow((22.5*self.EPS*self.BVPS), 1/2)
        except:
            self.ValorIntrínsecoGraham = 0

    def GetFundamentusIndices(self):
        
        self.PL = GlobalDatasOfFundamentus[self.Name]["P/L"]
        self.PVP = GlobalDatasOfFundamentus[self.Name]["P/VP"]
        self.EV_EBITDA = GlobalDatasOfFundamentus[self.Name]["EV/EBITDA"]
        self.DividendYield = GlobalDatasOfFundamentus[self.Name]["DY"]

        # self.ValorIntrínsecoGraham = 0

    def GetGraficIndices(self):
        df = self.dfRaw[['Open', 'High', 'Low','Close', 'Adj Close', 'Volume']].copy()
        mystock = Sdf.retype(df)
        # Sdf.KDJ_WINDOW = 14
        # Sdf.KDJ_PARAM = (3.0 / 3.0, 1.0 / 3.0)
        self.kdjk = mystock['kdjk']
        self.kdjd = mystock['kdjd']
        self.RSI = mystock['rsi_14']
        self.OBV = ta.OBV(self.dfRaw['Close'], self.dfRaw['Volume'])
        self.Momentum = ta.MOM(self.dfRaw['Close'], timeperiod=10)
        self.MACD = mystock['macd']
        self.MACD_S = mystock['macds']

    AnalyzeStatusBuy = 0
    AnalyzeStatusSale = 1
    AnalyzeStatusNeutral = 2
    # AnalyzeStatus = Enum('Buy', 'Sale','Neutral')

    def ConvertAnalyze(self, AnalyzeStatus):
        if(AnalyzeStatus == self.AnalyzeStatusBuy):
            return 'Compra'
        if(AnalyzeStatus == self.AnalyzeStatusNeutral):
            return 'Neutro'
        if(AnalyzeStatus == self.AnalyzeStatusSale):
            return 'Venda'
        
        return 'Neutro'

    def GetMACDAnalyze(self):
        Limit = 0 
        lastMACD = self.MACD[-5:] - self.MACD_S[-5:]

        if(lastMACD[-1] < Limit and max(lastMACD) > Limit ):
            return self.AnalyzeStatusSale

        if(min(lastMACD) < Limit and lastMACD[-1] > Limit):
            return self.AnalyzeStatusBuy
        
        return self.AnalyzeStatusNeutral
    
    def GetOBVAnalyze(self):
        lastobv = self.OBV[-10:]
        SlopeLastObv = self.GetSlopeLinearRegression(lastobv)

        if SlopeLastObv  > 0.2 :
            return self.AnalyzeStatusBuy

        if SlopeLastObv  < - 0.2:
            return self.AnalyzeStatusSale

        return self.AnalyzeStatusNeutral

    def GetMomentumAnalyze(self):
        Limit = 0   
        lastRSI = self.RSI[-5:]

        if(lastRSI[-1] < Limit and max(lastRSI) > Limit ):
            return self.AnalyzeStatusSale

        if(min(lastRSI) < Limit and lastRSI[-1] > Limit):
            return self.AnalyzeStatusBuy
        
        return self.AnalyzeStatusNeutral

    def GetRSIAnalyze(self):
        maxLimit = 70   
        minLimit = 30
        lastRSI = self.RSI[-5:]

        if(lastRSI[-1] < maxLimit and max(lastRSI) > maxLimit ):
            return self.AnalyzeStatusSale

        if(min(lastRSI) < minLimit and lastRSI[-1] > minLimit):
            return self.AnalyzeStatusBuy
        
        return self.AnalyzeStatusNeutral

    def GetStochasticAnalyze(self):
        maxLimit = 80   
        minLimit = 20
        lastkdjk = self.kdjk[-5:]
        lastkdjd = self.kdjd[-5:]

        if(lastkdjk[-1] < maxLimit and max(lastkdjk) > maxLimit  and lastkdjd[-1] < maxLimit and max(lastkdjd) > maxLimit ):
            return self.AnalyzeStatusSale

        if(min(lastkdjk) < minLimit and lastkdjk[-1] > minLimit and min(lastkdjd) < minLimit and lastkdjd[-1] > minLimit ):
            return self.AnalyzeStatusBuy
        
        return self.AnalyzeStatusNeutral
    
    def GetSlopeLinearRegression(self,data):
        # data = [0.32,0.12,0.21,0.47,0.52,0.76,0.87,0.96]
        conts = list()
        for i in range(0,len(data)): 
            conts.append(i)

        x = np.array(conts) # vetor com os valores de x
        y = np.array(data) # vetor com os valores de y

        p1 = np.polyfit(x,y,1) # fornece os valores do intercepto e a inclinação

        yfit = p1[0] * x + p1[1] # calcula os valores preditos
        yresid = y - yfit # resíduo = valor real - valor ajustado (valor predito)
        SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
        SQtotal = len(y) * np.var(y) # número de elementos do vetor y vezes a variância de y
        R2 = 1 - SQresid/SQtotal # coeficiente de determinação

        # print(p1) # imprime o intercepto e a inclinação
        # print(R2) # imprime coeficiente de determinação
        
        # import matplotlib.pyplot as plt

        # plt.plot(x,y,'o')
        # plt.plot(x,np.polyval(p1,x),'g--')
        # plt.xlabel("x")
        # plt.ylabel("y")
        # plt.show()
        return p1[0]


# StocksMyName = ['ABEV3']
# for stockName in StocksMyName:
#     s = Stock(stockName)
#     s.GetIndices()
#     s.GetProfitPower()
