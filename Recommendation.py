import GetStocks
import CSV
import Candle
from Stock import Stock

StocksName = ['ABEV3.SA','AZUL4.SA','B3SA3.SA','BBAS3.SA','BBDC3.SA','BBDC4.SA','BBSE3.SA','BRAP4.SA','BRDT3.SA','BRFS3.SA','BRKM5.SA','BRML3.SA','BTOW3.SA','CCRO3.SA','CIEL3.SA','CMIG4.SA','COGN3.SA','CSAN3.SA','CSNA3.SA','CVCB3.SA','CYRE3.SA','ECOR3.SA','EGIE3.SA','ELET3.SA','ELET6.SA','EMBR3.SA','ENBR3.SA','EQTL3.SA','FLRY3.SA','GGBR4.SA','GNDI3.SA','GOAU4.SA','GOLL4.SA','HYPE3.SA','IGTA3.SA','IRBR3.SA','ITSA4.SA','ITUB4.SA','JBSS3.SA','LAME4.SA','LREN3.SA','MGLU3.SA','MRFG3.SA','MRVE3.SA','MULT3.SA','NATU3.SA','PCAR4.SA','PETR3.SA','PETR4.SA','QUAL3.SA','RADL3.SA','RAIL3.SA','RENT3.SA','SBSP3.SA','SMLS3.SA','SUZB3.SA','TIMP3.SA','UGPA3.SA','USIM5.SA','VALE3.SA','VIVT4.SA','VVAR3.SA','WEGE3.SA','YDUQ3.SA']
#tickers = ['ABEV3.SA']
Stocks = []
for StockName in StocksName:
    tempStock = Stock(StockName)
    #tempStock.AnalysisLastDay()
    Stocks.append(tempStock)

def myFunc(e):
  return float(e.Score)

Stocks.sort(key=myFunc)
HighestScores = Stocks[:5]
sumHighestScores = sum(c.Score for c in HighestScores)
for HighestScore in HighestScores[:5]:
    #Stock(str(Stock['Name'])).PlotCandle()
    #HighestScore.PlotCandle()
    #Stock(stock['Name']).PrintName()
    print("Name:"+str(HighestScore.Name)+" - Percentage: "+str("%.2f" %float(HighestScore.Score/sumHighestScores*100))+"%")

    print("Suporte:"+str(HighestScore.Support)+" - Resistance:"+str(HighestScore.Resistance)+" - Last High:"+str(HighestScore.LastHigh)+" - Last Low:"+str(HighestScore.LastLow))
    print("----------------------------------------")