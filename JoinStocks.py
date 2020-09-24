import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import webbrowser
from dateutil.relativedelta import relativedelta
# import codecs
# from fbprophet import Prophet

def GetPlotCandlestick(dataFrame, name):
  datas = dataFrame.tail(200)
  fig = go.Figure(data=[go.Candlestick(x=datas['Date'],open=datas['Open'],high=datas['High'], low=datas['Low'], close=datas['Close'], name = name)])
  fig.add_trace(go.Scatter(x=datas['Date'], y=datas['Close5'], name ="Close5"))
  fig.add_trace(go.Scatter(x=datas['Date'], y=datas['Close28'], name ="Close28"))

  # Delt of Difference
  fig.add_trace(go.Bar(x=datas['Date'], y=datas['Diff_28-5'], name ="Diff_28-5"))


  fig.update_layout(title=name)
  return fig

def GetData(name,start,end):
    df = yf.download(name, start=start, end=end)
    df['Date'] = df.index

    rolling = df['Close'].rolling(window=5)
    df['Close5'] = rolling.mean()

    rolling = df['Close'].rolling(window=28)
    df['Close28'] = rolling.mean()

    df['Diff_28-5'] = df['Close5'].sub(df['Close28'], axis = 0) 

    return df

def GetOBV(df):
  df["OBV"] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()


def GetPlotOBV(df):
  if "OBV" not in df.columns:
    GetOBV(df)

  fig = go.Figure(go.Scatter(x=df['Date'], y=df['OBV'], name ="OBV"))
  fig.update_layout(
    autosize=False,
    width=1450,
    height=400, yaxis=dict(
        title_text="OBV",
        titlefont=dict(size=30)))
  return fig

# def PredictStock(name):
#      data = GetData(name,(datetime.today()+relativedelta(years=-1)).strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
#      df = pd.DataFrame()
#      df['y']=data['Close']
#      df['ds']=data.index
#      modelo = Prophet(daily_seasonality = True, yearly_seasonality= True)
#      modelo.fit(df)
#      futuro = modelo.make_future_dataframe(periods = 7)
#      predictions = modelo.predict(futuro)
#      fig = modelo.plot(predictions)
#      ax = fig.gca()
#      ax.set_title(name, size=34)

def JoinFigs(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")
    webbrowser.open(filename,2)


# StocksName = ["ABEV3.SA","AZUL4.SA","B3SA3.SA","BBAS3.SA","BBDC3.SA","BBDC4.SA","BBSE3.SA","BRAP4.SA","BRDT3.SA","BRFS3.SA","BRKM5.SA","BRML3.SA","BTOW3.SA","CCRO3.SA","CIEL3.SA","CMIG4.SA","COGN3.SA","CSAN3.SA","CSNA3.SA","CVCB3.SA","CYRE3.SA","ECOR3.SA","EGIE3.SA","ELET3.SA","ELET6.SA","EMBR3.SA","ENBR3.SA","EQTL3.SA","FLRY3.SA","GGBR4.SA","GNDI3.SA","GOAU4.SA","GOLL4.SA","HYPE3.SA","IGTA3.SA","IRBR3.SA","ITSA4.SA","ITUB4.SA","JBSS3.SA","LAME4.SA","LREN3.SA","MGLU3.SA","MRFG3.SA","MRVE3.SA","MULT3.SA","NTCO3.SA","PETR3.SA","PETR4.SA","QUAL3.SA","RADL3.SA","RAIL3.SA","RENT3.SA","SBSP3.SA","SMLS3.SA","SUZB3.SA","TIMP3.SA","UGPA3.SA","USIM5.SA","VALE3.SA","VIVT4.SA","VVAR3.SA","WEGE3.SA","YDUQ3.SA","GOLL4.SA"]
# StocksName = ["GGBR4.SA", "ITSA4.SA","WEGE3.SA","VVAR3.SA","VALE3.SA","SLCE3.SA","ABEV3.SA","CVCB3.SA","IRBR3.SA","PETR4.SA","TSLA34.SA","SUZB3.SA","GOAU4.SA","ELET3.SA","BIDI3.SA"]
StocksName = ["GGBR4.SA", "ITSA4.SA"]

listOfPlot = []
for Stock in StocksName:
  print(Stock)
  df = GetData(Stock,(datetime.today()+relativedelta(months=-12)).strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
  listOfPlot.append(GetPlotCandlestick(df, Stock))
  listOfPlot.append(GetPlotOBV(df))
  # lastMedianPrice = (df['High'].iloc[-1]+df['Low'].iloc[-1])/2
  # if lastMedianPrice < df['Low5'].iloc[-1] or lastMedianPrice > df['High5'].iloc[-1] :
    # PredictStock(Stock)
    # listOfPlot.append(GetPlot(df, Stock))


JoinFigs(listOfPlot)
      

